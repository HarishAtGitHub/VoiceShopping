from flask import Flask, jsonify
from flask import abort
from flask import request

from core.understander.business.shopping.analyzer import Analyzer as ShoppingAnalyzer
from core.understander.companies.walmart.analyzer import Analyzer as WalmartAnalyzer
from core.understander.companies.walmart.searcher import Searcher as WalmartSearcher
from core.commons.exceptions import UnableToUnderstandException
import properties.core.understander.business.shopping.messages as msg
from core.understander.companies.walmart.api.facet import get_facets

shopping_analyzer = ShoppingAnalyzer()
walmart_shopping_analyzer = WalmartAnalyzer()

from core.understander.business.general.question_analyzer import Analyzer

generic_analyzer = Analyzer()
app = Flask(__name__)

API_PATH = '/ml/api/'
API_VERSION = 'v1.0'
API_PREFIX = API_PATH + API_VERSION

WALMART_API_PATH = '/walmart/api/'
WALMART_API_PREFIX = WALMART_API_PATH + API_VERSION

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
    try:
        analyzed_form = shopping_analyzer.analyze(text)
    except UnableToUnderstandException as utue:
        return jsonify({'text' : str(utue)}), 400
    except:
        return jsonify({'text': msg.UNABLE_TO_UNDERSTAND}), 503
    return jsonify(analyzed_form)

@app.route(API_PATH + API_VERSION + '/shopping/understander/walmart', methods=['POST'])
def understand_shopping_walmart():
    text = request.json['text']
    try:
        analyzed_form = walmart_shopping_analyzer.analyze(text)
    except UnableToUnderstandException as utue:
        return jsonify({'text' : str(utue)}), 400
    except:
        return jsonify({'text': msg.UNABLE_TO_UNDERSTAND}), 503

    return jsonify(analyzed_form)

@app.route(API_PREFIX + '/shopping/search/walmart', methods=['POST'])
def shopping_search_walmart():
    text = request.json['text']
    try:
        analyzed_form = walmart_shopping_analyzer.analyze(text)
    except UnableToUnderstandException as utue:
        return jsonify({'text' : str(utue)}), 400
    except:
        return jsonify({'text': msg.UNABLE_TO_UNDERSTAND}), 503

    search_results = WalmartSearcher.fetch_results(analyzed_form)
    if search_results:
        return jsonify(search_results)
    else:
        return jsonify({'text': msg.UNABLE_TO_UNDERSTAND}), 503

@app.route(WALMART_API_PREFIX + '/facets', methods=['POST'])
def walmart_get_facets():
    try:
        try:
            product = request.json['product']
        except KeyError as ke:
            return jsonify({'text': msg.MANDATORY_PRODUCT_FIELD}), 400
        facets = get_facets(product)
        if facets:
            return jsonify(facets)
        else:
            return jsonify({'text': msg.NO_FACETS_FOUND}), 404
    except:
        return jsonify({'text': msg.FINAL_EXCEPTION}), 503

@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file(path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
