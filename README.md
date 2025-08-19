**PROYECTO: Análisis de Sentimientos de reseñas de productos de amazon**

**DESCRIPCIÓN DEL PROYECTO**

Este proyecto es una Plataforma de Análisis de Sentimientos en Tiempo Real para e-commerce. Nuestro objetivo principal es ayudar a las empresas a monitorear automáticamente las reseñas de productos y las menciones en redes sociales, identificando rápidamente problemas de calidad y oportunidades de mejora.

El objetivo principal es ayudar a las empresas a monitorear automáticamente las reseñas y menciones, identificando rápidamente:

- Opiniones positivas, negativas o neutras.

- Problemas específicos de precio, calidad o envío.

- Nivel de urgencia para priorizar la atención al cliente.

El sistema utiliza modelos de Procesamiento del Lenguaje Natural (NLP) para procesar grandes volúmenes de texto en tiempo real, permitiendo a las empresas actuar de manera proactiva en su servicio al cliente y estrategia de producto.

**ACCESO AL DASHOARD:**

Puedes acceder al dashboard en producción aquí:

<p align="center"> <a href="https://proyectog4analisisdesentimientos-production.up.railway.app/" target="_blank"> <img src="https://img.shields.io/badge/Dashboard-Online-success?style=for-the-badge&logo=streamlit" alt="Dashboard Online"/> </a> </p>

**CARATERÍSTICAS PRINCIPALES:**

- Análisis de Sentimientos: Clasifica el texto en positivo, negativo o neutro.

- Análisis de Sentimientos Basado en Aspectos (ABSA): Identifica y evalúa el sentimiento sobre aspectos específicos del producto o servicio (ej. precio, calidad, envío).

- Detección de Urgencia: Clasifica los comentarios negativos o problemas según su nivel de urgencia para priorizar las acciones.

- Procesamiento en Tiempo Real: Capaz de procesar flujos de datos continuos desde diversas fuentes.

- Sistema distribuido: Al utilizar Kafka es necesario desplegar diferentes servicios que se comuniquen a traves del broker, para ello se utiliza un monorepo en donde cada cada servicio tendrá su requirement.text y main.py respectivamente.
  
**ESTRUCTURA DEL PROYECTO** 
```
├── api/                        # Microservicio de la API (FastAPI)
│   ├── app.py                  # Aplicación principal de la API
│   ├── routes/                 # Definición de endpoints
│   ├── schemas/                # Definiciones de datos y validaciones
│   └── src/utils/              # Funciones de apoyo para la API
│   └── requirements.txt        # Dependencias necesarias para la API
│
├── dashboard/                  # Código del dashboard de visualización (Streamlit)
│   ├── src/                    # Código fuente del dashboard
│   ├── pruebas/                # Evidencias y versiones de prueba del panel
│   └── requirements.txt        # Dependencias del dashboard
│
├── data/                       # Datos utilizados en el proyecto
│   ├── raw/                    # Datos originales (Amazon Product Reviews)
│   ├── processed/              # Datos limpios y balanceados listos para modelado
│   └── external/               # Datos externos o de terceros
│
├── docker/                     # Archivos para la contenerización del proyecto
│   ├── absa/                   # Imagen para el módulo ABSA
│   │   └── requirements.txt    # Dependencias del contenedor ABSA
│   └── baseline/               # Imagen para el modelo baseline
│       └── requirements.txt    # Dependencias del contenedor baseline
│
├── docs/                       # Documentación adicional del proyecto
│   ├── images/                 # Imágenes de resultados y visualizaciones
│   └── reports/                # Reportes técnicos y logs de experimentos
│
├── models/                     # Modelos y configuraciones
│   ├── trained_models/         # Modelos entrenados (.joblib, transformers)
│   └── model_configs/          # Archivos de configuración de modelos (.json)
│
├── notebooks/                  # Jupyter notebooks del proyecto
│   ├── exploratory/            # Análisis exploratorio de datos (EDA)
│   ├── modeling/               # Entrenamiento y pruebas de modelos
│   └── evaluation/             # Pruebas dashboard local
│
├── test/                       # Pruebas unitarias e integración
│
├── utils/                      # Funciones genéricas de apoyo (logging, métricas, etc.)
│
├── .gitignore                  # Archivos/carpetas a ignorar por Git
├── Informe_Tecnico             # Archivo PDF, explicación proyecto
└── README.md                   # Documentación principal del proyecto
               
```
**Resultados y Evidencia**

