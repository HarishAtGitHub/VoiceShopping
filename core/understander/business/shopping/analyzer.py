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
                    result = self.get_key_value_pair(current)
                    if result:
                        op['attributes'].append(result)
                        self.start_index = self.start_index + index
                        break
                else:
                    break
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
            res = {}
            res['modifiers'] = {}
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
            return res
        else:
            return None


    def get_universal_attributes(self, text):
        analyzed_form = self.knowledge_analyzer.analyze_segments(
            text,
            number=True,
            currency=True,
            color=True)
        res = []
        if analyzed_form['COLOR']:
            color ={'key' : 'color'}
            color['value'] = analyzed_form['COLOR']
            res.append(color)

        if analyzed_form['NUMBER'] and analyzed_form['CURRENCY']:
            # this gives a possibility of money
            money = {'key' : 'money'}
            money['value'] = []
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
                    money['value'].append({'number': num, 'unit': m[1]})
            res.append(money)

        if res:
            return res
        else:
            return None

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