import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from docx import Document
import PyPDF2
import unicodedata

# Asegurar que las stopwords estén disponibles
try:
    stop_words = set(stopwords.words('spanish'))
except LookupError:
    import nltk
    nltk.download('stopwords')
    stop_words = set(stopwords.words('spanish'))

def normalize(texto: str) -> str:
    """Quita tildes y pasa a minúsculas"""
    sin_tildes = unicodedata.normalize("NFKD", texto)\
                  .encode("ASCII", "ignore")\
                  .decode("ASCII")
    return sin_tildes.lower()

def read_docx(path):
    # Función para leer archivos .docx
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs])

def read_pdf(path):
    # Función para leer archivos PDF
    with open(path, "rb") as f:
        lector = PyPDF2.PdfReader(f)
        texto = ""
        for página in lector.pages:
            texto += página.extract_text() or ""
        return normalize(texto)

def preprocess_documents(directory):
    # Preprocesamiento de documentos y cálculo de la matriz TF-IDF
    files = os.listdir(directory)
    corpus = []
    documents = []

    for file in files:
        # Omitir archivos temporales de Word y nombres ocultos
        if file.startswith('~$') or file.startswith('.'):
            continue
            
        path = os.path.join(directory, file)
        text = ""
        
        # Leer contenido según extensión
        try:
            if file.lower().endswith('.docx'):
                text = read_docx(path)
            elif file.lower().endswith('.txt'):
                with open(path, 'r', encoding='utf-8') as f:
                    text = f.read()
            elif file.lower().endswith('.pdf'):
                text = read_pdf(path)
            else:
                continue
        except Exception as e:
            print(f"Error procesando {file}: {e}")
            continue

        # Tokenización simple con regex
        original_text = text  # Guardar texto original para conteo
        tokens = re.findall(r"\w+", text.lower())
        tokens = [t for t in tokens if t not in stop_words and len(t) > 2]
        processed_text = " ".join(tokens)

        # Solo incluir documentos con contenido relevante
        if processed_text.strip():
            documents.append({
                'filename': file, 
                'content': processed_text,
                'original_content': original_text
            })
            corpus.append(processed_text)

    if not corpus:
        return [], None, []

    vectorizer = TfidfVectorizer(max_features=1000, min_df=1)
    tfidf_matrix = vectorizer.fit_transform(corpus)
    return documents, tfidf_matrix, vectorizer.get_feature_names_out()

def search_query(query, documents, tfidf_matrix, feature_names):
    # Búsqueda de consulta y ranking por similitud coseno
    if not documents or tfidf_matrix is None:
        return []
        
    from sklearn.metrics.pairwise import cosine_similarity

    # Procesar la consulta
    tokens = re.findall(r"\w+", query.lower())
    tokens = [t for t in tokens if t not in stop_words and len(t) > 2]
    query_str = " ".join(tokens)

    if not query_str:
        return []

    # Vectorizar con el vocabulario existente
    vectorizer = TfidfVectorizer(vocabulary=feature_names)
    query_vec = vectorizer.fit_transform([query_str])

    # Calcular similitud y ordenar resultados
    scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
    ranked = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)

    # Devolver solo resultados con puntuación positiva
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
    # Cuenta cuántas veces aparece una palabra o frase en un documento
    query_lower = query.lower()
    content_lower = document_content.lower()
    
    # Contar coincidencias exactas de la frase completa
    phrase_count = content_lower.count(query_lower)
    
    # Contar palabras individuales
    words = re.findall(r'\b\w+\b', query_lower)
    word_counts = {}
    
    for word in words:
        if len(word) > 2:  # Ignorar palabras muy cortas
            word_counts[word] = content_lower.count(word)
    
    # Si hay coincidencia exacta de frase, usar esa
    if phrase_count > 0:
        return phrase_count
    
    # Si no, usar la suma de palabras individuales
    return sum(word_counts.values()) if word_counts else 0