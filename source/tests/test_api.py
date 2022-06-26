import pytest
from source.helpers.work_with_api import API
from source.data.data_expected_bodies import DATA_FOR_GET_CHARACTER_BY_NAME, DATA_FOR_POST_CHARACTER_BY_BODY


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
