from flask import Flask, jsonify
from flask import abort
from flask import request

from core.understander.business.shopping.analyzer import Analyzer as ShoppingAnalyzer
from core.understander.companies.walmart.analyzer import Analyzer as WalmartAnalyzer

shopping_analyzer = ShoppingAnalyzer()
walmart_shopping_analyzer = WalmartAnalyzer()

from core.understander.business.general.question_analyzer import Analyzer

generic_analyzer = Analyzer()
app = Flask(__name__)

API_PATH = '/ml/api/'
API_VERSION = 'v1.0'

@app.route(API_PATH + API_VERSION + '/understander', methods=['GET'])
def get_status():
    return app.send_static_file('guide.html')


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

@app.route(API_PATH + API_VERSION + '/shopping/understander/walmart', methods=['POST'])
def understand_shopping_walmart():
    text = request.json['text']
    analyzed_form = walmart_shopping_analyzer.analyze(text)
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