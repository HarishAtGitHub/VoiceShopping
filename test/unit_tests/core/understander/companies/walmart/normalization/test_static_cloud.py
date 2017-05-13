from core.understander.companies.walmart.normalization.static_cloud import *

import unittest

def test_get_facet_meanings():

    expected_op = {'width': ['width', 'breadth', 'beam', 'narrowness', 'wideness', 'broadness', 'dimension'],
                   'brand': ['trade_name', 'brand_name', 'brand', 'marque', 'label', 'recording_label', 'name'],
                   'height': ['height', 'tallness', 'highness', 'loftiness', 'lowness', 'dimension', 'stature', 'height', 'shortness', 'tallness', 'bodily_property', 'altitude', 'height', 'ceiling', 'ceiling', 'level', 'elevation'],
                   'rating': ['evaluation', 'rating', 'marking', 'grading', 'scoring', 'judgment', 'judgement', 'assessment'],
                   'weight': ['weight', 'body_weight', 'dead_weight', 'heaviness', 'weightiness', 'lightness', 'weightlessness', 'poundage', 'tare', 'throw-weight', 'physical_property'],
                   'price': ['monetary_value', 'price', 'cost', 'assessment', 'average_cost', 'expensiveness', 'inexpensiveness', 'marginal_cost', 'incremental_cost', 'differential_cost', 'value', 'price', 'terms', 'damage', 'asking_price', 'selling_price', 'bid_price', 'closing_price', 'factory_price', 'highway_robbery', 'purchase_price', 'spot_price', 'cash_price', 'support_level', 'valuation', 'cost', 'price', 'worth'],
                   'retailer': ['retailer', 'retail_merchant', 'chandler', 'licensee', 'distributor', 'distributer', 'merchant', 'merchandiser'],
                   'length': ['length', 'circumference', 'diameter', 'diam', 'longness', 'radius', 'r', 'shortness', 'dimension', 'fundamental_quantity', 'fundamental_measure', 'physical_property'],
                   'color': ['color', 'colour', 'coloring', 'colouring', 'achromatic_color', 'achromatic_colour', 'chromatic_color', 'chromatic_colour', 'spectral_color', 'spectral_colour', 'coloration', 'colouration', 'complexion', 'skin_color', 'skin_colour', 'heather_mixture', 'heather', 'mottle', 'nonsolid_color', 'nonsolid_colour', 'dithered_color', 'dithered_colour', 'primary_color', 'primary_colour', 'shade', 'tint', 'tincture', 'tone', 'visual_property']}

    test = unittest.TestCase('__init__')
    test.assertDictEqual.__self__.maxDiff = None
    test.assertDictEqual(expected_op, get_facet_meanings())

def test_map_meanings_to_facet():
    expected_op = {'dithered_colour': 'color', 'primary_colour': 'color', 'colouration': 'color', 'diam': 'length', 'fundamental_measure': 'length', 'colouring': 'color', 'tint': 'color', 'support_level': 'price', 'cash_price': 'price', 'terms': 'price', 'licensee': 'retailer', 'purchase_price': 'price', 'throw-weight': 'weight', 'mottle': 'color', 'marque': 'brand', 'tincture': 'color', 'length': 'length', 'tone': 'color', 'skin_color': 'color', 'marginal_cost': 'price', 'heaviness': 'weight', 'circumference': 'length', 'damage': 'price', 'brand': 'brand', 'level': 'height', 'spectral_colour': 'color', 'fundamental_quantity': 'length', 'distributer': 'retailer', 'recording_label': 'brand', 'colour': 'color', 'wideness': 'width', 'body_weight': 'weight', 'evaluation': 'rating', 'retailer': 'retailer', 'primary_color': 'color', 'asking_price': 'price', 'distributor': 'retailer', 'price': 'price', 'poundage': 'weight', 'chromatic_colour': 'color', 'coloration': 'color', 'weightiness': 'weight', 'beam': 'width', 'lightness': 'weight', 'marking': 'rating', 'rating': 'rating', 'skin_colour': 'color', 'cost': 'price', 'selling_price': 'price', 'label': 'brand', 'tallness': 'height', 'merchandiser': 'retailer', 'stature': 'height', 'heather': 'color', 'brand_name': 'brand', 'longness': 'length', 'closing_price': 'price', 'value': 'price', 'grading': 'rating', 'diameter': 'length', 'highness': 'height', 'nonsolid_colour': 'color', 'differential_cost': 'price', 'color': 'color', 'nonsolid_color': 'color', 'factory_price': 'price', 'shade': 'color', 'highway_robbery': 'price', 'dead_weight': 'weight', 'breadth': 'width', 'lowness': 'height', 'radius': 'length', 'chandler': 'retailer', 'visual_property': 'color', 'r': 'length', 'incremental_cost': 'price', 'inexpensiveness': 'price', 'altitude': 'height', 'tare': 'weight', 'narrowness': 'width', 'ceiling': 'height', 'expensiveness': 'price', 'bodily_property': 'height', 'worth': 'price', 'weightlessness': 'weight', 'monetary_value': 'price', 'width': 'width', 'spectral_color': 'color', 'elevation': 'height', 'judgement': 'rating', 'spot_price': 'price', 'average_cost': 'price', 'achromatic_colour': 'color', 'trade_name': 'brand', 'weight': 'weight', 'merchant': 'retailer', 'retail_merchant': 'retailer', 'scoring': 'rating', 'height': 'height', 'bid_price': 'price', 'loftiness': 'height', 'dithered_color': 'color', 'coloring': 'color', 'valuation': 'price', 'broadness': 'width', 'complexion': 'color', 'judgment': 'rating', 'achromatic_color': 'color', 'heather_mixture': 'color', 'chromatic_color': 'color'}
    test = unittest.TestCase('__init__')
    test.assertDictEqual.__self__.maxDiff = None
    test.assertDictEqual(expected_op, map_meanings_to_facet())
