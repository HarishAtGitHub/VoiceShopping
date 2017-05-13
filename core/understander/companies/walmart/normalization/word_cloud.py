from core.commons.util import deserialize
import os
from constants import ROOT_DIR
class WordCloud():

    @classmethod
    def get_static_word_cloud(cls):
        return deserialize(os.path.join(ROOT_DIR, os.path.dirname(__file__), "static_cloud.ser"))