from core.commons.time_analyzer import TimeAnalyzer
from core.understander.business.general.question_analyzer import Analyzer


def understand(text):
    analyzer = Analyzer(text)
    question_processed_form = analyzer.analyse()
    time_analyzer = TimeAnalyzer(question_processed_form)
    time_analyzer.process_time_phrase()
    return question_processed_form

def analyze(text):
    return Analyzer(text).analyse()

def get_query_from_sentance(text, query_type=None):
    question_processed_form = understand(text)
    from core.query.query_generator import QueryGenerator
    if not query_type:
        query_generator = QueryGenerator(query_type)
    else:
        query_generator = QueryGenerator("elastic")
    query = query_generator.generate_query(question_processed_form)
    return query
