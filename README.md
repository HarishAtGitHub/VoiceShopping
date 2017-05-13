######### Understander Service ###########

export PYTHONPATH=`pwd`

Install python3
https://www.python.org/downloads/

sudo pip3 install flask spacy nltk

sudo python3 -m spacy.en.download all

sudo python3
>>> import ssl
>>> try:
...     _create_unverified_https_context = ssl._create_unverified_context
... except AttributeError:
...     pass
... else:
...     ssl._create_default_https_context = _create_unverified_https_context
... 
>>> nltk.download('wordnet')
>>> nltk.download('punkt')

python3 service/understander.py


######### developers ####################3

How to test ?
=============

sudo apt install python-nose3
sh test.sh
