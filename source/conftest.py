import pytest
from colorama import Style, init
from source.helpers.work_with_api import API
from source.data.data_expected_bodies import DATA_FOR_POST_CHARACTER_BY_BODY, DATA_CHANGED_NAME_FOR_PUT, \
    DATA_FOR_MANY_CHARS_MANIPULATIONS, WRONG_ORDER_OF_FIELDS_EXPECTED

init(autoreset=True)


# TODO: Make some cleaning with validation repeating. It hurts my eyes

def printing_fixture_setup_teardown(setup_or_teardown):
    print('\n' + '-' * 75)
    if setup_or_teardown == 'setup':
        print(f'{Style.BRIGHT}\tFixture\'s SetUp')
    else:
        print(f'{Style.BRIGHT}\tFixture\'s TearDown:')
    print('-' * 75)


def deleting_character(data, login_auth, password_auth):
    response = API().delete_character(raw_character_name=data["name"],
                                      login=login_auth, password=password_auth)
    if response.compare_status_code(200):
        validate_response = API().get_character_by_name(raw_character_name=data["name"],
                                                        login=login_auth,
                                                        password=password_auth)
        if not validate_response.compare_body({"error": "No such name"}):
            print('Characters were NOT deleted!')


def creating_character(data, login_auth, password_auth):
    response = API().post_character_by_body(json=data, login=login_auth, password=password_auth)
    if response.compare_status_code(200):
        validate_response = API().get_character_by_name(raw_character_name=data["name"], login=login_auth,
                                                        password=password_auth)
        if not validate_response.compare_status_code(200) or not validate_response.compare_body({"result": data}):
            print('Characters were NOT posted')


def pytest_addoption(parser):
    parser.addoption(
        "--login_auth", action="store", default=False, help="The login argument authorization",
    )
    parser.addoption(
        "--password_auth", action="store", default=False, help="The password argument authorization"
    )


@pytest.fixture()
def login_auth(request):
    return request.config.getoption("--login_auth")


@pytest.fixture()
def password_auth(request):
    return request.config.getoption("--password_auth")


@pytest.mark.parametrize('data', DATA_FOR_POST_CHARACTER_BY_BODY)
@pytest.fixture(scope="function")
def delete_several_characters(data, login_auth, password_auth):
    yield
    printing_fixture_setup_teardown('teardown')
    deleting_character(data, login_auth, password_auth)
    print('-' * 75)


@pytest.mark.parametrize('data', DATA_FOR_POST_CHARACTER_BY_BODY)
@pytest.fixture(scope="function")
def create_several_characters(data, login_auth, password_auth):
    printing_fixture_setup_teardown('setup')
    creating_character(data, login_auth, password_auth)
    print('-' * 75)
    yield


@pytest.fixture(scope="function")
def create_n_del_character_for_put(login_auth, password_auth):
    printing_fixture_setup_teardown('setup')
    data_unchanged = DATA_FOR_POST_CHARACTER_BY_BODY[1]
    creating_character(data_unchanged, login_auth, password_auth)
    print('-' * 75)
    yield
    printing_fixture_setup_teardown('teardown')
    data_changed = DATA_CHANGED_NAME_FOR_PUT[0]["result"]
    deleting_character(data_changed, login_auth, password_auth)
    print('-' * 75)


@pytest.fixture(scope="function")
def delete_3_characters_same_time(login_auth, password_auth):
    printing_fixture_setup_teardown('setup')
    for character in DATA_FOR_MANY_CHARS_MANIPULATIONS:
        response = API().delete_character(raw_character_name=character["result"]["name"], login=login_auth,
                                          password=password_auth)
        if response.compare_status_code(200):
            validate_response = API().get_character_by_name(raw_character_name=character["result"]["name"],
                                                            login=login_auth, password=password_auth)
            if not validate_response.compare_body({"error": "No such name"}):
                print('Characters were NOT deleted!')
    yield
    printing_fixture_setup_teardown('teardown')
    for character in DATA_FOR_MANY_CHARS_MANIPULATIONS:
        response = API().delete_character(raw_character_name=character["result"]["name"], login=login_auth,
                                          password=password_auth)
        if response.compare_status_code(200):
            validate_response = API().get_character_by_name(raw_character_name=character["result"]["name"],
                                                            login=login_auth, password=password_auth)
            if not validate_response.compare_body({"error": "No such name"}):
                print('Characters were NOT deleted!')
    print('-' * 75)


@pytest.fixture(scope="function")
def double_delete_character(login_auth, password_auth):
    printing_fixture_setup_teardown('setup')
    data = WRONG_ORDER_OF_FIELDS_EXPECTED["result"]
    deleting_character(data, login_auth, password_auth)
    print('-' * 75)
    yield
    printing_fixture_setup_teardown('teardown')
    deleting_character(data, login_auth, password_auth)
    print('-' * 75)
