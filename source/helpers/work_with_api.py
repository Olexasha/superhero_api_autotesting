import requests
from source import configuration
from source.helpers.work_with_asserting_respose import ParseResponse as Results
from source.data.data_headers import HEADERS


class API(object):
    def __init__(self):
        self.login = configuration.api_auth_login
        self.password = configuration.api_auth_pass
        self.raw_url = 'http://rest.test.ivi.ru/v2/character'

    def get_request(self, *args, **kwargs):
        return Results(requests.get(*args, **kwargs))

    def post_request(self, *args, **kwargs):
        return Results(requests.post(*args, **kwargs))

    def delete_request(self, *args, **kwargs):
        return Results(requests.delete(*args, **kwargs))

    def put_request(self, *args, **kwargs):
        return Results(requests.put(*args, **kwargs))

    def head_request(self, *args, **kwargs):
        return Results(requests.head(*args, **kwargs))

    def get_character_by_name(self, character_name):
        request_url = self.raw_url + '?name=' + character_name
        return self.get_request(url=request_url, headers=HEADERS, auth=(self.login, self.password))
