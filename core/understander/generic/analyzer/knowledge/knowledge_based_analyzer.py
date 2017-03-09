import time

def time_usage(func):
    def wrapper(*args, **kwargs):
        beg_ts = time.time()
        retval = func(*args, **kwargs)
        end_ts = time.time()
        print(func.__name__)
        print("elapsed time: %f" % (end_ts - beg_ts))
        return retval
    return wrapper

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

        self.tagged_output = {}

    @time_usage
    def analyze(self,
                text,
                person=False,
                date=False,
                number=False,
                currency=False,
                subject=False,
                action=False,
                color=False
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
                    color=color
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
                         color=False
                         ):
        self.text = text
        self.lowercase(text) \
            .tokenize() \
            .tag_pos() \
            .lemmatize() \
            .tag_universal(person, date, number, currency, subject, action, color)
        self.tagged_output['INPUT_TEXT'] = self.text
        return self.tagged_output


    def lowercase(self, text):
        # to mimic text that comes out of voice to text conversion
        self.text = text.lower()
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
        print(self.pos_tagged_tokens)
        return self

    @time_usage
    def lemmatize(self):
        '''
        self.lemmatized_tokens = [self.lemmatizer.lemmatize(token[0], pos=self.__find_tag_letter(token[1])) for token in
                                  self.pos_tagged_tokens]
        '''
        self.lemmatized_tokens = []
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
    def tag_universal(self,
                      person,
                      date,
                      number,
                      currency,
                      subject,
                      action,
                      color
                      ):
        from core.understander.generic.analyzer.knowledge.tagger.custom_tagger import CustomTagger
        tagger = CustomTagger(text=self.text,
                              lemmatized_tokens=self.lemmatized_tokens,
                              unlemmatized_tokens=self.tokens,
                              pos_tagged_tokens = self.pos_tagged_tokens,
                              spacy_ner=self.ner_spacy,
                              currency_extract=self.currency_extract,
                              color_extract=self.color_extract)
        # TODO: FIXME as the verb and person names got mixed up
        # do not change order
        # Fix it later properly
        if color: self.tagged_output['COLOR'] = tagger.tag_color()
        if person: self.tagged_output['PERSON'] = tagger.tag_person()
        #self.tagged_output['TYPE'] = tagger.tag_type()
        # removing date tagging as spacy loading takes a lot of time
        # https://github.com/explosion/spaCy/issues/219
        if date: self.tagged_output['DATE'] = tagger.tag_date()
        if number: self.tagged_output['NUMBER'] = tagger.tag_numbers()
        if currency: self.tagged_output['CURRENCY'] = tagger.tag_currency()
        if subject: self.tagged_output['SUBJECT'] = tagger.tag_subject()
        if action: self.tagged_output['ACTION'] = tagger.tag_action()
        return self