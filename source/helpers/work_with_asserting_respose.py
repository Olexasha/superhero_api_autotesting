from json.decoder import JSONDecodeError


class ParseResponse(object):
    def __init__(self, response):
        try:
            print(f'Data of executed request:\n    Request Method: {response.request.method};'
                  f'\n    Got Status Code: {response.status_code};'
                  f'\n    Called URL: {response.request.url};'
                  f'\n    Got Body: {response.text}')
            self.status_code = response.status_code
            self.body = response.json()
        except JSONDecodeError:
            print('I\'ve got not JSON type!')

    def compare_status_code(self, expected_status_code):
        print(f'Check if the expected status code: \"{expected_status_code}\" '
              f'is equal to the actual code: \"{self.status_code}\"')
        return self.status_code == expected_status_code

    def compare_body(self, expected_body):
        print(f'Check if the expected body: \"{expected_body}\" '
              f'is equal to the actual body: \"{self.body}\"')
        return self.body == expected_body
