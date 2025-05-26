from flask import Flask, request, render_template, send_from_directory
from utils.tfidf import preprocess_documents, search_query, get_word_count_in_document
import os
import time

app = Flask(__name__)

# Definir la ruta y asegurar que exista
docs_path = os.path.join(os.path.dirname(__file__), 'documents')
if not os.path.exists(docs_path):
    os.makedirs(docs_path)  # opcional: crea el directorio si no existe

# Preprocesar documentos si la carpeta existe y contiene archivos válidos
try:
    documents, tfidf_matrix, feature_names = preprocess_documents(docs_path)
except FileNotFoundError:
    documents, tfidf_matrix, feature_names = [], None, []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search')
def search():
    start_time = time.time()
    query = request.args.get('q')

    if not query:
        return render_template('index.html', results=[], query="", search_time=0)

    results = search_query(query, documents, tfidf_matrix, feature_names)
    enriched_results = []
    for result in results:
        word_count = get_word_count_in_document(query, result['original_content'])
        enriched_results.append({
            'filename': result['filename'],
            'score': result['score'],
            'word_count': word_count,
            'content': result['original_content'][:200] + '...' if len(result['original_content']) > 200 else result['original_content']
        })

    search_time = round((time.time() - start_time) * 1000, 2)
    return render_template('index.html',
                           results=enriched_results,
                           query=query,
                           search_time=search_time)

@app.route('/open_document/<filename>')
def open_document(filename):
    try:
        return send_from_directory(docs_path, filename, as_attachment=True)
    except FileNotFoundError:
        return "Archivo no encontrado", 404

if __name__ == '__main__':
    app.run(debug=True)
