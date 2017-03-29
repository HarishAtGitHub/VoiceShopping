from core.commons.util import *
import re

class KnowledgeBasedAnalyzer:
    @time_usage
    def __init__(self):
        import os
        dirname, filename = os.path.split(os.path.abspath(__file__))

        # spacy ner tagger
        import spacy
        self.ner_spacy = spacy.load('en')

        # wordnet lemmatizer
        from nltk.stem.wordnet import WordNetLemmatizer
        self.lemmatizer = WordNetLemmatizer()

        #load color and currency extract
        # TODO: put file locations in a common file
        currency_file = dirname + '/../../../../../data/extract/currency.ser'
        with open(currency_file, 'rb') as storage_file:
            import pickle
            self.currency_extract = pickle.load(storage_file)

        currency_file = dirname + '/../../../../../data/extract/color.ser'
        with open(currency_file, 'rb') as storage_file:
            import pickle
            self.color_extract = pickle.load(storage_file)

        # set common materials
        self.material_set = set()

        # complement lemmatizer at corner cases
        self.complementary_lemmatizer = {'wooden': 'wood'}

        self.lemmatized_tokens = []
        self.tagged_output = {}

    def add_additional_materials(self, materials = []):
        # added an empty list in signature to indicate the param type.
        # union list with existing set of common materials to allow
        # for addition of company specific materials
        self.material_set |= set(materials)

    @time_usage
    def analyze(self,
                text,
                person=False,
                date=False,
                number=False,
                currency=False,
                subject=False,
                action=False,
                color=False,
                math_comparisons=False
                ):
        segments = text.split('and')
        op = []
        for segment in segments:
            op.append(
                self.analyze_segments(segment,
                    person=person,
                    date=date,
                    number=number,
                    currency=currency,
                    subject=subject,
                    action=action,
                    color=color,
                    math_comparisons=math_comparisons
                                      ))
            self.tagged_output = {}

        return op

    @time_usage
    def analyze_segments(self,
                         text,
                         person=False,
                         date=False,
                         number=False,
                         currency=False,
                         subject=False,
                         action=False,
                         color=False,
                         material=False,
                         math_comparisons=False
                         ):
        self.text = text
        self.massage(text) \
            .tokenize() \
            .tag_pos() \
            .lemmatize() \
            .tag_universal(person, date, number, currency, subject, action,
                           color, material, math_comparisons)
        self.tagged_output['INPUT_TEXT'] = self.text
        return self.tagged_output

    def massage(self, text):
        # correct any possible problems in string
        # 1. convert to lower case
        self.text = text.lower()

        # 2. strip space before and after the string
        self.text = self.text.strip()

        # 3. remove more than one space in between words (or else it is considered as a separate token
        # which is irrelevant)
        self.text = re.sub('\s\s+', ' ', self.text)
        return self

    @time_usage
    def tokenize(self):
        from nltk import word_tokenize
        self.tokens = word_tokenize(self.text)
        return self

    @time_usage
    def tag_pos(self):
        from core.stanford.util.nlp import NLP

        self.pos_tagged_tokens = NLP.tag_pos(self.text)
        #print(self.pos_tagged_tokens)
        return self

    @time_usage
    def lemmatize(self):
        self.lemmatized_tokens = [self.lemmatizer.lemmatize(token[0], pos=self.__find_tag_letter(token[1])) for token in
                                  self.pos_tagged_tokens]
        # apply the complementary lemmatizer to address corner cases
        for token in self.lemmatized_tokens:
            lemmatized_token = self.complementary_lemmatizer.get(token)
            if lemmatized_token:
                self.lemmatized_tokens[self.lemmatized_tokens.index(token)] = lemmatized_token
        return self

    @time_usage
    def __find_tag_letter(self, token):
        # ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'
        JJ, RB, NN, VB = 'a', 'r', 'n', 'v'  # did not find a match for ADJ_SAT
        # REFER: https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
        VBD = VBG = VBN = VBP = VBZ = VB
        try:
            letter = eval(token)
        except NameError as ne:
            letter = 'n'  # default as per wordnet lemmatize function TODO: find some other way
        return letter

    @time_usage
    def tag_universal(self, person, date, number, currency, subject, action,
                      color, material, math_comparisons):
        from core.understander.generic.analyzer.knowledge.tagger.custom_tagger import CustomTagger
        tagger = CustomTagger(text=self.text,
                              lemmatized_tokens=self.lemmatized_tokens,
                              unlemmatized_tokens=self.tokens,
                              pos_tagged_tokens = self.pos_tagged_tokens,
                              spacy_ner=self.ner_spacy,
                              currency_extract=self.currency_extract,
                              color_extract=self.color_extract,
                              material_set=self.material_set)
        # TODO: FIXME as the verb and person names got mixed up
        # do not change order
        # Fix it later properly
        if color: self.tagged_output['COLOR'] = tagger.tag_color()
        if material: self.tagged_output['MATERIAL'] = tagger.tag_material()
        if person: self.tagged_output['PERSON'] = tagger.tag_person()
        #self.tagged_output['TYPE'] = tagger.tag_type()
        # removing date tagging as spacy loading takes a lot of time
        # https://github.com/explosion/spaCy/issues/219
        if date: self.tagged_output['DATE'] = tagger.tag_date()
        if number: self.tagged_output['NUMBER'] = tagger.tag_numbers()
        if currency: self.tagged_output['CURRENCY'] = tagger.tag_currency()
        if subject: self.tagged_output['SUBJECT'] = tagger.tag_subject()
        if action: self.tagged_output['ACTION'] = tagger.tag_action()
        if math_comparisons: self.tagged_output['RELATION'] = tagger.tag_math_inequality()
        return self