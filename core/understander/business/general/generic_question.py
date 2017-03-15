'''
from core.commons.time_analyzer import TimeAnalyzer
from core.understander.business.general.question_analyzer import Analyzer

class Analyzer:
    def __init__(self):
        from core.understander.generic.analyzer.grammar.grammar_based_analyzer import GrammarBasedAnalyzer
        self.grammar_analyzer = GrammarBasedAnalyzer()
        from core.understander.generic.analyzer.knowledge.knowledge_based_analyzer import KnowledgeBasedAnalyzer
        self.knowledge_analyzer = KnowledgeBasedAnalyzer()

    def understand(text):
        analyzer = Analyzer()
        question_processed_form = analyzer.analyse(text)
        time_analyzer = TimeAnalyzer(question_processed_form)
        time_analyzer.process_time_phrase()
        return question_processed_form

    def analyze(text):
        return self.knowledge_analyzer. analyse(text)

def get_query_from_sentance(text, query_type=None):
    question_processed_form = understand(text)
    from core.query.query_generator import QueryGenerator
    if not query_type:
        query_generator = QueryGenerator(query_type)
    else:
        query_generator = QueryGenerator("elastic")
    query = query_generator.generate_query(question_processed_form)
    return query
'''