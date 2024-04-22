from functools import wraps
import re

def _extract_element_content(element_string):
    match = re.search(r'{\n(.*?)\n}', element_string, re.DOTALL)
    if not match:
        return []

    content = match.group(1)
    results = re.findall(r'"(.*?)"', content)
    results = list(map(lambda x:x.upper(), results))

    return results

def log(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        request = func(self, *args, **kwargs)

        types = args[0]
        tickers = _extract_element_content(request.asElement()['securities'].toString())
        fields = _extract_element_content(request.asElement()['fields'].toString())
        self.log_request(types, tickers, fields)

        return request

    return wrapper
