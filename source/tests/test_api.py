import pytest
from copy import deepcopy
from source.helpers.work_with_api import API
from source.helpers.work_with_fields import WorkCharacters
from source.data.data_expected_bodies import DATA_FOR_POST_CHARACTER_BY_BODY, DATA_CHANGED_NAME_FOR_PUT, \
    MIN_LENGTH_FIELD, WRONG_ORDER_OF_FIELDS, WRONG_ORDER_OF_FIELDS_EXPECTED, MISSING_REQUIRED_FIELD, \
    DATA_STANDARD_CHARACTER
from source.data.data_expected_responses import RESPONSE_NEEDED_AUTHORIZATION, RESPONSE_SLICE_LOGIN, \
    RESPONSE_INVALID_POST_JSON, RESPONSE_MISSING_REQUIRED_FIELD, RESPONSE_FIELD_LENGTH_ERROR, RESPONSE_INVALID_INPUT, \
    RESPONSE_NO_SUCH_NAME_CHARACTER
from source.data.data_headers import HEADERS


# TODO:
# 1. Через match-case проверить поля у всех героев
#    1.1. Чисел после , не более 2
#    1.2. ? Рост-вес не больше/меньше адекватных
#    1.3. Проверка на такие штуки: "a href=", "\"...
#    1.4. ? Кириллица
# 2. Заполнить БД до 500 объектов (макс)
# 3. Ресетнуть БД
# 4. Задание полям другие типы данных
# 5. ? Узнать максимум чисел после запятой

