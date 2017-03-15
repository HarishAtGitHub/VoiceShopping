class TimeAnalyzer():
    def __init__(self, question_processed_form):
        self.question_processed_form = question_processed_form

    def process_time_phrase(self):
        # TODO: Support all time phrases
        import arrow
        datetime_format = "%Y-%m-%d %H:%M:%S"
        date_format = "%Y-%m-%d"
        separator = '***'
        if 'time_phrase' in self.question_processed_form:
            #print(question_processed_form['time_phrase'])
            time_phrase = self.question_processed_form['time_phrase']
            if time_phrase.startswith('next'):
                exact_time = time_phrase.replace('next', '').strip()
                self.question_processed_form['time_phrase'] = self.process_time_word(exact_time, 1, datetime_format, date_format, separator)
            elif time_phrase.startswith('last'):
                exact_time = time_phrase.replace('last', '').strip()
                self.question_processed_form['time_phrase'] = self.process_time_word(exact_time, -1, datetime_format, date_format, separator)
            elif time_phrase.startswith('now'):
                now = arrow.now().strftime(datetime_format)
                self.question_processed_form['time_phrase'] = now + separator + now
            elif time_phrase.startswith('today'):
                time = arrow.now()
                self.question_processed_form['time_phrase'] = time.datetime.strftime(date_format) + ' 00:00:00' + separator + \
                                                         time.datetime.strftime(date_format) + ' 23:59:59'
            elif time_phrase.startswith('tomorrow'):
                time = arrow.now().shift(days=1)
                self.question_processed_form['time_phrase'] = time.datetime.strftime(date_format) + ' 00:00:00' + separator + \
                                                         time.datetime.strftime(date_format) + ' 23:59:59'
            elif time_phrase.startswith('day after tomorrow'):
                time = arrow.now().shift(days=2)
                self.question_processed_form['time_phrase'] = time.datetime.strftime(date_format) + ' 00:00:00' + separator + \
                                                         time.datetime.strftime(date_format) + ' 23:59:59'
            elif time_phrase.startswith('soon'):
                now = arrow.now().strftime(datetime_format)
                future = arrow.now().shift(hours=4).strftime(datetime_format)
                self.question_processed_form['time_phrase'] = now + separator + future

    def process_time_word(self, exact_time, indicator, datetime_format, date_format, sep):
        import arrow
        timenow = arrow.now()
        if exact_time == 'week':
            if indicator == 1:
                time = timenow.shift(weeks=1)
                weekday = time.weekday()
                result = time.shift(days=-weekday).datetime.strftime(date_format) + ' 00:00:00' + sep + \
                         time.shift(days=6-weekday).datetime.strftime(date_format) + ' 23:59:59'
            elif indicator == -1:
                time = timenow.shift(weeks=-1)
                weekday = time.weekday()
                result = time.shift(days=-weekday).datetime.strftime(date_format) + ' 00:00:00' + sep + \
                         time.shift(days=6-weekday).datetime.strftime(date_format) + ' 23:59:59'
            return result

        elif exact_time == 'month':
            import calendar
            if indicator == 1:
                time = timenow.shift(months=1)
                month = time.month
                year = time.year
                day = time.day
                days = calendar.monthrange(year,month)[1]
                result = time.shift(days=-day+1).datetime.strftime(date_format) + ' 00:00:00' + sep + \
                         time.shift(days=days-day).datetime.strftime(date_format) + ' 23:59:59'
            elif indicator == -1:
                time = timenow.shift(months=-1)
                month = time.month
                year = time.year
                day = time.day
                days = calendar.monthrange(year,month)[1]
                result = time.shift(days=-day+1).datetime.strftime(date_format) + ' 00:00:00' + sep + \
                         time.shift(days=days-day).datetime.strftime(date_format) + ' 23:59:59'
            return result
        elif exact_time == 'year':
            if indicator == 1:
                year = timenow.year
                result = str(year+1) + '-01-01 00:00:00' + sep + str(year+1) + '-12-31 23:59:59'
            elif indicator == -1:
                year = timenow.year
                result = str(year-1) + '-01-01 00:00:00' + sep + str(year-1) + '-12-31 23:59:59'
            return result
        '''
        elif exact_time == 'weekend':
            if indicator == 1:

            elif indicator == -1:
        elif exact_time == 'morning':
            if indicator == 1:

            elif indicator == -1:
        elif exact_time == 'afternoon':
            if indicator == 1:

            elif indicator == -1:

        elif exact_time == 'night':
            if indicator == 1:

            elif indicator == -1:
        '''
