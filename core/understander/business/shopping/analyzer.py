from core.understander.generic.question_category_dict import *

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
            date=False,
            number=True,
            currency=True,
            subject=True,
            action=True)
        if len(analyzed_form['SUBJECT']) > 1 or self.running_index == len(self.tokens) - 1:
            res = {}
            if analyzed_form['NUMBER']:
                res[analyzed_form['SUBJECT'][0]] = analyzed_form['NUMBER'][0]
            if analyzed_form['CURRENCY']:
                res['CURRENCY'] = analyzed_form['CURRENCY'][0]
            return res
        else:
            return None


    def get_universal_attributes(self, text):
        analyzed_form = self.knowledge_analyzer.analyze_segments(
            text,
            person=False,
            date=False,
            number=False,
            currency=False,
            subject=False,
            action=False,
            color=True)
        res = []
        if analyzed_form['COLOR']:
            color = {'COLOR' : analyzed_form['COLOR']}
            res.append(color)

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
                person=False,
                date=False,
                number=False,
                currency=False,
                subject=True,
                action=False,
                color=True)
            if analyzed_form['SUBJECT']:
                self.start_index = 2 + index + 1
                return analyzed_form['SUBJECT']
        return None