'''
from core.understander.business.shopping.analyzer import Analyzer
analyzer = Analyzer()

question = 'chairs that have cost lesser than three hundred USD rating greater than 4 preference of five'
import time
s = time.time()
print(analyzer.analyze(question))
print('elapsed time %f' % (time.time() - s))
'''
