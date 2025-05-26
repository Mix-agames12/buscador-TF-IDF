import os
import re
import unicodedata
from sklearn.feature_extraction.text import TfidfVectorizer
from docx import Document
import PyPDF2
from multiprocessing import Pool, cpu_count
import nltk
from nltk.corpus import stopwords

# Descargar stopwords si no están disponibles
try:
    stop_words = set(stopwords.words('spanish'))
except LookupError:
    print("Descargando stopwords de NLTK...")
    nltk.download('stopwords')
    stop_words = set(stopwords.words('spanish'))

def normalize(texto: str) -> str:
    """Quita tildes y pasa a minúsculas"""
    sin_tildes = unicodedata.normalize("NFKD", texto)\
                  .encode("ASCII", "ignore")\
                  .decode("ASCII")
    return sin_tildes.lower()

def read_docx(path):
    """Función para leer archivos .docx"""
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs])

def read_pdf(path):
    """Función para leer archivos PDF"""
    with open(path, "rb") as f:
        lector = PyPDF2.PdfReader(f)
        texto = ""
        for página in lector.pages:
            texto += página.extract_text() or ""
        return normalize(texto)

def process_single_file(file, directory):
    if file.startswith('~$') or file.startswith('.'):
        return None

    path = os.path.join(directory, file)
    text = ""

    try:
        if file.lower().endswith('.docx'):
            text = read_docx(path)
        elif file.lower().endswith('.txt'):
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
        elif file.lower().endswith('.pdf'):
            text = read_pdf(path)
        else:
            return None
    except Exception as e:
        print(f"Error procesando {file}: {e}")
        return None

    original_text = text
    tokens = re.findall(r"\w+", text.lower())
    tokens = [t for t in tokens if t not in stop_words and len(t) > 2]
    processed_text = " ".join(tokens)

    if not processed_text.strip():
        return None

    return {
        'filename': file,
        'content': processed_text,
        'original_content': original_text
    }

def preprocess_documents(directory):
    files = os.listdir(directory)
    file_paths = [(file, directory) for file in files]

    # Usar map secuencial para compatibilidad con Flask/Windows
    results = [process_single_file(file, directory) for file in files]

    documents = [r for r in results if r is not None]
    corpus = [d['content'] for d in documents]

    if not corpus:
        return [], None, []

    vectorizer = TfidfVectorizer(max_features=1000, min_df=1)
    tfidf_matrix = vectorizer.fit_transform(corpus)
    return documents, tfidf_matrix, vectorizer.get_feature_names_out()

def search_query(query, documents, tfidf_matrix, feature_names):
    """Búsqueda de consulta y ranking por similitud coseno"""
    if not documents or tfidf_matrix is None:
        return []

    from sklearn.metrics.pairwise import cosine_similarity

    tokens = re.findall(r"\w+", query.lower())
    tokens = [t for t in tokens if t not in stop_words and len(t) > 2]
    query_str = " ".join(tokens)

    if not query_str:
        return []

    vectorizer = TfidfVectorizer(vocabulary=feature_names)
    query_vec = vectorizer.fit_transform([query_str])
    scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
    ranked = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)

    return [
        {
            'filename': doc['filename'],
            'score': round(score, 4),
            'content': doc['content'],
            'original_content': doc.get('original_content', doc['content'])
        }
        for doc, score in ranked if score > 0
    ]

def get_word_count_in_document(query, document_content):
    """Cuenta cuántas veces aparece una palabra o frase en un documento"""
    query_lower = query.lower()
    content_lower = document_content.lower()
    phrase_count = content_lower.count(query_lower)

    words = re.findall(r'\b\w+\b', query_lower)
    word_counts = {word: content_lower.count(word) for word in words if len(word) > 2}

    return phrase_count if phrase_count > 0 else sum(word_counts.values())