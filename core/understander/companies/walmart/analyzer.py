from core.understander.business.shopping.analyzer import Analyzer as ShoppingAnalyzer
from properties.core.understander.business.shopping import json_properties as shopping_json_prop
from properties.core.understander.business.shopping import messages
from core.commons.exceptions import UnableToUnderstandException

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

    def analyze(self, text, knowledge=False):
        self.text = text.lower().strip()
        if not knowledge:
            try:
                self.analyzed_form = self.analyzer.analyze(text)
            except UnableToUnderstandException as utue:
                raise utue
            except:
                raise UnableToUnderstandException(messages.UNABLE_TO_UNDERSTAND)

            if self.analyzed_form and self.analyzed_form[shopping_json_prop.MAIN_KEY_NAME]:
                self.get_attributes()

            return self.analyzed_form
        else:
            product = self.analyzer.get_product(text)
            if product:
                from core.understander.companies.walmart.knowledge import get_knowledge
                return get_knowledge(product[0])
            else:
                raise UnableToUnderstandException(messages.UNABLE_TO_UNDERSTAND)

    def get_attributes(self):
        shipping_details = self.get_shipping_details()
        if shipping_details:
            self.analyzed_form[shopping_json_prop.MAIN_ATTRIBUTES_KEY].append(shipping_details)

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
        if res[shopping_json_prop.ATTR_VALUE]:
            return res
        else:
            return None
