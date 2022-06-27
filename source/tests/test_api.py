import pytest
from source.helpers.work_with_api import API
from source.helpers.work_with_fields import WorkCharacters
from source.data.data_expected_bodies import DATA_FOR_POST_CHARACTER_BY_BODY, DATA_CHANGED_NAME_FOR_PUT
from source.data.data_expected_responses import NEEDED_AUTHORIZATION, SLICE_LOGIN
from source.data.data_headers import HEADERS


class TestAPI(object):

    @pytest.mark.parametrize('data', DATA_FOR_POST_CHARACTER_BY_BODY)
    def test_get_character_by_name(self, data, login_auth, password_auth, create_several_characters,
                                   delete_several_characters):
        response = API().get_character_by_name(raw_character_name=data["name"],
                                               login=login_auth, password=password_auth)
        assert response.compare_status_code(200)
        assert response.compare_body({"result": data})

    @pytest.mark.parametrize('data', DATA_FOR_POST_CHARACTER_BY_BODY)
    def test_create_character(self, data, login_auth, password_auth, delete_several_characters):
        response = API().post_character_by_body(json=data, login=login_auth, password=password_auth)
        assert response.compare_status_code(200)
        assert response.compare_body({"result": data})
        response = API().get_character_by_name(raw_character_name=data["name"], login=login_auth,
                                               password=password_auth)
        assert response.compare_status_code(200)
        assert response.compare_body({"result": data})

    @pytest.mark.parametrize('data', DATA_FOR_POST_CHARACTER_BY_BODY)
    def test_delete_character_by_name(self, data, login_auth, password_auth, create_several_characters):
        response = API().delete_character(raw_character_name=data["name"], login=login_auth, password=password_auth)
        deleted_hero = {"result": "Hero {0} is deleted".format(data["name"])}
        assert response.compare_status_code(200)
        assert response.compare_body(deleted_hero)

    def test_headers_field(self, login_auth, password_auth):
        response = API().head_characters_page(login=login_auth, password=password_auth)
        assert response.compare_status_code(200)
        headers = response.return_headers()
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
    def test_update_character_identity_by_name(self, data, login_auth, password_auth, create_n_del_character_for_put):
        response = API().put_character_by_name(json=data["result"],
                                               login=login_auth, password=password_auth)
        assert response.compare_status_code(200)
        assert response.compare_body(data)
        response = API().get_character_by_name(raw_character_name=data["result"]["name"],
                                               login=login_auth, password=password_auth)
        assert response.compare_status_code(200)
        assert response.compare_body(data)

    def test_get_all_characters(self, login_auth, password_auth, create_3_characters):
        response = API().get_all_characters(login=login_auth, password=password_auth)
        assert response.compare_status_code(200)
        characters_before = response.count_all_characters()
        characters_after = WorkCharacters().count_after_create_chars(login=login_auth, password=password_auth)
        assert characters_before + 3 == characters_after

    def test_get_all_duplicate_chars(self, login_auth, password_auth):
        response = API().get_all_characters(login=login_auth, password=password_auth)
        assert response.compare_status_code(200)
        assert WorkCharacters().find_duplicate_characters(response.return_body())

    def test_wrong_authorization(self, login_auth, password_auth):
        response = API().get_all_characters(login=login_auth, password='dc_better_than_marvel')
        assert response.compare_status_code(401)
        assert response.compare_body(NEEDED_AUTHORIZATION)
        response = API().get_all_characters(login=' ', password=password_auth)
        assert response.compare_status_code(401)
        assert response.compare_body(NEEDED_AUTHORIZATION)

    def test_empty_login(self, login_auth, password_auth):
        response = API().get_all_characters(login='', password=password_auth)
        assert response.compare_status_code(500)
        assert response.compare_raw_text(SLICE_LOGIN)
