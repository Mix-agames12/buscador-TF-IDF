# 🔍 Buscador TF-IDF Avanzado

Sistema de recuperación de información inteligente basado en el algoritmo TF-IDF (Term Frequency-Inverse Document Frequency) con interfaz web y visualizaciones interactivas.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura del Proyecto](#-arquitectura-del-proyecto)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Funcionalidades Detalladas](#-funcionalidades-detalladas)
- [API Endpoints](#-api-endpoints)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Contribución](#-contribución)

## ✨ Características

### 🎯 Funcionalidades Principales

- **Búsqueda Inteligente**: Algoritmo TF-IDF para ranking de relevancia
- **Soporte Multi-formato**: Compatible con PDF, DOCX y TXT
- **Interfaz Moderna**: Diseño responsivo con efectos visuales
- **Análisis Detallado**: Conteo de coincidencias por documento
- **Descarga Directa**: Acceso inmediato a documentos desde los resultados

### 🚀 Características Avanzadas

- ⚡ **Búsqueda en tiempo real** con medición de velocidad (ms)
- 📊 **Gráficos duales** mostrando relevancia y coincidencias
- 🎨 **Efectos de feedback** y animaciones suaves
- 🔗 **Enlaces directos** a documentos para descarga
- 🏷️ **Tarjetas informativas** con métricas detalladas

## 🏗️ Arquitectura del Proyecto

```
search-engine/
│
├── 📁 documents/              # Carpeta con documentos a indexar
│   ├── documento1.txt
│   ├── documento2.docx
│   └── documento3.txt
│
├── 🐍 app.py                  # Servidor Flask principal
├── 📋 requirements.txt        # Dependencias del proyecto
│
├── 📁 templates/
│   └── 🌐 index.html          # Interfaz web 
│
├── 📁 static/ (opcional)
│   └── 🎨 style.css          # Estilos adicionales
│
└── 📁 utils/
    └── 🔧 tfidf.py            # Funciones de procesamiento TF-IDF
```

## 🛠️ Instalación

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Paso a paso

1. **Clona el repositorio**

2. **Instala las dependencias**

```bash
pip install -r requirements.txt
```


3. **Ejecuta la aplicación**

```bash
python app.py
```

7. **Accede a la aplicación**
   - Abre tu navegador en: `http://localhost:5000`

## 🎯 Uso

### Búsqueda Básica


1. Ingresa tu consulta en la barra de búsqueda
2. Haz clic en "_Buscar_" o presiona Enter
3. Revisa los resultados ordenados por relevancia

### Interpretando Resultados

- **Relevancia**: Puntaje TF-IDF (0.0 - 1.0)
- **Coincidencias**: Número de veces que aparece la consulta
- **Vista Previa**: Extracto del contenido del documento

### Acceso a Documentos

- Haz clic en el nombre del documento para descargarlo
- Los archivos se descargan directamente desde el servidor

## 🔍 Funcionalidades Detalladas

### Algoritmo TF-IDF

```python
TF-IDF = TF(t,d) × IDF(t,D)
```

- **TF**: Frecuencia del término en el documento
- **IDF**: Frecuencia inversa en la colección
- **Resultado**: Relevancia ponderada del documento

### Procesamiento de Texto

- **Normalización**: Eliminación de acentos y conversión a minúsculas
- **Tokenización**: Extracción de palabras significativas
- **Stop Words**: Filtrado de palabras comunes en español
- **Limpieza**: Remoción de palabras menores a 3 caracteres

### Formatos Soportados

| Formato | Extensión | Descripción |
|---------|-----------|-------------|
| Word | `.docx` | Documentos Microsoft Word |
| Texto | `.txt` | Archivos de texto plano |

## 🌐 API Endpoints

### `GET /`

**Descripción**: Página principal del buscador

- **Respuesta**: Interfaz HTML del buscador

### `GET /search`

**Descripción**: Realizar búsqueda en documentos

- **Parámetros**:
  - `q` (string): Consulta de búsqueda
- **Respuesta**: Resultados con métricas y visualizaciones

### `GET /open_document/<filename>`

**Descripción**: Descargar documento específico

- **Parámetros**:
  - `filename` (string): Nombre del archivo
- **Respuesta**: Descarga directa del archivo

## 🔧 Tecnologías Utilizadas

### Backend

- **Flask**: Framework web de Python
- **scikit-learn**: Algoritmos de machine learning
- **NLTK**: Procesamiento de lenguaje natural
- **python-docx**: Lectura de archivos DOCX

### Frontend

- **HTML**: Estructura semántica
- **CSS**: Estilos modernos con gradientes
- **JavaScript**: Interactividad y efectos

### Tarjetas de Resultados

```
📄 [Nombre del Documento - Clickeable]
├── 🎯 Relevancia: 0.8542
├── 🔢 Coincidencias: 15
└── 📝 Vista Previa: "Extracto del contenido..."
```

## ⚡ Optimizaciones

### Performance

- **Índice Pre-calculado**: Matriz TF-IDF se genera al inicio
- **Caché en Memoria**: Documentos procesados se mantienen en RAM
- **Vectorización Eficiente**: Uso de sklearn para cálculos matriciales

### UX/UI

- **Feedback Visual**: Indicadores de carga y estado
- **Validación de Entrada**: Prevención de búsquedas vacías
- **Animaciones Staggered**: Aparición progresiva de resultados

## 🐛 Solución de Problemas

### Problemas Comunes

#### Error: "No module named 'nltk'"

```bash
pip install nltk
python -c "import nltk; nltk.download('stopwords')"
```

#### Sin resultados en búsqueda

- Verifica que los documentos contengan texto extraíble
- Intenta con términos más específicos
- Revisa que los archivos no estén corruptos

### Logs de Depuración

```python
# En app.py, activa el modo debug
app.run(debug=True)
```


## 👨‍💻 Autores

- **[Anthony Guerra](https://github.com/tu-usuario)**
- **[Sebastian Guerrero](https://github.com/Alejandro512)** 


---

⭐ **¡Dale una estrella si este proyecto te fue útil!** ⭐
