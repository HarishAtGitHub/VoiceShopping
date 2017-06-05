from os.path import dirname

ROOT_DIR = dirname(__file__)
WALMART_API_ENDPOINT = "http://api.walmartlabs.com"
WALMART_SEARCH_API_PATH = "/v1/search"
QUERY_STRING_SEPARATOR = "?"
API_KEY_PARAM = "apiKey=vjcgatgh6wfxzd7wbaqj5v7a"
WALMART_SEARCH_URL = ''.join([WALMART_API_ENDPOINT, WALMART_SEARCH_API_PATH,
                              QUERY_STRING_SEPARATOR, API_KEY_PARAM])
WALMART_UI_URL = 'https://www.walmart.com/search/'