from flask import Flask, jsonify
from flask import abort
from flask import request

app = Flask(__name__)

API_PATH = '/ml/api/'
API_VERSION = 'v1.0'

@app.route(API_PATH + API_VERSION + '/understand', methods=['GET'])
def get_status():
    return "Hello ! Answer service is Up. Do a POST request to same URL with body in the  json form {'text':'<text>'}"

@app.route(API_PATH + API_VERSION + '/understand', methods=['POST'])
def understand():
    try:
        text = request.json['text']
        if 'query_type' in request.json:
            query_type = request.json['query_type']
        else:
            query_type = None
        return jsonify(get_query(text, query_type))
    except KeyError as ke:
        abort(417)

def get_query(text, query_type):
    from core.understander.generic import generic_question
    result = generic_question.get_query_from_sentance(text, query_type)
    return result

@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file(path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)