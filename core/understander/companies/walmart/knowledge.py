def get_knowledge(product : str):
    from core.understander.companies.walmart.normalization.word_cloud import WordCloud
    static_word_cloud =  WordCloud.get_static_word_cloud()
    dynamic_word_cloud = WordCloud.get_dynamic_word_cloud(product)
    return {
        'static' : static_word_cloud,
        'dynamic' : dynamic_word_cloud
    }