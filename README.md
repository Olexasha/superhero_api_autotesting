# README
### Представленный сценарий является фреймворком для автотестирования API. ###

#### Автотесты покрывают следующие кейсы: 
1. Вызовы GET, POST, DELETE (3 объектов), PUT на корректность проверки базовой работоспособности;
2. Вызов HEAD при GET-запросе для проверки передаваемых Headers;
3. Вызов всех объектов в БД через GET и проверка корректности (путём добавления 3х герояв и сравнения состояния до/после);
4. Проверка всех объектов на идентичные сущности;
5. Негативные тесты на недоступные операции с объектами;
6. Проверки кодов возврата (200, 400, 401, 404, 500), используя различные методы;
7. Проверки ответов сервера при повторном удалении персонажа, создании существующего и тд.;
8. Проверка условий мин/макс длины полей и выхода за эти условия;
9. Создание персонажа лишь с требуемым полем и без него;
10. Валидация полученных схем персонажей и ответов сервера по типам данных и некоторым символьным ограничениям;
11. Прикручен Allure.
####

### Логин и пароль от тестового сервиса передаются через параметры запуска ###
    `--login_auth=<login> --password_auth=<password>`


### Вызов тестов осуществляется из директории ### 
    `../test_ticket/source/` 

### Вызов тестов по следующим маркам:
1.     test_http_functional: Start of tests covering standard HTTP methods
2.     test_objects_api: Start of tests covering the correctness of objects in the database
3.     test_negative_cases: Start of tests covering negative cases
###

### Пример вызова набора тестов по маркировке test_http_functional: ###

    `rand_user@rand_os:(venv).../source$ pytest -vvs --login_auth=<login> --password_auth=<password> -m test_http_functional`

### Пример генерации Allure отчетика в Web формате на локал хосте: ###

    `rand_user@rand_os:(venv).../source$ pytest -vv --login_auth <login> --password_auth <password> --alluredir=/tmp/allure`
    `rand_user@rand_os:(venv).../source$ .../allure-2.7.0/bin/allure serve /tmp/allure/`

### Краткое описание архитектуры:
При вызове набора/тестового модуля/теста, выполняется вызов `source.helpers.work_with_api`, где организуется URL запрос 
с требуемым HTTP методом (используя библиотеку `requests`), запрос выполняется, а его результат приходит в 
`source.helpers.work_with_asserting_respose`. В последнем классе выполняется "разбиение" HTTP ответа на нужные части и
их возврат тестам по требованию.
На тесты накладываются декораторы аллюра и валидация полученных полей JSON.

1.     ../source/data/ - данные, необходимые для работы с объектами в БД, ответами от API и JSON схемки
2.     ../source/helpers/work_with_api.py - организация HTTP запросов
3.     ../source/helpers/work_with_asserting_respose.py - дробление HTTP ответа на нужные части, assert'ing в тесты
4.     ../source/helpers/work_with_fields.py - логика работы с полями объектов
5.     ../source/tests/test_api - тестовый набор
6.     ../source/conftest.py - фикстуры
7.     ../source/pytest.ini - custom марки
###