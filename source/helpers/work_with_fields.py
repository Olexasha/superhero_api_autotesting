from source.helpers.work_with_api import API
from source.data.data_expected_bodies import DATA_FOR_POST_CHARACTER_BY_BODY, DATA_CHANGED_NAME_FOR_PUT, \
    DATA_FOR_MANY_CHARS_MANIPULATIONS


class WorkCharacters(object):

    def count_after_create_chars(self, login, password):
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
