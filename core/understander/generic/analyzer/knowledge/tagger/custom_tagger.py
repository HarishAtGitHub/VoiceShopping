class CustomTagger:
    def __init__(self, unlemmatized_tokens, lemmatized_tokens, pos_tagged_tokens, stanford_ner, spacy_ner):
        self.lemmatized_tokens = lemmatized_tokens
        self.unlemmatized_tokens = unlemmatized_tokens
        self.pos_tagged_tokens = pos_tagged_tokens
        import os
        dirname, _ = os.path.split(os.path.abspath(__file__))
        # TODO: put file locations in a common file
        currency_file = dirname + '/../../../../../../data/extract/currency.ser'
        with open(currency_file, 'rb') as storage_file:
            import pickle
            self.currency_extract = pickle.load(storage_file)
        self.stanford_ner = stanford_ner
        self.spacy_ner = spacy_ner
        self.NOUN_TAGS = set(['NNS', 'NN', 'NNP', 'NNPS'])
        self.VERB_TAGS = set(['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'])

    def tag_person(self):
        # fix to have persons at different locations
        ner_tagged_tokens = self.stanford_ner.tag(self.unlemmatized_tokens)
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

    def tag_numbers(self):
        pos_tagged_tokens = self.pos_tagged_tokens
        nums = list()
        start = False
        NUMBER_TAGS = set(['CD'])

        for index, token in enumerate(pos_tagged_tokens):
            if ((token[1] in NUMBER_TAGS)
                and not self.is_in_dates(token[0])):
                if nums:
                    if start:
                        nums[len(nums) - 1] = nums[len(nums) - 1] + ' ' + token[0]
                        if self.is_in_dates(nums[len(nums) - 1]):
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
                and not self.is_in_names(token[0])
                and not self.is_in_dates(token[0])
                and not self.is_in_nums(token[0])
                and not self.is_in_currencies(token[0])):
                if nouns:
                    if start:
                        nouns[len(nouns) - 1] = nouns[len(nouns) - 1] + ' ' + token[0]
                        if self.is_in_dates(nouns[len(nouns) - 1]):
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

    def tag_action(self):
        pos_lemmatized_tagged_tokens = self.pos_tagged_tokens
        verbs = list()
        start = False

        USELESS_VERBS = set(['is', 'was', 'are', 'were',  'has', 'had', 'have', 'does', 'do', 'doing', 'be'])
        for token in pos_lemmatized_tagged_tokens:
            if (token[1] in self.VERB_TAGS and
                    not (self.is_in_names(token[0])) and
                    not (token[0] in USELESS_VERBS) and
                    not (self.is_in_nouns(token[0]))):
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

    def is_in_nums(self, segment):
        for num in self.nums:
            if segment in num.split(' '):
                return True

    def is_in_names(self, segment):
        # used because some names were misunderstood as verbs like sylvester in douglas sylvester(not sure why)
        for person in self.persons:
            if segment in person.split(' '):
                return True

    def is_in_dates(self, segment):
        # used because some names were misunderstood as verbs like sylvester in douglas sylvester(not sure why)
        #return segment in self.dates
        for date in self.dates:
            if segment in date.split(' '):
                return True

    # used especially not to repeat the gerunds
    def is_in_nouns(self, segment):
        # used because some names were misunderstood as verbs like sylvester in douglas sylvester(not sure why)
        #return segment in self.dates
        for noun in self.nouns:
            if segment in noun.split(' '):
                return True


    def is_in_currencies(self, segment):
        # used because some names were misunderstood as verbs like sylvester in douglas sylvester(not sure why)
        for currency in self.currencies:
            if segment in currency.split(' '):
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



