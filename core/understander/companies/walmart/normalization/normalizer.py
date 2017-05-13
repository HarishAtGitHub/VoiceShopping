class Normalizer():
    def __init__(self, data):
        self.data = data


    def normalize(self):
        from core.understander.companies.walmart.normalization.word_cloud import WordCloud
        print(WordCloud.get_static_word_cloud())

if __name__ == '__main__':
    n = Normalizer("dummy")
    print("working")
    n.normalize()