Los principales resultados del proyecto se encuentran en:

- EDA: Distribución de reseñas y palabras más frecuentes.
  
**Figura 1.** Distribución de longitud de reseñas.
<img width="1890" height="1406" alt="01_distribucion_longitud_resenas" src="https://github.com/user-attachments/assets/81a31923-ff30-46a0-ad73-cdf5d5635ccd" />

**Figura 2.** Cantidad de menciones por aspecto (precio, calidad y envío).
<img width="1890" height="1406" alt="01_menciones_por_aspecto" src="https://github.com/user-attachments/assets/a3ea2107-d991-4d0e-8437-084cd2b80494" />

Modelos:

- Baseline con TF-IDF + Regresión Logística.

- BERT Tiny con embeddings preentrenados.

- ABSA: detección de opiniones sobre precio, calidad y envío.
  
**Figura 3.** Rendimiento del modelo ABSA — F1 por aspecto.
<img width="689" height="390" alt="04_absa_f1 (1)" src="https://github.com/user-attachments/assets/827b181a-3367-4866-8de1-3de095f4a6ec" />

- Dashboard: visualización de KPIs (porcentaje de reseñas negativas, urgencia alta, top aspectos con problemas, tendencias).

**Figura 4.** Dashboard con KPIs de análisis de sentimientos.
![WhatsApp Image 2025-08-18 at 21 35 05](https://github.com/user-attachments/assets/53d3c497-1030-4c1a-946c-7a95c031b285)

 Ver carpeta docs/images/ para las evidencias del dashboard.
 
**ARQUITECTURA DEL PROYECTO**

El sistema está diseñado bajo un enfoque de microservicios que se comunican a través de Apache Kafka. La idea es mantener los componentes desacoplados, escalables y fáciles de mantener.

**Figura 5.** Arquitectura de microservicios desplegada en Railway.
![WhatsApp Image 2025-08-18 at 21 34 12](https://github.com/user-attachments/assets/57522364-6f99-42b0-aadf-a1792641bf22)

La API recoge las respuestas y las entrega al Dashboard, que las muestra al usuario.
El sistema está diseñado bajo un enfoque de microservicios que se comunican a través de Apache Kafka. La idea es mantener los componentes desacoplados, escalables y fáciles de mantener.

- Modelos: contienen los algoritmos de análisis de sentimientos y de aspectos. Se conectan a Kafka para procesar los mensajes y devolver resultados.

- Kafka: funciona como el bus de mensajería que conecta todos los servicios, asegurando comunicación confiable y asíncrona.

- API: actúa como la puerta de entrada al sistema. Se comunica con Kafka para enviar solicitudes y obtener respuestas de los modelos.

- Dashboard: es la interfaz visual para el usuario final. Consulta a la API y muestra los resultados y métricas en tiempo real.

**FLUJO DE DATOS**

1. El usuario interactúa con el Dashboard.

2. El Dashboard envía la solicitud a la API.

3. La API publica la solicitud en Kafka.

4. Los modelos consumen los mensajes, procesan los datos y envían la respuesta a Kafka.

5. La API recoge las respuestas y las entrega al Dashboard, que las muestra al usuario.

**CONCLUSIONES**

El proyecto demostró que es posible integrar modelos de análisis de sentimientos y ABSA en un sistema distribuido basado en microservicios. 
Gracias al uso de Kafka, la arquitectura es escalable, resiliente y permite procesar datos en tiempo real de manera eficiente.

Los experimentos mostraron un buen desempeño en la detección de sentimientos y en el análisis por aspectos clave como precio, calidad y envío, 
logrando métricas consistentes en distintos escenarios.

Como trabajo futuro, se propone ampliar la cobertura de aspectos analizados, optimizar los modelos con técnicas más avanzadas de NLP, 
y explorar integraciones adicionales con sistemas de notificación y alertas en entornos productivos.


**COLABORADORES DEL PROYECTO**

- David Francisco Alvarez Alvarez
- Marcelo Xavier Castillo Valverde 
- Alejandro Sebastian Castro Nasevilla
- Lady Anahi Garces velasco
- Daniela Estefania Pezantez Chimbo
- María Mercedes Vera Letamendi

