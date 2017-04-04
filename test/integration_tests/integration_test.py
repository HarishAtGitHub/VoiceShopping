import requests, json

# code from: http://stackoverflow.com/a/25851972/1597944
def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj

def dict_compare(d1, d2):
    return ordered(d1) == ordered(d2)

def run_api_test(url, httpMethod, data, expected_output):
    headers = {"Content-Type" : "application/json"}
    expected_output = eval(expected_output)
    if httpMethod == "POST":
        response = requests.post(url, data=json.dumps(data), headers = headers)
    if response.status_code == 200:
        output = response.json()
        result = dict_compare(output, expected_output)
        if not result:
            print("API URL {} Test failed due to mismatch in expected output".format(url))
        else:
            print("API URL {} Test passed".format(url))
    else:
        print("API URL {} Test failed due to non 200 status response ".format(url))
    
if __name__ == "__main__":
    with open("test_input.json") as f:
        tests = json.loads(f.read())
    for test in tests:
        run_api_test(test['url'], test['httpMethod'], test['requestBody'], test['responseBody'])
