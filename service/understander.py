from flask import Flask, jsonify
from flask import abort
from flask import request

from core.understander.business.shopping.analyzer import Analyzer

shopping_analyzer = Analyzer()

from core.understander.business.general.question_analyzer import Analyzer

generic_analyzer = Analyzer()
app = Flask(__name__)

API_PATH = '/ml/api/'
API_VERSION = 'v1.0'

@app.route(API_PATH + API_VERSION + '/understand', methods=['GET'])
def get_status():
    return "Hello ! Answer service is Up. Do a POST request to same URL with body in the  json form {'text':'<text>'}"

@app.route(API_PATH + API_VERSION + '/general/understander', methods=['POST'])
def understand():
    text = request.json['text']
    analyzed_form = generic_analyzer.analyze(text)
    return jsonify(analyzed_form)

@app.route(API_PATH + API_VERSION + '/shopping/understander', methods=['POST'])
def understand_shopping():
    text = request.json['text']
    analyzed_form = shopping_analyzer.analyze(text)
    return jsonify(analyzed_form)

@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file(path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)