from core.commons.text2num import text2num, NumberException
from properties.core.understander.business.shopping import json_properties as shopping_json_prop
import re
from properties.core.understander.business.shopping import messages
from core.commons.exceptions import UnableToUnderstandException

class Analyzer:
    # instantiate analyzer only once and reuse it or else each time it takes time
    def __init__(self):
        from core.understander.generic.analyzer.grammar.grammar_based_analyzer import GrammarBasedAnalyzer
        self.grammar_analyzer = GrammarBasedAnalyzer()
        from core.understander.generic.analyzer.knowledge.knowledge_based_analyzer import KnowledgeBasedAnalyzer
        self.knowledge_analyzer = KnowledgeBasedAnalyzer()

    def add_additional_materials(self, materials = []):
        self.knowledge_analyzer.add_additional_materials(materials)

    def analyze(self, text):
        self.text = text.lower().strip()
        self.text = re.sub('\s\s+', ' ', self.text)

        self.tokens = self.text.split(' ')
        self.start_index = 0
        self.running_index = 0

        # get product name
        op = {}
        product = self.get_main_product()
        if product:
            op[shopping_json_prop.MAIN_KEY_NAME] = product
        else:
            raise UnableToUnderstandException(messages.UNABLE_TO_UNDERSTAND)

        # get product attributes
        op[shopping_json_prop.MAIN_ATTRIBUTES_KEY] = []
        self.running_index = self.start_index
        current = ''
        while True:
            if self.start_index < len(self.tokens) - 1:
                for index, token in enumerate(self.tokens[self.start_index:]):
                    self.running_index = self.start_index + index
                    current = current + ' ' + token
                    result, analyzed_form = self.get_key_value_pair(current)
                    if result:
                        op[shopping_json_prop.MAIN_ATTRIBUTES_KEY].extend(result)
                        self.start_index = self.start_index + index
                        break
                else:
                    break
                # before discarding the sentence see if you can make sense of it
                res = self.get_possible_meaning(text, analyzed_form)
                if res:
                    op[shopping_json_prop.MAIN_ATTRIBUTES_KEY].extend(res)
                # discard the sentence
                current = ''
                continue
            else:
                break
        # get global attributes to handle cases like get green  chairs
        universal_attrib = self.get_universal_attributes(text)
        if universal_attrib:
            op[shopping_json_prop.MAIN_ATTRIBUTES_KEY] = op[shopping_json_prop.MAIN_ATTRIBUTES_KEY] + universal_attrib

        op = self.process_output(op)
        # return product details
        return op

    def process_output(self, output):
        if output[shopping_json_prop.MAIN_ATTRIBUTES_KEY]:
            output[shopping_json_prop.MAIN_ATTRIBUTES_KEY] = self.remove_duplicate_attributes(
                output[shopping_json_prop.MAIN_ATTRIBUTES_KEY])
        return output

    def remove_duplicate_attributes(self, attributes):
        # TODO: devise a better way to remove duplicate attributes
        money_seen = False
        color_seen = False
        properties = []
        for attrib in attributes:
            if attrib['key'] == 'money':
                if not money_seen:
                    properties.append(attrib)
                    money_seen = True
                continue
            elif attrib['key'] == 'color':
                if not color_seen:
                    properties.append(attrib)
                    color_seen = True
                continue
            else:
                properties.append(attrib)
        return properties

    def get_key_value_pair(self, text):
        analyzed_form = self.knowledge_analyzer.analyze_segments(
            text,
            person=True,
            number=True,
            currency=True,
            subject=True,
            action=True,
            math_comparisons=True)

        # 3 cases
        # 1. more than one subject found so it is time to map the first subject to value
        # 2. sentence has ended
        #       a) one subject with one value so try to get value
        #       b) one subject with no value so just get the meaning
        #       b) no subject case so just get meaning
        # 3. else
        if len(analyzed_form['SUBJECT']) > 1:

            op = []

            res = {}
            res[shopping_json_prop.ATTR_MODIFIER] = {}
            res[shopping_json_prop.ATTR_KEY] = ''
            res[shopping_json_prop.ATTR_VALUE] = ''
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
            res = self.get_value(analyzed_form)
            if res and res[shopping_json_prop.ATTR_KEY]:
                op.append(res)

            if op:
                return op, analyzed_form
            else:
                return None, analyzed_form
        elif  self.running_index == len(self.tokens) - 1:
            if len(analyzed_form['SUBJECT']) == 1:
                op = []
                res = {}
                res[shopping_json_prop.ATTR_MODIFIER] = {}
                res[shopping_json_prop.ATTR_KEY] = ''
                res[shopping_json_prop.ATTR_VALUE] = ''
                res[shopping_json_prop.ATTR_KEY] = analyzed_form['SUBJECT'][0]
                res = self.get_value(analyzed_form)
                if res and res[shopping_json_prop.ATTR_KEY]:
                    if res[shopping_json_prop.ATTR_VALUE] :
                        op.append(res)
                    else:
                        meanings = self.get_possible_meaning(text, analyzed_form)
                        if meanings:
                            op.extend(meanings)
                if op:
                    return op, analyzed_form
                else:
                    return None, analyzed_form

            else: #means no subject so just get possible meaning
                op = []
                meanings = self.get_possible_meaning(text, analyzed_form)
                if meanings:
                    op.extend(meanings)
                if op:
                    return op, analyzed_form
                else:
                    return None, analyzed_form
        else:
            return None, analyzed_form

    def get_value(self, analyzed_form):
        res = {}
        res[shopping_json_prop.ATTR_MODIFIER] = {}
        res[shopping_json_prop.ATTR_KEY] = ''
        res[shopping_json_prop.ATTR_VALUE] = ''
        if analyzed_form['NUMBER']:
            res[shopping_json_prop.ATTR_KEY] = analyzed_form['SUBJECT'][0]
            try:
                res[shopping_json_prop.ATTR_VALUE] = int(text2num(analyzed_form['NUMBER'][0]))
            except NumberException as ne:
                try:
                    res[shopping_json_prop.ATTR_VALUE] = int(analyzed_form['NUMBER'][0])
                except ValueError as ve:
                    res[shopping_json_prop.ATTR_VALUE] = analyzed_form['NUMBER'][0]
        if analyzed_form['CURRENCY']:
            res[shopping_json_prop.ATTR_MODIFIER]['CURRENCY'] = analyzed_form['CURRENCY'][0]
        if analyzed_form['RELATION']:
            res[shopping_json_prop.ATTR_MODIFIER][shopping_json_prop.ATTR_MODIFIER_RELATION] = analyzed_form['RELATION']

        return res

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
                res[shopping_json_prop.ATTR_KEY] = shopping_json_prop.ATTR_TARGET_AUDIENCE
                res[shopping_json_prop.ATTR_VALUE] = analyzed_form['SUBJECT'][0]
        '''


        # check money
        res = {}
        res[shopping_json_prop.ATTR_MODIFIER] = {}
        res[shopping_json_prop.ATTR_KEY] = ''
        res[shopping_json_prop.ATTR_VALUE] = []
        if analyzed_form['NUMBER'] and analyzed_form['CURRENCY']:
            money = self.get_money(text, analyzed_form)
            res[shopping_json_prop.ATTR_KEY] = money[shopping_json_prop.ATTR_KEY]
            res[shopping_json_prop.ATTR_VALUE] = money[shopping_json_prop.ATTR_VALUE]
            res[shopping_json_prop.ATTR_MODIFIER] = money[shopping_json_prop.ATTR_MODIFIER]
        if res[shopping_json_prop.ATTR_KEY]:
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
            color=True,
            material=True)
        op = []

        # check color
        if analyzed_form['COLOR']:
            color ={shopping_json_prop.ATTR_KEY : shopping_json_prop.ATTR_COLOR}
            color[shopping_json_prop.ATTR_VALUE] = analyzed_form['COLOR']
            op.append(color)

        # check and set material
        material = analyzed_form['MATERIAL']
        if material:
            material_attr = {shopping_json_prop.ATTR_KEY : shopping_json_prop.ATTR_MATERIAL}
            material_attr[shopping_json_prop.ATTR_VALUE] = material
            op.append(material_attr)

        # check money
        if analyzed_form['NUMBER'] and analyzed_form['CURRENCY']:
            money = self.get_money(text, analyzed_form)
            op.append(money)

        # check life stage
        life_stages = ['adult', 'child', 'teen', 'toddler', 'infant', 'kid']
        res = {}
        res[shopping_json_prop.ATTR_MODIFIER] = {}
        res[shopping_json_prop.ATTR_KEY] = ''
        res[shopping_json_prop.ATTR_VALUE] = []
        for life_stage in life_stages:
            if life_stage in text:
                res[shopping_json_prop.ATTR_KEY] = shopping_json_prop.ATTR_TARGET_AUDIENCE
                res[shopping_json_prop.ATTR_VALUE].append(life_stage)
        if res[shopping_json_prop.ATTR_KEY]:
            op.append(res)

        if op:
            return op
        else:
            return None

    def get_money(self, text, analyzed_form):
        # this gives a possibility of money
        money = {shopping_json_prop.ATTR_KEY: shopping_json_prop.ATTR_MONEY}
        money[shopping_json_prop.ATTR_VALUE] = ''
        money[shopping_json_prop.ATTR_MODIFIER] = {}
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
                money[shopping_json_prop.ATTR_VALUE] = {shopping_json_prop.ATTR_NUMBER: num, shopping_json_prop.ATTR_UNIT: m[1]}

        if analyzed_form['RELATION']:
            money[shopping_json_prop.ATTR_MODIFIER][shopping_json_prop.ATTR_MODIFIER_RELATION] = analyzed_form['RELATION']

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
                material=True,
                color=True)
            if analyzed_form['SUBJECT']:
                self.start_index = 2 + index + 1
                return analyzed_form['SUBJECT']
        return None
