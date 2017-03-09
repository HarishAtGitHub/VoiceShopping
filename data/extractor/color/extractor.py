from bs4 import BeautifulSoup
import re

# get location of current file
def get_current_file_location():
    import os
    dirname, _ = os.path.split(os.path.abspath(__file__))
    return dirname

def massage_string(string):
    import re
    #if 'green' in string:
    #    print(string)
    excluded_regex = ['\(.*\)', '\[.*\]']
    for rgex in excluded_regex:
        annotations = re.findall('\(.*\)', string)
        for annotation in annotations:
            string = string.replace(annotation, '')


    # replace single quote and hyphen
    string = string.replace("'", '')
    string = string.replace("-", ' ')
    return string.lower().strip()

def parse_wiki(file_name):
    #################### read corpus file ##################################
    corpus_file = get_current_file_location() + '/../../corpus/color/' + file_name

    with open(corpus_file, 'r') as corpus:
        corpus_content = corpus.read()

    #################### load in beautiful soup ##############################
    soup = BeautifulSoup(corpus_content, 'html.parser')
    colors = []
    tr_list = soup.find_all("table", {"class" : "wikitable"})[0].find_all("tr")[1:]

    for tr in tr_list:
        color = tr.find_all('th')[0].text
        colors.append(massage_string(color))
    return colors

wiki_file_list= ['color.corpus1.wiki', 'color.corpus2.wiki', 'color.corpus3.wiki']
op = []
for file_name in wiki_file_list:
    colors = parse_wiki(file_name)
    op = op + colors

op = set(op)

####################### store the extract in the serialized form ################
extract_file = get_current_file_location() + '/../../extract/color.ser'
with open(extract_file, 'wb') as storage_file:
    import pickle
    pickle.dump(op, storage_file)


################# display the serialized file ##############################
with open(extract_file, 'rb') as storage_file:
    import pickle
    obj = pickle.load(storage_file)
    print(obj)