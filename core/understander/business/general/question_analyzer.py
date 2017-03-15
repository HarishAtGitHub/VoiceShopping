from core.understander.business.general.question_category_dict import *

class Analyzer:
    # instantiate analyzer only once and reuse it or else each time it takes time
    def __init__(self):
        from core.understander.generic.analyzer.grammar.grammar_based_analyzer import GrammarBasedAnalyzer
        self.grammar_analyzer = GrammarBasedAnalyzer()
        from core.understander.generic.analyzer.knowledge.knowledge_based_analyzer import KnowledgeBasedAnalyzer
        self.knowledge_analyzer = KnowledgeBasedAnalyzer()

    def analyze(self,
                text):
        self.text = text.lower()
        # categorize text
        self.categorize()

        # handle based on the category
        '''
        if(self.question_processed_form['category'] == 'other'):
            result = self.grammar_analyzer.analyze(self.question.question_extract)
            if result['SUBJECT'] == 'NOT FOUND':
                return self.knowledge_analyzer.analyze(self.question.question_extract)
            else:
                return result
        else:
            return self.knowledge_analyzer.analyze(self.question.question_extract)
        '''
        return self.knowledge_analyzer.analyze(self.question.question_extract,
                                               person=True,
                                               date=True,
                                               number=True,
                                               currency=True,
                                               subject=True,
                                               action=True)

    def categorize(self):
        import re
        selected_marker = selected_category = question_extract = None
        # question_markers = question_category.keys()
        for marker in question_markers:
            if re.search(marker, self.text):
                selected_marker = marker
                selected_category = question_category[selected_marker]
                question_extract = self.text[self.text.index(selected_marker):]
                break

        if selected_category is None:
            selected_marker = 'other'
            selected_category = 'other'
            question_extract = self.text

        from collections import namedtuple
        Question = namedtuple('Question', ['category', 'marker_value', 'question_extract','actual_question'])
        question = Question(category=selected_category,
                            marker_value=selected_marker,
                            question_extract=question_extract,
                            actual_question=self.text)
        self.question = question
        self.question_processed_form = {
            'category': question.category,
            'actual_question' : question.actual_question
        }
