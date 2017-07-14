import os
import itertools
from nltk.corpus import wordnet as w
from nltk.corpus.reader.wordnet import Synset

class WordCloud():

    @classmethod
    def get_static_word_cloud(cls):
        from constants import ROOT_DIR
        from core.commons.util import deserialize
        return deserialize(os.path.join(ROOT_DIR, os.path.dirname(__file__), "static_cloud.ser"))

    @classmethod
    def get_dynamic_word_cloud(cls, product: str):
        from core.understander.companies.walmart.api.facet import get_facets
        facets_and_values = get_facets(item=product)
        meanings_facet_map = {}
        if facets_and_values:
            attributes = facets_and_values.keys()
            from core.understander.companies.walmart.normalization.word_cloud import WordCloud
            facet_meanings = {}
            for attribute in attributes:
                facet_meanings[attribute] = WordCloud.get_word_cloud_from_word(attribute)
            # FIXME: the same logic below is alos in static cloud
            for facet, meanings in facet_meanings.items():
                if meanings:
                    for meaning in meanings:
                        meanings_facet_map[meaning] = facet
                else:
                    # case where there are no meanings for some strange reason
                    # map to itself
                    meanings_facet_map[facet] = facet

        if meanings_facet_map:
            return meanings_facet_map
        else:
            return None

    @classmethod
    def get_word_cloud_from_word_sense(cls, word_sense):
        # be careful while doing something in this function because this is  used in
        # a standalone file
        word_sense = w.synset(word_sense)
        syns = word_sense.lemma_names()
        hypernyms = list(itertools.chain(*[h.lemma_names() for h in word_sense.hypernyms()]))
        hyponyms = list(itertools.chain(*[h.lemma_names() for h in word_sense.hyponyms()]))
        word_cloud = syns + hyponyms + hypernyms
        return word_cloud

    '''
        to get word cloud give a human understandable word
    '''
    @classmethod
    def get_word_cloud_from_word(cls, word: str) -> list:
        word_synsets = w.synsets(word)
        meanings = []
        if word_synsets:
            for word_synset in word_synsets:
                meanings = meanings + cls.get_word_cloud_from_synset(word_synset)
            return meanings
        else:
            return None

    @classmethod
    def get_word_cloud_from_synset(cls, word_synset: Synset):
        return cls.get_word_cloud_from_word_sense(word_synset.name())