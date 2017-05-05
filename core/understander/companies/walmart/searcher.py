from constants import QUERY_STRING_SEPARATOR as qss
from constants import WALMART_SEARCH_URL
from requests import get

COLOR_KEY = "facet.filter=color:"

class Searcher:

    @classmethod
    def get_value_as_list(cls, value):
        #NOTE: converting all types to list to avoid if else conditions
        #FIXME: when the value list contains multiple entries, multiple
        #facet.filter/range params are appended into query string. is this ok?
        value_map = {int : [value], str : [value], list : value, dict : []}
        #FIXME ignore values of type dict until we figure out how to handle
        return value_map[type(value)]

    @classmethod
    def get_range_min_max(cls, attr, relation):
        lowest = "0"
        #FIXME: what should be the highest value?
        #it could vary based on attr - eg. cost, length
        highest = "1000"
        value = attr.get("value")
        value = cls.get_value_as_list(value)
        min_max_list = [{"<": (lowest, str(v)), ">": (str(v), highest)}[relation[0]] for v in value]
        return min_max_list

    @classmethod
    def add_facet(cls, attrs, url_parts):
        url_parts.append("facet=on")
        for attr in attrs:
            key = attr.get("key")
            try:
                modifiers = attr["modifiers"]
                relation = modifiers["relation"]
                mm_list = cls.get_range_min_max(attr, relation)
                [url_parts.append("facet.range=" + key + ":[" + min + "+TO+" + max + "]") for min, max in mm_list]
            except KeyError:
                value = attr.get("value")
                value = cls.get_value_as_list(value)
                [url_parts.append("facet.filter=" + key + ":" + v) for v in value]
        return url_parts

    @classmethod
    def construct_url(cls, analyzed_form):
        url_parts = [WALMART_SEARCH_URL]
        parsed_output = analyzed_form
        product = str(parsed_output.get("product")[0])
        url_parts.append("query=" + product)
        attrs = parsed_output.get("attributes")
        url_parts = cls.add_facet(attrs, url_parts)
        wmurl = '&'.join(url_parts)
        return wmurl

    @staticmethod
    def handle_special_cases(walmart_url):
        # walmart api syntax says 'price' so replace 'cost' and remove 'money'
        walmart_url = walmart_url.replace('cost', 'price')

        # walmart API processes color only when first letter is capitalized
        split1 = walmart_url.split(COLOR_KEY)
        try:
            split2 = split1[1].split(qss)
        except IndexError:
            # no color in url so return
            return walmart_url
        split2[0] = split2[0].title()
        split1[1] = qss.join(split2)
        walmart_url = COLOR_KEY.join(split1)
        return walmart_url

    @staticmethod
    def make_request(url):
        response = get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return []

    @classmethod
    def fetch_results(cls, analyzed_form):
        return cls.make_request(cls.handle_special_cases(cls.construct_url(analyzed_form)))


