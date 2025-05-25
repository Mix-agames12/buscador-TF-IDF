from flask import Flask, request, render_template, send_from_directory
from utils.tfidf import preprocess_documents, search_query, get_word_count_in_document
import time
import os

app = Flask(__name__)
docs_path = 'documents/'  # Path to the directory containing documents
documents, tfidf_matrix, feature_names = preprocess_documents(docs_path)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search')
def search():
    start_time = time.time()
    query = request.args.get('q')
    
    if not query:
        return render_template('index.html', results=[], search_time=0)
    
    # Realizar búsqueda
    results = search_query(query, documents, tfidf_matrix, feature_names)
    
    # Enriquecer resultados con conteo de palabras
    enriched_results = []
    for result in results:
        word_count = get_word_count_in_document(query, result['content'])
        enriched_results.append({
            'filename': result['filename'],
            'score': result['score'],
            'word_count': word_count,
            'content': result['content'][:200] + '...' if len(result['content']) > 200 else result['content']
        })
    
    # Calcular tiempo de búsqueda
    search_time = round((time.time() - start_time) * 1000, 2)  # en milisegundos
    
    return render_template('index.html', 
                         results=enriched_results, 
                         query=query, 
                         search_time=search_time)

@app.route('/open_document/<filename>')
def open_document(filename):
    # Endpoint para abrir/descargar documentos
    try:
        return send_from_directory(docs_path, filename, as_attachment=True)
    except FileNotFoundError:
        return "Archivo no encontrado", 404

if __name__ == '__main__':
    app.run(debug=True)