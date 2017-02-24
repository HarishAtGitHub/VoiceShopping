class QueryGenerator:
    def __init__(self, query_type):
        self.query_type = query_type

    def generate_query(self, question_processed_form):
        if self.query_type == 'elastic':
            return ElasticQueryGenerator.generate_query(question_processed_form)
        elif self.query_type == 'sql':
            return SQLQueryGenerator.generate_query(question_processed_form)
        else:
            return ElasticQueryGenerator.generate_query(question_processed_form)


class ElasticQueryGenerator:
    @classmethod
    def generate_query(cls, question_processed_form):
        query = {
            "query": {
                "range": {
                    "event_start_date_machine": {
                        "gte": "start_time",
                        "lte": "end_time",
                        "format": "YYYY-MM-dd HH:mm:ss"
                    }
                }
            }
        }
        if 'time_phrase' in question_processed_form and question_processed_form['time_phrase']:
            times = question_processed_form['time_phrase'].split(sep='***')
            query['query']['range']['event_start_date_machine']['gte'] = times[0]
            query['query']['range']['event_start_date_machine']['lte'] = times[1]
            return query
        else:
            return None


class SQLQueryGenerator:
    @classmethod
    def generate_query(cls, question_processed_form):
        pass
