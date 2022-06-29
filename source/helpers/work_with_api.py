import requests
import allure
from source.helpers.work_with_asserting_respose import ParseResponse as Results
from source.data.data_headers import HEADERS


@allure.title('Общение с API')
class API(object):
    """
    Class describes working with API
    """
    def __init__(self):
        self.raw_url = 'http://rest.test.ivi.ru/v2/character'

    @allure.step('Создание URL для 1 персонажа')
    def make_url(self, raw_character_name):
        """
        Replaces spaces with a valid symbol
        :param raw_character_name: raw variant of character's name
        :return: legal character's name
        """
        character_name = raw_character_name.replace(' ', '+')
        return self.raw_url + '?name=' + character_name

    @allure.step('Выполнение GET-запроса')
    def get_request(self, *args, **kwargs):
        """
        Make GET request
        :return: Calls the 'ParseResponse' class to handle HTTP data
        """
        return Results(requests.get(*args, **kwargs))

    @allure.step('Выполнение POST-запроса')
    def post_request(self, *args, **kwargs):
        """
        Make POST request
        :return: Calls the 'ParseResponse' class to handle HTTP data
        """
        return Results(requests.post(*args, **kwargs))

    @allure.step('Выполнение DELETE-запроса')
    def delete_request(self, *args, **kwargs):
        """
        Make DELETE request
        :return: Calls the 'ParseResponse' class to handle HTTP data
        """
        return Results(requests.delete(*args, **kwargs))

    @allure.step('Выполнение PUT-запроса')
    def put_request(self, *args, **kwargs):
        """
        Make PUT request
        :return: Calls the 'ParseResponse' class to handle HTTP data
        """
        return Results(requests.put(*args, **kwargs))

    @allure.step('Выполнение HEAD-запроса')
    def head_request(self, *args, **kwargs):
        """
        Make HEAD request
        :return: Calls the 'ParseResponse' class to handle HTTP data
        """
        return Results(requests.head(*args, **kwargs))

    @allure.step('Формирование GET-запроса 1 персонажа')
    def get_character_by_name(self, raw_character_name, login, password):
        """
        Forms GET request
        :return: Ready-made request
        """
        request_url = self.make_url(raw_character_name=raw_character_name)
        return self.get_request(url=request_url, headers=HEADERS, auth=(login, password))

    @allure.step('Формирование POST-запроса 1 персонажа')
    def post_character_by_body(self, login, password, *args, **kwargs):
        """
        Forms POST request
        :return: Ready-made request
        """
        return self.post_request(url=self.raw_url, headers=HEADERS, auth=(login, password), *args, **kwargs)

    @allure.step('Формирование DELETE-запроса 1 персонажа')
    def delete_character(self, raw_character_name, login, password):
        """
        Forms DELETE request
        :return: Ready-made request
        """
        request_url = self.make_url(raw_character_name=raw_character_name)
        return self.delete_request(url=request_url, headers=HEADERS, auth=(login, password))

    @allure.step('Формирование HEAD-запроса')
    def head_characters_page(self, login, password):
        """
        Forms HEAD request
        :return: Ready-made request
        """
        request_url = self.raw_url + 's'
        return self.head_request(url=request_url, headers=HEADERS, auth=(login, password))

    @allure.step('Формирование PUT-запроса 1 персонажа')
    def put_character_by_name(self, login, password, *args, **kwargs):
        """
        Forms PUT request
        :return: Ready-made request
        """
        return self.put_request(url=self.raw_url, headers=HEADERS, auth=(login, password), *args, **kwargs)

    @allure.step('Формирование GET-запроса всех персонажа')
    def get_all_characters(self, login, password):
        """
        Forms GET request for all characters
        :return: Ready-made request
        """
        request_url = self.raw_url + 's'
        return self.get_request(url=request_url, headers=HEADERS, auth=(login, password))

    @allure.step('Формирование DELETE-запроса всех персонажей')
    def delete_all_characters(self, login, password):
        """
        Resets DB characters to default
        :return: Ready-made request
        """
        request_url = 'http://rest.test.ivi.ru/v2/reset'
        return self.post_request(url=request_url, headers=HEADERS, auth=(login, password))

    @allure.step('Формирование GET-запроса с есуществующbv URL')
    def get_wrong_url_resource(self, login, password):
        """
        Tries to get non-existed resource for testing code 404
        :return: Ready-made request
        """
        request_url = 'http://rest.test.ivi.ru/v2/character/unexpected'
        return self.get_request(url=request_url, headers=HEADERS, auth=(login, password))
