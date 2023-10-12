from flask import Flask, request, jsonify
from flask_cors import CORS
from main import search
from indexation_module import get_file_contents, find_weights_of_query_elements
from logic_strategy import tokenize_query

app = Flask(__name__)
CORS(app)


@app.route('/docs', methods=['POST'])
def docs():
    query = request.json["query"]
    docsList = search(query)
    response = []
    for doc_name in docsList:
        full_text = get_file_contents(doc_name)
        top_words = []
        for key, value in find_weights_of_query_elements(tokenize_query(query), full_text).items():
            top_words.append({ "word": key, "weightCoef": value })
        document_info = {
            "name": doc_name,
            "topWords": top_words,
            "snippet": full_text[:300]
        }
        response.append(document_info)
    return jsonify(response)


@app.route('/text', methods=['POST'])
def text():
    doc_name = request.json["docName"]
    return jsonify(get_file_contents(doc_name))


@app.route('/metrics', methods=['GET'])
def metrics():
    return jsonify({
        "recall": 0.8461,
        "precision": 0.7857,
        "accuracy": 0.8936,
        "error": 0.1063,
        "fMeasure": 0.8148
    })


if __name__ == '__main__':
    app.run()