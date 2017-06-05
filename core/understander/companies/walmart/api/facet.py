from constants import WALMART_UI_URL

def get_ui_url(url, query_params):
    query_strings = []
    for key, value in query_params.items():
        query_strings.append(key + '=' + value)
    query_string = '&'.join(query_strings)
    return url + '?' + query_string

def get_web_page(url=None):
    # BASE CASE
    if not url: return None

    import requests
    web_page = requests.get(url)
    return web_page.content

def get_facets_in_webpage(web_page=None):
    # BASE CASE
    if not web_page: return None

    from bs4 import BeautifulSoup
    web_page_soup = BeautifulSoup(web_page, 'html.parser')
    sidebar_div_tag = get_sidebar_div_tag(web_page_soup)
    facet_html_elements = get_facet_html_elements_from_sidebar_div(sidebar_div_tag)
    return get_all_facets_info(facet_html_elements)

def get_sidebar_div_tag(web_page_soup):
    divs = web_page_soup.findAll('div', {'class': 'sidebar-container'})
    if not len(divs) > 0: return None  # no items in sidebar so returning
    sidebar_div_tag = divs[0]  # just assuming that it is the first div
    return sidebar_div_tag

def get_facet_html_elements_from_sidebar_div(sidebar_div_tag):
    facets_div_tag = sidebar_div_tag.children
    facet_html_elements = []
    for facet_div_tag in facets_div_tag:
        #print(facet_div_tag.get('aria-label'))
        #inner_tags = facet_div_tag.children
        #for inner_tag in inner_tags:
        #   facet_html_elements.append(inner_tag)
        facet_html_elements.append(facet_div_tag)
    return facet_html_elements

def get_all_facets_info(facet_html_elements):
    result = {}
    for facet_html_element in facet_html_elements:
        #print(get_facets_bar(facet_html_element))
        #options_type = facet_html_element.get('class')
        #if not options_type: break
        #print(options_type[0])
        name_list = facet_html_element.findAll('a', {'class': 'expander-toggle'})
        if not name_list:
            return None
        else:
            facet_name = name_list[0].text
            facet_info = get_facet_info(facet_html_element)
            if facet_info:
                result[facet_name] = facet_info
            else:
                continue
    return result

def get_facet_info(facet_html_element):
    # we have 3 types as far as walmart is concerned
    # 1. departments-facet-desktop     <dept-facet-desktop>               <aria-level>
    # 2. facets-bar                    <facets-bar>               <" ">   <aria-level>
    # 3. general-checkbox-facet        <general-checkbox-facet>   (2)

    # as far as html is concerned we have 3 types
    # 1. checkbox (facet-item-list)
    # 2. radio button (radio-button-facet)
    # 3. textbox + checkbox (eg. price) (we can just take the checkbox) (or we can eliminate price)
    # so analyse each and return a json including name, type, options-type, options


    inner_div = facet_html_element.find('div', recursive=False)
    facet_type = inner_div.get('class')
    if not facet_type: return None
    return get_info_from_html(inner_div)

def get_info_from_html(html_element):
    possible_facet_html_element_types = ['radio-button-facet',
                                         'facet-item-list',
                                         'department-facet-list']
    result = None
    for possible_facet_html_element_type in possible_facet_html_element_types:
        form_element = html_element.find('div', {'class': possible_facet_html_element_type})
        if form_element:
            result = form_element
            break # we found out so we are breaking
    if result:
        return parse_html_element(form_element)
    else:
        return None

###
# in future if you want to parse new element type just add the entry to the method_mapping and
# add te corresponding function to have the functionality to parse the element
# also add the item to the list  possible_facet_html_element_types
#
###
def parse_html_element(element):
    class_name = element.get('class')
    if class_name:
        method_mapping = {
            'radio-button-facet': parse_radio_button_facet,
            'facet-item-list': parse_facet_item_list,
            'department-facet-list': parse_department_facet_list
        }
        return method_mapping[class_name[0]](element)
    else: return None

def parse_radio_button_facet(element):
    values = []
    type = 'radio'
    for div in element.findAll('div', {'class': type}):
        span_elements = div.findAll('span')
        if not span_elements:
            continue
        else:
            value = ''
            for span_element in span_elements:
                value = value + span_element.text
            values.append(value)
    result = {'type': type,
              'values': values}
    return result

def parse_facet_item_list(element):
    values = []
    type = 'option'
    for div in element.findAll('div', {'class' : type}):
        input_elements = div.findAll('input')
        if not input_elements:
            continue
        else:
            for input_element in input_elements:
                values.append(input_element.get('name'))

    # exception cases like color that has another unit within it.
    # variants variants-swatches
    #for div in element.findAll('div', {'class' : 'variants variants-swatches'}):
    for div in element.findAll('div', {'class': 'variant-name'}):
            values.append(div.text)

    result = {'type' : type,
              'values' : values}
    return result

def parse_department_facet_list(element):
    #print('parsing ----> ', element.get('class'))
    pass

def get_form_element_info(class_name, form_element):
    print(class_name)
    print(form_element)

def get_facets_bar(facet_html_element):
    return facet_html_element.findAll('div', {'class' : 'facets-bar'})

def get_facets(item=None):
    # BASE CASE
    if not item: return None

    # get url of the ui that needs to be parsed
    url = get_ui_url(WALMART_UI_URL, {'query' : item})

    # get web page
    web_page = get_web_page(url)

    # get the facets in the page by parsing the page
    facets = get_facets_in_webpage(web_page)
    return facets

