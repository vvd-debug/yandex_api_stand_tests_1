import sender_stand_request
import data

def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body['firstName'] = first_name
    return current_body

# Функция для позитивной проверки
def positive_assert(first_name):
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body(first_name)
    # В переменную user_response сохраняется результат запроса на создание пользователя:
    user_response = sender_stand_request.post_new_user(user_body)

    # Проверяется, что код ответа равен 201
    assert user_response.status_code == 201
    # Проверяется, что в ответе есть поле authToken и оно не пустое
    assert user_response.json()["authToken"] != ""

    # В переменную users_table_response сохраняется результат запроса на получение данных из таблицы user_model
    users_table_response = sender_stand_request.get_users_table()

    # Строка, которая должна быть в ответе
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    # Проверка, что такой пользователь есть и он единственный
    assert users_table_response.text.count(str_user) == 1

# Тест 1. Успешное создание пользователя
# Параметр fisrtName состоит из 2 символов
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")

def test_create_user_2_letter_in_first_name_get_success_response():
    user_body = get_user_body('Aa')
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""

    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
           + user_body["address"] + ",,," + user_response.json()["authToken"]

    assert users_table_response.text.count(str_user) == 1

def test_create_user_15_letter_in_first_name_get_success_response():
    user_body = get_user_body('Aaaaaaaaaaaaaaa')
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""

    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    assert users_table_response.text.count(str_user) == 1

#Тест 2 с помощью позитив ассерт
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert('Aaaaaaaaaaaaaaa')

#вспмогательная функция негативной проверки
def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    # В переменную response сохраняется результат запроса на создание пользователя:
    response = sender_stand_request.post_new_user(user_body)

    # Проверяется, что код ответа равен 400
    assert response.status_code == 400
    #Проверка, что в теле ответа атрибут code равен 400
    assert response.json()["code"] == 400
    # Проверка текста в теле ответа атрибута message
    assert response.json()["message"] == "Имя пользователя введено некорректно. " \
                                             "Имя может содержать только русские или латинские буквы, " \
                                             "длина должна быть не менее 2 и не более 15 символов"

#Тест №3 -- проверяет, что нельзя создать пользователя с именем из одной буквы
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol('A')

#Тест №4 -- должен выдать ошибку, если в имени будет больше 15 букв
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol('Aaaaaaaaaaaaaaaa')

#Тест № 5 -- разрешены английские буквы
def test_create_user_english_letter_in_first_name_get_success_response():
    positive_assert('QWERty')

#Тест №6 -- создание новго пользователя
# в поле first_name разрешены русские буквы
def test_create_user_russian_letter_in_first_name_get_success_response():
    positive_assert('Мария')

#Тест №7 -- создание нового пользователя
#в поле first_name не могут быть пробелы
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol('A p')

#Тест №8 -- создание нового пользователя
# в поле first_name не должно быть спецсимволов
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol('*')

#Тест №9 -- создание нового пользователя
#в поле first_name не должно быть цифр
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol('123Gjyg')

#вспомогательная функция для проверки поля first_name
def negative_assert_no_first_name(user_body):
        # В переменную response сохрани результат вызова функции
    response = sender_stand_request.post_new_user(user_body)

        # Проверь, что код ответа — 400
    assert response.status_code == 400

        # Проверь, что в теле ответа атрибут "code" — 400
    assert response.json()["code"] == 400

        # Проверь текст в теле ответа в атрибуте "message"
    assert response.json()["message"] == "Не все необходимые параметры были переданы"


#Тест № 10 -- создание нового пользователя, передан пустой параметр
def test_create_user_no_first_name_get_error_response():
    # Копируется словарь с телом запроса из файла data в переменную user_body
    # Иначе можно потерять данные из исходного словаря
    user_body = data.user_body.copy()
    # Удаление параметра firstName из запроса
    user_body.pop("firstName")
    # Проверка полученного ответа
    negative_assert_no_first_name(user_body)

#Тест 11 -- создание новго пользователя, нет символов
def test_create_user_empty_first_name_get_error_response():
        # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body("")
        # Проверка полученного ответа
    negative_assert_no_first_name(user_body)


# Тест №12 -- в поле first_name передан не строковой тип параметра
def test_create_user_number_type_first_name_get_error_response():
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body(12)
    # Проверка полученного ответа
    response = sender_stand_request.post_new_user(user_body)

    # Проверка кода ответа
    assert response.status_code == 400

