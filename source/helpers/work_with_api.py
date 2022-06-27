import requests
from source.helpers.work_with_asserting_respose import ParseResponse as Results
from source.data.data_headers import HEADERS


class API(object):
    """
    Class describes working with API
    """
    def __init__(self):
        self.raw_url = 'http://rest.test.ivi.ru/v2/character'

    def make_url(self, raw_character_name):
        """
        Replaces spaces with a valid symbol
        :param raw_character_name: raw variant of character's name
        :return: legal character's name
        """
        character_name = raw_character_name.replace(' ', '+')
        return self.raw_url + '?name=' + character_name

    def get_request(self, *args, **kwargs):
        """
        Make GET request
        :return: Calls the 'ParseResponse' class to handle HTTP data
        """
        return Results(requests.get(*args, **kwargs))

    def post_request(self, *args, **kwargs):
        """
        Make POST request
        :return: Calls the 'ParseResponse' class to handle HTTP data
        """
        return Results(requests.post(*args, **kwargs))

    def delete_request(self, *args, **kwargs):
        """
        Make DELETE request
        :return: Calls the 'ParseResponse' class to handle HTTP data
        """
        return Results(requests.delete(*args, **kwargs))

    def put_request(self, *args, **kwargs):
        """
        Make PUT request
        :return: Calls the 'ParseResponse' class to handle HTTP data
        """
        return Results(requests.put(*args, **kwargs))

    def head_request(self, *args, **kwargs):
        """
        Make HEAD request
        :return: Calls the 'ParseResponse' class to handle HTTP data
        """
        return Results(requests.head(*args, **kwargs))

    def get_character_by_name(self, raw_character_name, login, password):
        """
        Forms GET request
        :return: Ready-made request
        """
        request_url = self.make_url(raw_character_name=raw_character_name)
        return self.get_request(url=request_url, headers=HEADERS, auth=(login, password))

    def post_character_by_body(self, login, password, *args, **kwargs):
        """
        Forms POST request
        :return: Ready-made request
        """
        return self.post_request(url=self.raw_url, headers=HEADERS, auth=(login, password), *args, **kwargs)

    def delete_character(self, raw_character_name, login, password):
        """
        Forms DELETE request
        :return: Ready-made request
        """
        request_url = self.make_url(raw_character_name=raw_character_name)
        return self.delete_request(url=request_url, headers=HEADERS, auth=(login, password))

    def head_characters_page(self, login, password):
        """
        Forms HEAD request
        :return: Ready-made request
        """
        request_url = self.raw_url + 's'
        return self.head_request(url=request_url, headers=HEADERS, auth=(login, password))

    def put_character_by_name(self, login, password, *args, **kwargs):
        """
        Forms PUT request
        :return: Ready-made request
        """
        return self.put_request(url=self.raw_url, headers=HEADERS, auth=(login, password), *args, **kwargs)

    def get_all_characters(self, login, password):
        """
        Forms GET request for all characters
        :return: Ready-made request
        """
        request_url = self.raw_url + 's'
        return self.get_request(url=request_url, headers=HEADERS, auth=(login, password))

