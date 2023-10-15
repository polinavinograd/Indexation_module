from flask import Flask, request, jsonify
from flask_cors import CORS
from main import search, get_doc_text_by_name, get_metrics

app = Flask(__name__)
CORS(app)

@app.route('/docs', methods=['POST'])
def docs():
    SEARCH_RESULTS = search(request.json["query"])
    RESPONSE = list(map(lambda search_result: {
        "name": search_result.document.name,
        "topWords": search_result.top_words,
        "relevance": search_result.relevance,
        "date": f'{search_result.document.creation_datetime.day}-{search_result.document.creation_datetime.month}-{search_result.document.creation_datetime.year}',
        "snippet": search_result.document.text[:300]
    }, SEARCH_RESULTS))
    return jsonify(RESPONSE)

@app.route('/text', methods=['POST'])
def text():
    return jsonify(get_doc_text_by_name(request.json["docName"]))

@app.route('/metrics', methods=['GET'])
def metrics():
    return jsonify(get_metrics())

if __name__ == '__main__':
    app.run()