import os
import itertools
from nltk.corpus import wordnet as w

class WordCloud():

    @classmethod
    def get_static_word_cloud(cls):
        from constants import ROOT_DIR
        from core.commons.util import deserialize
        return deserialize(os.path.join(ROOT_DIR, os.path.dirname(__file__), "static_cloud.ser"))

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