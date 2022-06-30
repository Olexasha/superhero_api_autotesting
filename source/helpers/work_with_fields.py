import allure
from jsonschema import validate, ValidationError
from colorama import Style
from source.helpers.work_with_api import API
from source.data.data_expected_bodies import DATA_FOR_MANY_CHARS_MANIPULATIONS


@allure.title('Логика работы с экземплярами персонажей')
class WorkCharacters(object):

    @allure.step('Подсчёт количество персонажей после добавления новых')
    def count_after_create_chars(self, login: str, password: str) -> int:
        """
        Counts the number of all characters before creating new ones. Some validates also
        :param login: login auth
        :param password: password auth
        :return: call the method of counting all characters by response
        """
        for character in DATA_FOR_MANY_CHARS_MANIPULATIONS:
            response = API().post_character_by_body(json=character["result"], login=login, password=password)
            if response.compare_status_code(200):
                validate_response = API().get_character_by_name(raw_character_name=character["result"]["name"],
                                                                login=login, password=password)
                if not validate_response.compare_status_code(200) or \
                        not validate_response.compare_body(character):
                    assert False, print('Characters were NOT posted')
        response = API().get_all_characters(login=login, password=password)
        return response.count_all_characters()

    @allure.step('Поиск одинаковых экземпляров персонажей')
    def find_duplicate_characters(self, payload: dict) -> bool:
        """
        Looks for the same characters and adds them to the 'duplicates'. 'duplicates' specifies the character
        to be repeated and the number of repetitions
        :param payload: payload
        :return: bool value
        """
        print(f'\n\t  The current number of characters in the database: {len(payload)}')
        counter = {}
        for character_fields in payload:
            counter[character_fields["name"]] = counter.get(character_fields["name"], 0) + 1
        duplicates = {element: count for element, count in counter.items() if count > 1}
        if duplicates != {}:
            print(f'{Style.BRIGHT}\n\tThere is a recurring character in the database '
                  f'(key: character, value: count of repeats): {duplicates}')
            return False

    @allure.step('Задание длины string полей')
    def make_field_symbols(self, payload: dict, count_of_symbols: int) -> dict:
        """
        Generates the desired number of field elements
        :param payload: character fields
        :param count_of_symbols: needed count of symbols
        :return: dict (data for POST method)
        """
        for field in payload:
            if field == "height" or field == "weight":
                payload[field] = 1.0
            else:
                payload[field] = '9' * count_of_symbols
        return payload

    @staticmethod
    @allure.step('Валидация полей')
    def validate_fields(payload: dict | list, schema: dict) -> bool:
        """
        Compares the received characters fields with the sample 'SCHEMA'
        :param schema: schema sample for validation
        :param payload: character fields
        :return: bool value
        """
        try:
            if isinstance(payload, list):
                # bad_cases = {}
                for character_fields in payload:
                    validate(instance=character_fields, schema=schema)
            else:
                validate(instance=payload, schema=schema)
            return True
        except ValidationError as err:
            allure.attach(body=err, name='validation_stderr', attachment_type=allure.attachment_type.TEXT)
            # raw_error_msg = (str(err)).split()
            # parsed_key, value = raw_error_msg[-2], raw_error_msg[-1]
            # key = parsed_key.split("[")[-1].split("]")[0].split("\'")[1]
            # bad_cases.update({character_fields["name"]: {key: value}})
            raise err
