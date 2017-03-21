from core.commons.text2num import text2num, NumberException

class Analyzer:
    # instantiate analyzer only once and reuse it or else each time it takes time
    def __init__(self):
        from core.understander.generic.analyzer.grammar.grammar_based_analyzer import GrammarBasedAnalyzer
        self.grammar_analyzer = GrammarBasedAnalyzer()
        from core.understander.generic.analyzer.knowledge.knowledge_based_analyzer import KnowledgeBasedAnalyzer
        self.knowledge_analyzer = KnowledgeBasedAnalyzer()

    def analyze(self, text):
        self.text = text.lower()

        self.tokens = self.text.split(' ')
        self.start_index = 0
        self.running_index = 0

        # get product name
        op = {}
        product = self.get_main_product()
        if product:
            op['PRODUCT'] = product
        else:
            return 'Sorry, We were unable to figure the product you are searching for'

        # get product attributes
        op['attributes'] = []
        self.running_index = self.start_index
        current = ''
        while True:
            if self.start_index < len(self.tokens) - 1:
                for index, token in enumerate(self.tokens[self.start_index:]):
                    self.running_index = self.start_index + index
                    current = current + ' ' + token
                    result, analyzed_form = self.get_key_value_pair(current)
                    if result:
                        op['attributes'].extend(result)
                        self.start_index = self.start_index + index
                        break
                else:
                    break
                # before discarding the sentence see if you can make sense of it
                res = self.get_possible_meaning(text, analyzed_form)
                if res:
                    op['attributes'].extend(res)
                # discard the sentence
                current = ''
                continue
            else:
                break
        # get global attributes to handle cases like get green  chairs
        op['attributes'] = op['attributes'] + self.get_universal_attributes(text)
        # return product details
        return op

    def get_key_value_pair(self, text):
        analyzed_form = self.knowledge_analyzer.analyze_segments(
            text,
            person=True,
            number=True,
            currency=True,
            subject=True,
            action=True,
            math_comparisons=True)

        if len(analyzed_form['SUBJECT']) > 1 or self.running_index == len(self.tokens) - 1:
            op = []

            res = {}
            res['modifiers'] = {}
            res['key'] = ''
            res['value'] = ''
            # see the portion before subject and see if you can get possible meaning before discarding
            text_trimmed =  text.lstrip().rstrip()
            if not text_trimmed.startswith(analyzed_form['SUBJECT'][0]):
                # then it means there is a part that is before subject
                # but in this algo we take a stand that we always take value after the key

                segments = text_trimmed.split(analyzed_form['SUBJECT'][0], 1)
                pre_subject_segment = segments[0]
                actual_segment = analyzed_form['SUBJECT'][0] + segments[1]
                analyzed_form_pre = self.get_analyzed_form(pre_subject_segment)
                meanings = self.get_possible_meaning(text, analyzed_form_pre)
                if meanings:
                    op.extend(meanings)

                # this is reset to new one based on the segment after the subject
                analyzed_form = self.get_analyzed_form(actual_segment)

            # analyze segment starting from subject till the next subject
            if analyzed_form['NUMBER']:
                res['key'] = analyzed_form['SUBJECT'][0]
                try:
                    res['value'] = int(text2num(analyzed_form['NUMBER'][0]))
                except NumberException as ne:
                    try:
                        res['value'] = int(analyzed_form['NUMBER'][0])
                    except ValueError as ve:
                        res['value'] = analyzed_form['NUMBER'][0]
            if analyzed_form['CURRENCY']:
                res['modifiers']['CURRENCY'] = analyzed_form['CURRENCY'][0]
            if analyzed_form['RELATION']:
                res['modifiers']['RELATION'] = analyzed_form['RELATION']
            if res['key']:
                op.append(res)

            if op:
                return op, analyzed_form
            else:
                return None, analyzed_form
        else:
            return None, analyzed_form

    def get_analyzed_form(self, text):
        return  self.knowledge_analyzer.analyze_segments(
            text,
            person=True,
            number=True,
            currency=True,
            subject=True,
            action=True,
            math_comparisons=True)

    def get_possible_meaning(self, text, analyzed_form):
        op = []
        '''
        if analyzed_form['SUBJECT']:
            if analyzed_form['SUBJECT'][0] in ['adult', 'child', 'teen', 'toddler', 'infant', 'kid']:
                res['key'] = 'lifestage'
                res['value'] = analyzed_form['SUBJECT'][0]
        '''


        # check money
        res = {}
        res['modifiers'] = {}
        res['key'] = ''
        res['value'] = []
        if analyzed_form['NUMBER'] and analyzed_form['CURRENCY']:
            money = self.get_money(text, analyzed_form)
            res['key'] = money['key']
            res['value'] = money['value']
            res['modifiers'] = money['modifiers']
        if res['key']:
            op.append(res)

        if op:
            return op
        else:
            return None

    def get_universal_attributes(self, text):
        analyzed_form = self.knowledge_analyzer.analyze_segments(
            text,
            number=True,
            currency=True,
            color=True)
        op = []

        # check color
        if analyzed_form['COLOR']:
            color ={'key' : 'color'}
            color['value'] = analyzed_form['COLOR']
            op.append(color)

        # check money
        if analyzed_form['NUMBER'] and analyzed_form['CURRENCY']:
            money = self.get_money(text, analyzed_form)
            op.append(money)

        # check life stage
        life_stages = ['adult', 'child', 'teen', 'toddler', 'infant', 'kid']
        res = {}
        res['modifiers'] = {}
        res['key'] = ''
        res['value'] = []
        for life_stage in life_stages:
            if life_stage in text:
                res['key'] = 'lifestage'
                res['value'].append(life_stage)
        if res['key']:
            op.append(res)

        if op:
            return op
        else:
            return None

    def get_money(self, text, analyzed_form):
        # this gives a possibility of money
        money = {'key': 'money'}
        money['value'] = ''
        money['modifiers'] = {}
        import itertools
        for m in itertools.product(analyzed_form['NUMBER'], analyzed_form['CURRENCY']):
            segment = ' '.join(m)
            if segment in text:
                try:
                    num = int(text2num(m[0]))
                except NumberException as ne:
                    try:
                        num = int(m[0])
                    except ValueError as ve:
                        num = m[0]
                money['value'] = {'number': num, 'unit': m[1]}

        if analyzed_form['RELATION']:
            money['modifiers']['RELATION'] = analyzed_form['RELATION']

        return money

    def get_main_product(self):
        current = ' '.join(self.tokens[:2])
        # iterate till u find the first subject.
        # that is the main subject
        for index, token in enumerate(self.tokens[2:]):
            current = current + ' ' + token
            analyzed_form = self.knowledge_analyzer.analyze_segments(
                current,
                subject=True,
                color=True)
            if analyzed_form['SUBJECT']:
                self.start_index = 2 + index + 1
                return analyzed_form['SUBJECT']
        return None