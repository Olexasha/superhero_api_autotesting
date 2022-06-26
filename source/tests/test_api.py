import pytest
from source.helpers.work_with_api import API
from source.data.data_expected_bodies import DATA_FOR_POST_CHARACTER_BY_BODY, DATA_CHANGED_NAME_FOR_PUT
from source.data.data_headers import HEADERS


class TestAPI(object):

    @pytest.mark.parametrize('data', DATA_FOR_POST_CHARACTER_BY_BODY)
    def test_get_character_by_name(self, data, cmdopt, cmdopt2, create_several_characters, delete_several_characters):
        response = API().get_character_by_name(raw_character_name=data["name"],
                                               login=cmdopt, password=cmdopt2)
        assert response.compare_status_code(200)
        assert response.compare_body({"result": data})

    @pytest.mark.parametrize('data', DATA_FOR_POST_CHARACTER_BY_BODY)
    def test_create_character(self, data, cmdopt, cmdopt2, delete_several_characters):
        response = API().post_character_by_body(json=data, login=cmdopt, password=cmdopt2)
        assert response.compare_status_code(200)
        assert response.compare_body({"result": data})
        response = API().get_character_by_name(raw_character_name=data["name"], login=cmdopt, password=cmdopt2)
        assert response.compare_status_code(200)
        assert response.compare_body({"result": data})

    @pytest.mark.parametrize('data', DATA_FOR_POST_CHARACTER_BY_BODY)
    def test_delete_character_by_name(self, data, cmdopt, cmdopt2, create_several_characters):
        response = API().delete_character(raw_character_name=data["name"], login=cmdopt, password=cmdopt2)
        deleted_hero = {"result": "Hero {0} is deleted".format(data["name"])}
        assert response.compare_status_code(200)
        assert response.compare_body(deleted_hero)

    def test_headers_field(self, cmdopt, cmdopt2):
        response = API().head_characters_page(login=cmdopt, password=cmdopt2)
        assert response.compare_status_code(200)
        headers = response.compare_headers()
        for key in headers.keys():
            match key:
                case "Server":
                    assert headers[key] == "nginx"
                case "Date":
                    assert headers[key] != '' and headers[key] != ' '
                case "Content-Type":
                    assert headers[key] == HEADERS["Content-Type"]
                case "Content-Length":
                    assert int(headers[key]) > 3000
                case "Connection":
                    assert headers[key] == HEADERS["Connection"]

    @pytest.mark.parametrize('data', DATA_CHANGED_NAME_FOR_PUT)
    def test_update_character_identity_by_name(self, data, cmdopt, cmdopt2, create_n_del_character_for_put):
        response = API().put_character_by_name(json=data["result"],
                                               login=cmdopt, password=cmdopt2)
        assert response.compare_status_code(200)
        assert response.compare_body(data)
        response = API().get_character_by_name(raw_character_name=data["result"]["name"],
                                               login=cmdopt, password=cmdopt2)
        assert response.compare_status_code(200)
        assert response.compare_body(data)

    @pytest.mark.parametrize('count_of_rerun', range(3))
    def test_get_all_characters(self, cmdopt, cmdopt2, count_of_rerun, create_n_del_character_for_put):
        response = API().get_all_characters(login=cmdopt, password=cmdopt2)
        assert response.compare_status_code(200)
        assert response.count_all_characters() >= 1
