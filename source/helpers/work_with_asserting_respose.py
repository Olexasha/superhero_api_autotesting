import allure
from colorama import Style, init
from json.decoder import JSONDecodeError


class ParseResponse(object):
    """
    Class works with the obtained values
    """
    def __init__(self, response):
        """
        Dividing the answer into components
        :param response: HTTP answer
        """
        try:
            print(f'Data of executed request:\n    Request Method: {response.request.method};'
                  f'\n    Got Status Code: {response.status_code};'
                  f'\n    Callable URL: {response.request.url};'
                  f'\n    Got Headers: {response.headers};'
                  f'\n    Got Body: {response.text}')
            self.status_code = response.status_code
            self.headers = response.headers
            self.text = response.text
            self.body = response.json()
            init(autoreset=True)
        except JSONDecodeError:
            print('I\'ve got not JSON type!')

    @allure.step("fafaf = {expected_status_code}")
    def compare_status_code(self, expected_status_code: int) -> bool:
        """
        HTTP code status comparison
        :param expected_status_code: expected code
        :return: bool value
        """
        print(f'{Style.BRIGHT}Check if the expected status code: \"{expected_status_code}\" '
              f'is equal to the actual code: \"{self.status_code}\"')
        return self.status_code == expected_status_code

    def compare_body(self, expected_body: dict) -> bool:
        """
        HTTP JSON body comparison
        :param expected_body: expected body
        :return: bool value
        """
        print(f'{Style.BRIGHT}Check if the expected body: '
              f'\n\t\t\"{expected_body}\" '
              f'\n\tis equal to the actual body: '
              f'\n\t\t\"{self.body}\"')
        return self.body == expected_body

    def compare_raw_text(self, expected_text: str) -> bool:
        """
        HTTP raw body comparison
        :param expected_text: expected text
        :return: bool value
        """
        print(f'{Style.BRIGHT}Check if the expected text: '
              f'\n\t\t\"{expected_text}\" '
              f'\n\tis equal to the actual text: '
              f'\n\t\t\"{self.text}\"')
        return self.text == expected_text

    def return_headers(self) -> dict:
        """
        :return: HTTP headers
        """
        return self.headers

    def return_body(self) -> dict:
        """
        :return: HTTP JSON body
        """
        return self.body["result"]

    def count_all_characters(self) -> int:
        """
        :return: Count of all characters
        """
        print(f'{Style.BRIGHT}\n\t  The current number of characters in the database: {len(self.body["result"])}')
        return len(self.body["result"])

