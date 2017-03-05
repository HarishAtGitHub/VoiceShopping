from bs4 import BeautifulSoup
import re

# get location of current file
def get_current_file_location():
    import os
    dirname, _ = os.path.split(os.path.abspath(__file__))
    return dirname

# process string to nomalize it
def massage_string(string):
    # remove referrence annotation
    annotations = re.findall('\[.*\]', string)
    for annotation in annotations:
        string = string.replace(annotation, '')

    # remove hex string
    string = string.replace('\xa0', '')

    # make (none) to a string that will not occur
    if string == '(none)':
        string = 'zzzzzz'
    # lower case
    return string.lower()

#################### read corpus file ##################################
corpus_file = get_current_file_location() + '/../../corpus/currency.corpus.wiki'

with open(corpus_file, 'r') as corpus:
    corpus_content = corpus.read()

#################### load in beautiful soup ##############################
soup = BeautifulSoup(corpus_content, 'html.parser')

#################### extract content ####################################
trs = soup.find("table").find("tbody").find_all("tr")

currency_fractional_units = set()
currency_short_forms = set()
currency_long_forms = set()
currency_readable_forms = set()
count = 0
rowspan = None
for tr in trs:
    tds = tr.find_all('td')
    try:
        rowspan = tds[0].attrs['rowspan']
    except KeyError as ke:
        rowspan = None
        pass # means no rowspan attribute found so we silently pass
    if(rowspan):
        count = int(rowspan)
        currency_long_forms.add(massage_string(tds[1].text))
        currency_short_forms.add(massage_string(tds[3].text))
        currency_fractional_units.add(massage_string(tds[4].text))
        count = count - 1
        continue

    if(count >= 1):
        currency_long_forms.add(massage_string(tds[0].text))
        currency_short_forms.add(massage_string(tds[2].text))
        currency_fractional_units.add(massage_string(tds[3].text))
        count = count - 1
    else:
        currency_long_forms.add(massage_string(tds[1].text))
        currency_short_forms.add(massage_string(tds[3].text))
        currency_fractional_units.add(massage_string(tds[4].text))

misc = set(['usd', 'rupees', 'rupee', 'rs'])
'''
extract_object = {'currency_long_forms' : currency_long_forms,
                  'currency_short_forms' : currency_short_forms,
                  'currency_fractional_units' : currency_fractional_units,
                  'misc': misc}
'''
extract_object = currency_long_forms.union(currency_short_forms)\
    .union(currency_fractional_units)\
    .union(misc)
extract_file = get_current_file_location() + '/../../extract/currency.ser'

####################### store the extract in the serialized form ################
with open(extract_file, 'wb') as storage_file:
    import pickle
    pickle.dump(extract_object, storage_file)


################# display the serialized file ##############################
with open(extract_file, 'rb') as storage_file:
    import pickle
    obj = pickle.load(storage_file)
    print(obj)
