from core.understander.generic.question_analyzer import Analyzer
analyzer = Analyzer()
#text = 'what is the lantern walk'
#print(analyzer.analyze(text))
#text = 'what sports events are happening next week'
#print(analyzer.analyze(text))
from test.inputs.generic_question import what, who, misc_questions

print(analyzer.analyze('who is playing foot ball'))
for q in misc_questions:
   print(analyzer.analyze(q))
for q in who:
   print(analyzer.analyze(q))
for q in what:
   print(analyzer.analyze(q))
