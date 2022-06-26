import pytest
from source.helpers.work_with_api import API
from source.data.data_expected_bodies import DATA_FOR_GET_CHARACTER_BY_NAME, DATA_FOR_POST_CHARACTER_BY_BODY


# from source.data.data_expected_responses import STDOUT_DELETED_CHARACTER

# TODO: GET, POST, DEL, PUT just for only 3 save objects (NOT DIFFERENT)!
class TestAPI(object):

    @pytest.mark.parametrize('data', DATA_FOR_GET_CHARACTER_BY_NAME)
    def test_get_character_by_name(self, data):
        response = API().get_character_by_name(raw_character_name=data["result"]["name"])
        assert response.compare_status_code(200)
        assert response.compare_body(data)

    @pytest.mark.parametrize('data', DATA_FOR_POST_CHARACTER_BY_BODY)
    def test_post_character_by_name(self, data):
        response = API().post_character_by_body(json=data)
        assert response.compare_status_code(200)
        assert response.compare_body({"result": data})
        response = API().get_character_by_name(raw_character_name=data["name"])
        assert response.compare_status_code(200)
        assert response.compare_body({"result": data})

    @pytest.mark.parametrize('data', DATA_FOR_POST_CHARACTER_BY_BODY)
    def test_delete_character_by_name(self, data):
        response = API().delete_character(raw_character_name=data["name"])
        deleted_hero = {"result": "Hero {0} is deleted".format(data["name"])}
        assert response.compare_status_code(200)
        assert response.compare_body(deleted_hero)
