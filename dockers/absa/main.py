from pathlib import Path
import os
import joblib
import warnings

warnings.filterwarnings("ignore")

MODELS_DIR = Path(os.getenv("MODELS_DIR", "/app/models"))

print(f"🔎 Buscando modelos en {MODELS_DIR} ...")

def _aspect_from_filename(p: Path) -> str:
    name = p.stem
    name = name.replace("04_aspect_", "").replace("_clf", "")
    return name

def load_models(models_dir: Path, min_size_bytes: int = 1024) -> dict:
    models = {}
    if not models_dir.exists():
        print(f"⚠️ Carpeta {models_dir} no existe. Arrancando sin modelos.")
        return models

    for path in sorted(models_dir.glob("04_aspect_*_clf.joblib")):
        size = path.stat().st_size
        print(f" - {path.name}  ({size} bytes)")
        if size < min_size_bytes:
            print(f"   ↪️  Omitido: archivo demasiado pequeño (posible vacío/corrupto).")
            continue

        try:
            bundle = joblib.load(path)
        except Exception as e:
            print(f"   ↪️  Omitido: error al cargar {path.name}: {e}")
            continue

        model = None
        preproc = None
        if isinstance(bundle, dict):
            model = bundle.get("model") or bundle.get("pipeline") or bundle.get("clf")
            preproc = bundle.get("preproc") or bundle.get("vectorizer") or bundle.get("tfidf")
        else:
            model = bundle

        if model is None:
            print(f"   ↪️  Omitido: bundle sin 'model' válido en {path.name}")
            continue

        aspect = _aspect_from_filename(path)
        models[aspect] = {"model": model, "preproc": preproc}
        print(f"   ✅ Cargado modelo para aspecto: {aspect}")

    return models

MODELS = load_models(MODELS_DIR)

if not MODELS:
 
    print("Models")
 
