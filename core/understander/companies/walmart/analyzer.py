from core.understander.business.shopping.analyzer import Analyzer as ShoppingAnalyzer
from properties.core.understander.business.shopping import json_properties as shopping_json_prop

MATERIALS = [
    "Fabric",
    "Leather",
    "Wood",
    "Microfiber",
    "Plastic",
    "Faux Leather",
    "Metal",
    "Vinyl",
    "Steel",
    "Polyester",
    "Rubber",
    "MESH",
    "Upholstered",
    "Foam",
    "Polyster",
    "100% Polyester",
    "Resin",
    "Bonded Leather",
    "Polycarbonate",
    "Resin Wicker"
]

class Analyzer:
    def __init__(self):
        self.analyzer = ShoppingAnalyzer()
        self.analyzer.add_additional_materials(MATERIALS)

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