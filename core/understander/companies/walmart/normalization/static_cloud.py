known_facets = {
    'height' : ['height.n.01', 'stature.n.02', 'altitude.n.01'],
    'length' : ['length.n.01'],
    'width' : ['width.n.01'],
    'weight' : ['weight.n.01'],
    'price' : ['monetary_value.n.01', 'price.n.02', 'price.n.04'],
    'retailer' : ['retailer.n.01'],
    'brand' : ['trade_name.n.01'],
    'color': ['color.n.01'],
    'rating' : ['evaluation.n.01']
}

from nltk.corpus import wordnet as w
import itertools

'''def get_word_cloud(word_sense):
    word_sense = w.synset(word_sense)
    syns = word_sense.lemma_names()
    hypernyms = list(itertools.chain(*[h.lemma_names() for h in word_sense.hypernyms()]))
    hyponyms = list(itertools.chain(*[h.lemma_names() for h in word_sense.hyponyms()]))
    word_cloud = syns + hyponyms + hypernyms
    return word_cloud
'''

def get_facet_meanings():
    from core.understander.companies.walmart.normalization.word_cloud import WordCloud
    facets_meanings = {}
    for facet, word_senses in known_facets.items():
        word_cloud = []
        for word_sense in word_senses:
            # be careful while doing something ins wordcloud because this is a standalone file
            # and it is using a module from the project
            word_cloud = word_cloud + WordCloud.get_word_cloud_from_word_sense(word_sense)

        facets_meanings[facet] = word_cloud
    return facets_meanings

def correct_ambiguity(facet_meanings):
    # 1. shortness appears in height and length
    # 2. dimension appears in width and height and length
    # 3. brand has value a 'name' which is very general
    # 4. physical_property is in both length and weight
    # so remove all ambiguous things
    facet_meanings['height'].remove('shortness')
    facet_meanings['length'].remove('shortness')
    facet_meanings['width'].remove('dimension')
    facet_meanings['height'].remove('dimension')
    facet_meanings['length'].remove('dimension')
    facet_meanings['brand'].remove('name')
    facet_meanings['weight'].remove('physical_property')
    facet_meanings['length'].remove('physical_property')
    facet_meanings['price'].remove('assessment')
    facet_meanings['rating'].remove('assessment')
    return facet_meanings

def map_meanings_to_facet():
    facet_meanings = get_facet_meanings()
    facet_meanings = correct_ambiguity(facet_meanings)
    meanings_facet_map = {}
    for facet, meanings in facet_meanings.items():
        for meaning in meanings:
            meanings_facet_map[meaning] = facet

    return meanings_facet_map

if __name__ == '__main__':
    from core.commons.util import *
    import os

    meanings_facet_map = map_meanings_to_facet()
    file_location = os.path.join(os.path.dirname(__file__), "static_cloud.ser")
    serialize(meanings_facet_map, file_location)

    # check if what we put in is what we got
    #import unittest

    #test = unittest.TestCase('__init__')
    #obj = deserialize(file_location)
    #test.assertDictEqual.__self__.maxDiff = None
    #test.assertDictEqual(meanings_facet_map, obj)
