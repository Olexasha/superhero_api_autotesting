import pytest
from colorama import Style, init
from source.helpers.work_with_api import API
from source.data.data_expected_bodies import DATA_FOR_GET_CHARACTER_BY_NAME, DATA_FOR_POST_CHARACTER_BY_BODY

init(autoreset=True)


# TODO: See the notation in test_api.py

def pytest_addoption(parser):
    parser.addoption(
        "--login_auth", action="store", default=False, help="The login argument authorization",
    )
    parser.addoption(
        "--password_auth", action="store", default=False, help="The password argument authorization"
    )


@pytest.fixture()
def cmdopt(request):
    return request.config.getoption("--login_auth")


@pytest.fixture()
def cmdopt2(request):
    return request.config.getoption("--password_auth")


@pytest.mark.parametrize('data', DATA_FOR_POST_CHARACTER_BY_BODY)
@pytest.fixture(scope="function")
def delete_several_characters(data, cmdopt, cmdopt2):
    yield
    print(f'{Style.BRIGHT}\n\tFixture\'s TearDown:')
    print('-' * 75)
    response = API().delete_character(raw_character_name=data["name"], login=cmdopt, password=cmdopt2)
    if response.compare_status_code(200):
        validate_response = API().get_character_by_name(raw_character_name=data["name"], login=cmdopt, password=cmdopt2)
        if not validate_response.compare_body({"error": "No such name"}):
            print('Characters were NOT deleted!')
    print('-' * 75)


@pytest.mark.parametrize('data', DATA_FOR_POST_CHARACTER_BY_BODY)
@pytest.fixture(scope="function")
def create_several_characters(data, cmdopt, cmdopt2):
    print(f'{Style.BRIGHT}\n\tFixture\'s SetUp')
    print('-' * 75)
    response = API().post_character_by_body(json=data, login=cmdopt, password=cmdopt2)
    if response.compare_status_code(200):
        validate_response = API().get_character_by_name(raw_character_name=data["name"], login=cmdopt, password=cmdopt2)
        if not validate_response.compare_status_code(200) or not validate_response.compare_body({"result": data}):
            print('Characters were NOT posted')
    print('-' * 75)
    yield




