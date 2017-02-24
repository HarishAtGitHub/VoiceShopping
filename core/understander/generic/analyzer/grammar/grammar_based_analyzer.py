class GrammarBasedAnalyzer:
    def __init__(self):
        self.tagged_output = {}

    def analyze(self, text):
        self.tagged_output['INPUT_TEXT'] = text
        grammars = [('map.cfg', 'direction', 'LOCATION')]
        for grammar in grammars:
            trees = self.get_processed_trees(grammar=grammar[0])
            match_found = False
            for tree in trees:
                match_found = True
                subject_phrase = self.tree_iterator(tree, grammar[2]).leaves()
                subject_phrase = ''.join(subject_phrase)
                self.tagged_output['SUBJECT'] = [subject_phrase]
                self.tagged_output[grammar[2]] = [subject_phrase]
                self.tagged_output['TYPE'] = grammar[1]

            if match_found:
                return self.tagged_output
            else:
                self.tagged_output['SUBJECT'] = 'NOT FOUND'
                return self.tagged_output


    def get_processed_trees(self, grammar=None, trace=False):
        import os
        grammar_file = os.path.join(os.path.dirname(__file__), '../../../../../grammars/',
                                        grammar)
        with open(grammar_file, 'r') as file:
            grammar_str = file.read()
        import nltk
        grammar_content = nltk.PCFG.fromstring(grammar_str)
        parser = nltk.ViterbiParser(grammar_content)
        if trace: parser.trace()
        trees = parser.parse(self.tagged_output['INPUT_TEXT'])
        return trees

    def tree_iterator(self, tree, label):
        value = None
        for a in tree:
            if isinstance(a, str):
                continue
            if a.label() == label:
                value = a
                break
            else:
                temp = self.tree_iterator(a, label)
                if temp is not None:
                    value = temp
        return value