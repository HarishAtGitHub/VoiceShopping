import unittest
from core.understander.companies.walmart.api.facet import get_facets
from core.understander.companies.walmart.api.facet import get_ui_url
from core.understander.companies.walmart.api.facet import get_facets_in_webpage
from core.understander.companies.walmart.api.facet import get_web_page

test = unittest.TestCase()

def test_get_ui_url():
    expected_op = "www.domain.com/?q=chairs"
    result = get_ui_url("www.domain.com/", {"q" : "chairs"})
    test.assertEquals(expected_op, result)

def test_get_facets():
    expected_op = None # no item given case
    result = get_facets()
    test.assertEquals(None, result)

def test_get_facets_in_webpage():
    expected_op = None # no web page case
    result = get_facets_in_webpage()
    test.assertEquals(None, result)

def test_get_web_page():
    expected_op = None  # no url case
    result = get_web_page()
    test.assertEquals(None, result)

if __name__=='__main__':
    test_get_ui_url()
    test_get_facets()
    test_get_facets_in_webpage()