class TestAPI(object):
    """
    Class to run tests by pytest
    """

    @pytest.mark.test_http_functional
    @pytest.mark.parametrize('data', DATA_FOR_POST_CHARACTER_BY_BODY)
    def test_get_character_by_name(self, data, login_auth, password_auth, create_several_characters,
                                   delete_several_characters):
        """
        Tests GET objects three times
        :param data: payload
        :param create_several_characters: setup fixture
        :param delete_several_characters: teardown fixture
        """
        response = API().get_character_by_name(raw_character_name=data["name"],
                                               login=login_auth, password=password_auth)
        assert response.compare_status_code(200)
        assert response.compare_body({"result": data})

    @pytest.mark.test_http_functional
    @pytest.mark.parametrize('data', DATA_FOR_POST_CHARACTER_BY_BODY)
    def test_create_character(self, data, login_auth, password_auth, delete_several_characters):
        """
        Tests POST objects three times
        :param data: payload
        :param delete_several_characters: teardown fixture
        """
        response = API().post_character_by_body(json=data, login=login_auth, password=password_auth)
        assert response.compare_status_code(200)
        assert response.compare_body({"result": data})
        response = API().get_character_by_name(raw_character_name=data["name"], login=login_auth,
                                               password=password_auth)
        assert response.compare_status_code(200)
        assert response.compare_body({"result": data})

    @pytest.mark.test_http_functional
    @pytest.mark.parametrize('data', DATA_FOR_POST_CHARACTER_BY_BODY)
    def test_delete_character_by_name(self, data, login_auth, password_auth, create_several_characters):
        """
        Tests DELETE objects three times
        :param data: payload
        :param create_several_characters: setup fixture
        """
        response = API().delete_character(raw_character_name=data["name"], login=login_auth, password=password_auth)
        deleted_hero = {"result": "Hero {0} is deleted".format(data["name"])}
        assert response.compare_status_code(200)
        assert response.compare_body(deleted_hero)

    @pytest.mark.test_objects_api
    def test_headers_field(self, login_auth, password_auth):
        """
        Check headers fields by GET method
        """
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
                    assert int(headers[key]) > 0
                case "Connection":
                    assert headers[key] == HEADERS["Connection"]

    @pytest.mark.test_http_functional
    @pytest.mark.parametrize('data', DATA_CHANGED_NAME_FOR_PUT)
    def test_update_character_identity_by_name(self, data, login_auth, password_auth, create_n_del_character):
        """
        Test PUT object
        :param data: payload
        :param create_n_del_character_for_put: setup and teardown fixture
        """
        response = API().put_character_by_name(json=data["result"],
                                               login=login_auth, password=password_auth)
        assert response.compare_status_code(200)
        assert response.compare_body(data)
        response = API().get_character_by_name(raw_character_name=data["result"]["name"],
                                               login=login_auth, password=password_auth)
        assert response.compare_status_code(200)
        assert response.compare_body(data)

    @pytest.mark.test_http_functional
    def test_get_all_characters(self, login_auth, password_auth, delete_3_characters_same_time):
        """
        Tests GET all objects. The status is checked before the creation of 3 characters and after
        :param create_3_characters: setup and teardown fixture
        """
        response = API().get_all_characters(login=login_auth, password=password_auth)
        assert response.compare_status_code(200)
        characters_before = response.count_all_characters()
        characters_after = WorkCharacters().count_after_create_chars(login=login_auth, password=password_auth)
        assert characters_before + 3 == characters_after

    @pytest.mark.test_objects_api
    def test_get_all_duplicate_chars(self, login_auth, password_auth):
        """
        Tests for the presence of duplicate characters
        """
        response = API().get_all_characters(login=login_auth, password=password_auth)
        assert response.compare_status_code(200)
        assert WorkCharacters().find_duplicate_characters(response.return_body())

    @pytest.mark.test_negative_cases
    def test_wrong_authorization(self, login_auth, password_auth):
        """
        Tests wrong authorization data in advance
        """
        response = API().get_all_characters(login=login_auth, password='dc_better_than_marvel')
        assert response.compare_status_code(401)
        assert response.compare_body(RESPONSE_NEEDED_AUTHORIZATION)
        response = API().get_all_characters(login=' ', password=password_auth)
        assert response.compare_status_code(401)
        assert response.compare_body(RESPONSE_NEEDED_AUTHORIZATION)

    @pytest.mark.test_negative_cases
    def test_empty_login(self, login_auth, password_auth):
        """
        Tests wrong authorization by empty field
        """
        response = API().get_all_characters(login='', password=password_auth)
        assert response.compare_status_code(500)
        assert response.compare_raw_text(RESPONSE_SLICE_LOGIN)

    @pytest.mark.test_negative_cases
    def test_wrong_order_of_field(self, login_auth, password_auth, double_delete_character):
        """
        Tests POST method with wrong fields order
        :param double_delete_character: setup and teardown fixture
        """
        response = API().post_character_by_body(json=WRONG_ORDER_OF_FIELDS["result"],
                                                login=login_auth, password=password_auth)
        assert response.compare_status_code(200)
        assert response.compare_body(WRONG_ORDER_OF_FIELDS_EXPECTED)

    @pytest.mark.test_negative_cases
    def test_delete_deleted_char(self, login_auth, password_auth):
        """
        Tests the correctness of the return body when DELETE a character 'Anyone' that does not exist
        """
        response = API().delete_character(raw_character_name="Anyone", login=login_auth, password=password_auth)
        assert response.compare_status_code(400)
        assert response.compare_body(RESPONSE_NO_SUCH_NAME_CHARACTER)

    @pytest.mark.test_negative_cases
    def test_create_existing_char(self, login_auth, password_auth, create_n_del_character):
        """
        Tests the correctness of the return body when POST an existing 'Spider-Man' character
        :param create_n_del_character: setup and teardown fixture
        """
        response = API().post_character_by_body(json=DATA_FOR_POST_CHARACTER_BY_BODY[1], login=login_auth,
                                                password=password_auth)
        assert response.compare_status_code(400)
        existing_hero = {"error": "Spider-Man is already exists"}
        assert response.compare_body(existing_hero)

    @pytest.mark.test_negative_cases
    def test_get_not_existing_char(self, login_auth, password_auth):
        """
        Tests the correctness of the body return when GET a non-existent 'Anyone' character
        """
        response = API().get_character_by_name(raw_character_name="Anyone",
                                               login=login_auth, password=password_auth)
        assert response.compare_status_code(400)
        nonexistent_hero = {"error": "No such name"}
        assert response.compare_body(nonexistent_hero)

    @pytest.mark.test_objects_api
    def test_post_wrong_input(self, login_auth, password_auth):
        """
        Tests the POST wrong input data
        """
        data = deepcopy(MIN_LENGTH_FIELD["result"])
        payload = data.pop("name")
        response = API().post_character_by_body(json=payload, login=login_auth,
                                                password=password_auth)
        assert response.compare_status_code(400)
        assert response.compare_body(RESPONSE_INVALID_INPUT)

    @pytest.mark.test_objects_api
    def test_post_missing_required_field(self, login_auth, password_auth):
        """
        Tests the empty value of required field 'name'
        """
        response = API().post_character_by_body(json=MISSING_REQUIRED_FIELD, login=login_auth,
                                                password=password_auth)
        assert response.compare_status_code(400)
        assert response.compare_body(RESPONSE_MISSING_REQUIRED_FIELD)

    @pytest.mark.test_objects_api
    def test_post_min_field_positive(self, login_auth, password_auth, reset_database_after):
        """
        Tests the minimum symbols length of the field
        """
        data = deepcopy(MIN_LENGTH_FIELD)
        payload = WorkCharacters().make_field_symbols(data["result"], 1)
        response = API().post_character_by_body(json=payload, login=login_auth, password=password_auth)
        assert response.compare_status_code(200)
        assert response.compare_body({"result": payload})

    @pytest.mark.test_objects_api
    def test_post_max_field_positive(self, login_auth, password_auth, reset_database_after):
        """
        Tests the maximum symbols length of the field
        """
        data = deepcopy(MIN_LENGTH_FIELD)
        payload = WorkCharacters().make_field_symbols(data["result"], 350)
        response = API().post_character_by_body(json=payload, login=login_auth, password=password_auth)
        assert response.compare_status_code(200)
        assert response.compare_body({"result": payload})

    @pytest.mark.test_negative_cases
    def test_post_min_field_negative(self, login_auth, password_auth, reset_database_after):
        """
        Tests the minimum symbols length of the field
        """
        data = deepcopy(MIN_LENGTH_FIELD)
        payload = WorkCharacters().make_field_symbols(data["result"], 0)
        response = API().post_character_by_body(json=payload, login=login_auth, password=password_auth)
        assert response.compare_status_code(400)
        assert response.compare_body(RESPONSE_FIELD_LENGTH_ERROR)

    @pytest.mark.test_negative_cases
    def test_post_max_field_negative(self, login_auth, password_auth, reset_database_after):
        """
        Tests the maximum symbols length of the field
        """
        data = deepcopy(MIN_LENGTH_FIELD)
        payload = WorkCharacters().make_field_symbols(data["result"], 351)
        response = API().post_character_by_body(json=payload, login=login_auth, password=password_auth)
        assert response.compare_status_code(400)
        assert response.compare_body(RESPONSE_FIELD_LENGTH_ERROR)

    @pytest.mark.test_http_functional
    @pytest.mark.parametrize('data', DATA_STANDARD_CHARACTER)
    def test_reset_database(self, data, login_auth, password_auth, create_character):
        """
        Tests the correctness of database reseting
        :param data: standart character
        :param create_character: setup fixture which creates standart character
        """
        response = API().delete_all_characters(login_auth, password_auth)
        assert response.compare_status_code(200)
        response = API().get_character_by_name(raw_character_name=data["result"]["name"],
                                               login=login_auth, password=password_auth)
        assert response.compare_body(RESPONSE_NO_SUCH_NAME_CHARACTER)

    @pytest.mark.test_objects_api
    def test_get_fields_validate(self, login_auth, password_auth):
        """
        Tests the received character's fields with the JSON sample
        """
        response = API().get_all_characters(login=login_auth, password=password_auth)
        assert response.compare_status_code(200)
        assert WorkCharacters().validate_fields(response.return_body())

