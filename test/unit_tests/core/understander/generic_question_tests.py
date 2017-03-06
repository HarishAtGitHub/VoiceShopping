from core.understander.business.shopping.analyzer import Analyzer
analyzer = Analyzer()

question = 'chairs that have cost lesser than three hundred USD rating greater than 4 preference of five'
print(analyzer.analyze(question))

'''
from core.understander.generic.generic_question import Analyzer

question = 'what are the main countries liked by Hitler during 1987'
analyzer = Analyzer()
print(analyzer.analyze(question,
                       ))
'''