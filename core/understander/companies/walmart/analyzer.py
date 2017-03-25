from constants import ROOT_DIR
from core.commons.company_data import DataStore
from core.understander.business.shopping.analyzer import Analyzer as ShoppingAnalyzer
from properties.core.understander.business.shopping import json_properties as shopping_json_prop
from os.path import dirname, join

class Analyzer:
    def __init__(self):
        materials_file = join(ROOT_DIR, 'data', 'materials', 'walmart_options')
        data = DataStore(materials_file)
        self.analyzer = ShoppingAnalyzer(data)

    def analyze(self, text):
        self.text = text.lower().strip()
        self.analyzed_form =  self.analyzer.analyze(text)
        if self.analyzed_form and self.analyzed_form[shopping_json_prop.MAIN_KEY_NAME]:
            self.get_attributes()

        return self.analyzed_form

    def get_attributes(self):
        self.get_shipping_details()

    def get_shipping_details(self):
        shipping_options = ['two day shipping', 'free pickup today',
                            'ship to home', 'free pickup']
        res = {
            shopping_json_prop.ATTR_KEY : shopping_json_prop.ATTR_SHIPPING,
            shopping_json_prop.ATTR_VALUE : [],
            shopping_json_prop.ATTR_MODIFIER : {}
        }
        for shipping_option in shipping_options:
            if shipping_option in self.text:
                res[shopping_json_prop.ATTR_VALUE].append(shipping_option)
        self.analyzed_form[shopping_json_prop.MAIN_ATTRIBUTES_KEY].append(res)