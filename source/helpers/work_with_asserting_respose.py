from colorama import Style, init
from json.decoder import JSONDecodeError


class ParseResponse(object):
    def __init__(self, response):
        try:
            print(f'Data of executed request:\n    Request Method: {response.request.method};'
                  f'\n    Got Status Code: {response.status_code};'
                  f'\n    Callable URL: {response.request.url};'
                  f'\n    Got Headers: {response.headers};'
                  f'\n    Got Body: {response.text}')
            self.status_code = response.status_code
            self.headers = response.headers
            self.body = response.json()
            init(autoreset=True)
        except JSONDecodeError:
            print('I\'ve got not JSON type!')

    def compare_status_code(self, expected_status_code):
        print(f'{Style.BRIGHT}Check if the expected status code: \"{expected_status_code}\" '
              f'is equal to the actual code: \"{self.status_code}\"')
        return self.status_code == expected_status_code

    def compare_body(self, expected_body):
        print(f'{Style.BRIGHT}Check if the expected body: '
              f'\n\t\t\"{expected_body}\" '
              f'\n\tis equal to the actual body: '
              f'\n\t\t\"{self.body}\"')
        return self.body == expected_body

    def compare_headers(self):
        print(self.headers)
        return self.headers
