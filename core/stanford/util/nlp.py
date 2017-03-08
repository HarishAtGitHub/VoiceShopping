import requests
from properties.core import STANFORD_NLP_POS_TAG_ENDPOINT, STANFORD_NLP_NER_TAG_ENDPOINT

class NLP():
    @classmethod
    def tag_pos(cls, text):
        params = {'text' : text}
        result = requests.get(STANFORD_NLP_POS_TAG_ENDPOINT, params=params)
        return [tuple(i.split('_')) for i in result.text.strip().split(' ')]

    @classmethod
    def tag_ner(cls, text):
        params = {'text': text}
        result = requests.get(STANFORD_NLP_NER_TAG_ENDPOINT, params=params)
        return [tuple(i.split('/')) for i in result.text.strip().split(' ')]