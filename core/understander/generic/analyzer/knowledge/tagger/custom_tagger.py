from core.commons.util import *

class CustomTagger:
    def __init__(self, text, unlemmatized_tokens, lemmatized_tokens,
                 pos_tagged_tokens, spacy_ner, color_extract, currency_extract,
                 material_set):
        self.text = text
        self.lemmatized_tokens = lemmatized_tokens
        self.unlemmatized_tokens = unlemmatized_tokens
        self.pos_tagged_tokens = pos_tagged_tokens
        import os
        dirname, _ = os.path.split(os.path.abspath(__file__))

        self.color_extract = color_extract
        self.material_set = material_set
        self.material_map = {m.lower(): m for m in self.material_set}
        self.currency_extract = currency_extract


        self.spacy_ner = spacy_ner
        self.NOUN_TAGS = set(['NNS', 'NN', 'NNP', 'NNPS'])
        self.VERB_TAGS = set(['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'])
        self.persons = []
        self.dates = []
        self.nums = []
        self.currencies = []
        self.colors = []
        self.materials = []
        self.math_comparisons = []

    @time_usage
    def tag_person(self):
        # fix to have persons at different locations
        from core.stanford.util.nlp import NLP
        ner_tagged_tokens = NLP.tag_ner(self.text)
        persons = list()
        start = False
        for token in ner_tagged_tokens:
            if (token[1] == 'PERSON'):
                if persons:
                    if start:
                        persons[len(persons) - 1] = persons[len(persons) - 1] + ' ' + token[0]
                    else:
                        start = True
                        persons.append(token[0])
                else:
                    start = True
                    persons.append(token[0])
            else:
                start = False
        self.persons = persons # for it to be used in other places
        return persons

    @time_usage
    def tag_math_inequality(self):
        entities = []
        terms_less = ['less than', 'lesser than', 'not more than', 'below', 'under']
        terms_more = ['more than', 'greater than', 'above', 'over']
        terms_equal = ['equal to', 'about']
        relations = {
                     '<' : terms_less,
                     '>' : terms_more,
                     '=' : terms_equal
                     }
        for relation in relations.keys():
            for term in relations[relation]:
                if term in self.text:
                    entities.append(relation)

        self.math_comparisons = entities
        return self.math_comparisons

    @time_usage
    def tag_numbers(self):
        pos_tagged_tokens = self.pos_tagged_tokens
        nums = list()
        start = False
        NUMBER_TAGS = set(['CD'])

        for index, token in enumerate(pos_tagged_tokens):
            if ((token[1] in NUMBER_TAGS)
                and not self.is_segment_already_tagged(token[0], ['dates'])):
                if nums:
                    if start:
                        nums[len(nums) - 1] = nums[len(nums) - 1] + ' ' + token[0]
                        if self.is_segment_already_tagged(nums[len(nums) - 1], ['dates']):
                            nums.pop()
                    else:
                        start = True
                        nums.append(token[0])
                else:
                    start = True
                    nums.append(token[0])
            else:
                start = False
        self.nums = nums  # for it to be used in other places
        return nums

    @time_usage
    def tag_color(self):
        # assumption : colors can span 1,2,3 words together
        colors = []
        # len 3
        for i in zip(self.unlemmatized_tokens,
                     self.unlemmatized_tokens[1:],
                     self.unlemmatized_tokens[2:]):
            segment = ' '.join(list(i))
            if segment in self.color_extract:
                colors.append(segment)

        # len 3
        for i in zip(self.unlemmatized_tokens,
                     self.unlemmatized_tokens[1:]):
            segment = ' '.join(list(i))
            if segment in self.color_extract:
                colors.append(segment)

        # len 3
        for segment in self.unlemmatized_tokens:
            if segment in self.color_extract:
                colors.append(segment)
        self.colors = colors
        return colors

    @time_usage
    def tag_material(self):
        # assumption : materials can span 1 or 2 words together
        token_list = self.lemmatized_tokens[:]
        # len 2
        for i in zip(token_list,
                     token_list[1:]):
            segment = ' '.join(list(i)).lower()
            if segment in self.material_map:
                self.materials.append(self.material_map[segment])
                # remove the processed tokens to guard against 'resin' being
                # added to materials if 'resin wicker' is already found
                for token in i:
                    token_list.remove(token)
        # len 1
        for token in token_list:
            token_lc = token.lower()
            if token_lc in self.material_map and token_lc not in self.materials:
                self.materials.append(self.material_map[token_lc])
        return self.materials

    @time_usage
    def tag_subject(self, tokens = None):
        # fix to have persons at different locations
        #ner_tagged_tokens = self.stanford_ner.tag(tokens if tokens else self.tokens)
        import nltk
        pos_tagged_tokens = self.pos_tagged_tokens
        nouns = list()
        start = False
        NUMBER_TAGS = set(['CD'])

        GERUND_TAG = 'VBG'
        for index, token in enumerate(pos_tagged_tokens):
            if ((token[1] in self.NOUN_TAGS or token[1] in NUMBER_TAGS)
                and not self.is_segment_already_tagged(token[0], ['currencies',
                                                                  'persons',
                                                                  'dates',
                                                                  'nums',
                                                                  'materials',
                                                                  'colors'])):
                if nouns:
                    if start:
                        nouns[len(nouns) - 1] = nouns[len(nouns) - 1] + ' ' + token[0]
                        if self.is_segment_already_tagged(nouns[len(nouns) - 1], ['dates']):
                            nouns.pop()

                    else:
                        start = True
                        nouns.append(token[0])
                else:
                    start = True
                    nouns.append(token[0])
                # special case for verbs preceding nouns like sporting events - essentially gerunds
                if (index > 1 and pos_tagged_tokens[index - 1][1] == GERUND_TAG
                    and pos_tagged_tokens[index - 2][1] not in self.VERB_TAGS):
                    nouns[len(nouns) - 1] = pos_tagged_tokens[index - 1][0] + ' ' + nouns[len(nouns) - 1]
            else:
                start = False
        self.nouns = nouns # for it to be used in other places
        return nouns

    def tag_currency(self):
        self.currencies = []
        for token in self.unlemmatized_tokens:
            if token in self.currency_extract:
                self.currencies.append(token)
        return self.currencies

    @time_usage
    def tag_date(self):
        doc = self.spacy_ner(' '.join(self.unlemmatized_tokens))
        dates = []
        for ent in doc.ents:
            # print(ent.label_, ent.text)
            if (ent.label_ == 'DATE'):
                dates.append(ent.text)
        self.dates = dates
        # FIXME train spacy with the following
        # for now put the terms directly
        date_left_out_tokens = ['soon', 'now', 'near future']
        text = ' '.join(self.unlemmatized_tokens)
        for token in date_left_out_tokens:
            if token in text:
                self.dates.append(token)
        return dates

    @time_usage
    def tag_action(self):
        pos_lemmatized_tagged_tokens = self.pos_tagged_tokens
        verbs = list()
        start = False

        USELESS_VERBS = set(['is', 'was', 'are', 'were',  'has', 'had', 'have', 'does', 'do', 'doing', 'be'])
        for token in pos_lemmatized_tagged_tokens:
            if (token[1] in self.VERB_TAGS and
                    not (self.is_segment_already_tagged(token[0], ['persons', 'nouns'])) and
                    not (token[0] in USELESS_VERBS)):
                if verbs:
                    if start:
                        verbs[len(verbs) - 1] = verbs[len(verbs) - 1] + ' ' + token[0]
                    else:
                        start = True
                        verbs.append(token[0])
                else:
                    start = True
                    verbs.append(token[0])

            else:
                start = False
        return verbs

    def is_segment_already_tagged(self, segment, tags):
        for tag in tags:
            for item in self.__dict__[tag]:
                if segment.lower() in item.lower().split(' '):
                    return True

    def tag_type(self):
        supported_solid_question_types = ['what', 'who', 'when']
        supported_boolean_question_types = ['can', 'will', 'shall', 'would', 'could']
        supported_qty_question_types = ['how many', 'how much']
        tokens = self.unlemmatized_tokens
        if tokens[0] in supported_solid_question_types:
            return tokens[0]
        elif tokens[0] + ' ' + tokens[1] in supported_qty_question_types:
            return 'quantity'
        elif tokens[0] in supported_boolean_question_types:
            return 'boolean'
        else:
            return 'other'



