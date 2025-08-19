import os, json, time, joblib, glob, re
from pathlib import Path
from confluent_kafka import Consumer, Producer

BOOTSTRAP = os.getenv("KAFKA_BROKERS", "kafka:9092")
GROUP_ID  = os.getenv("GROUP_ID", "absa-consumer")
TOPIC_IN  = os.getenv("TOPIC_IN", "ml.absa.in")
TOPIC_OUT = os.getenv("TOPIC_OUT", "ml.absa.out")
MODELS_DIR= os.getenv("MODELS_DIR", "/app/models")

MODELS_PATH = Path(MODELS_DIR)
MODELS_PATH.mkdir(parents=True, exist_ok=True)

def is_lfs_pointer(p: Path) -> bool:
    try:
        head = p.read_bytes()[:200]
        return b"git-lfs.github.com/spec/v1" in head
    except Exception:
        return False

def load_bundle(path: Path):
    """
    Devuelve (model, preproc, kind):
      - kind='pipeline' si es un Pipeline o estimador que acepta texto
      - kind='pair'     si es (model, preproc)
      - kind='dict'     si viene dict con 'model' y opcional 'preproc'
    """
    obj = joblib.load(path)

    # 1) dict {"model":..., "preproc":...}
    if isinstance(obj, dict) and "model" in obj:
        return obj["model"], obj.get("preproc"), "dict"

    # 2) tuple (model, preproc)
    if isinstance(obj, tuple) and len(obj) == 2:
        return obj[0], obj[1], "pair"

    # 3) Pipeline/estimador directo
    return obj, None, "pipeline"

# ---- Cargar todos los modelos 04_aspect_*_clf.joblib ----
ASPECT_MODELS = {}

paths = sorted(MODELS_PATH.glob("04_aspect_*_clf.joblib"))
print(f"🔎 Buscando modelos en {MODELS_PATH} ...")
for p in paths:
    try:
        print(f" - {p.name}  ({p.stat().st_size} bytes)")
    except Exception:
        print(f" - {p.name}  (no se pudo leer tamaño)")

if not paths:
    raise RuntimeError(f"No hay modelos de aspecto en {MODELS_DIR}/04_aspect_*_clf.joblib")

# Verifica punteros LFS
for p in paths:
    if is_lfs_pointer(p):
        raise RuntimeError(
            f"El archivo {p} es un PUNTERO de Git LFS, no el binario del modelo.\n"
            "Soluciones: sube el .joblib real (sin LFS) o descárgalo en el Dockerfile."
        )

for path in paths:
    try:
        model, pre, kind = load_bundle(path)
    except Exception as e:
        raise RuntimeError(f"Error al cargar {path.name}: {e}")

    aspect = re.sub(r"^04_aspect_|_clf\.joblib$", "", path.name)
    ASPECT_MODELS[aspect] = (model, pre, kind)

print("✅ ABSA loaded aspects:", ", ".join(sorted(ASPECT_MODELS.keys())))

def infer_all(payload: dict | str):
    text = payload["text"] if isinstance(payload, dict) else str(payload)
    results = {}
    for aspect, (model, pre, kind) in ASPECT_MODELS.items():
        if kind == "pipeline":
            # pipeline/estimador que acepta texto directamente
            y = model.predict([text])[0]
        elif pre is not None:
            X = pre.transform([text])
            y = model.predict(X)[0]
        else:
            # sin preproc: intenta con texto crudo como vector de 1 elem.
            y = model.predict([text])[0]
        results[aspect] = y
    return results

# ---- Kafka clients ----
c = Consumer({
    "bootstrap.servers": BOOTSTRAP,
    "group.id": GROUP_ID,
    "auto.offset.reset":"earliest",
    "enable.auto.commit": True
})
p = Producer({"bootstrap.servers": BOOTSTRAP})

def main():
    c.subscribe([TOPIC_IN])
    print(f"🎧 ABSA listening: {TOPIC_IN}")
    try:
        while True:
            m = c.poll(1.0)
            if not m:
                continue
            if m.error():
                print("KafkaErr:", m.error())
                continue
            try:
                evt = json.loads(m.value().decode("utf-8"))
                cid = evt.get("correlation_id", "no-cid")
                res = infer_all(evt.get("payload", ""))
                out = {"correlation_id": cid, "result": res, "ts": time.time()}
                p.produce(TOPIC_OUT, json.dumps(out).encode("utf-8"), key=cid)
                p.poll(0)
                print("✅ processed:", out)
            except Exception as e:
                print("❌ processing error:", e)
    finally:
        c.close()
        p.flush()

if __name__ == "__main__":
    main()
