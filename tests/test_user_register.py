import allure
import requests
from lib.base_case import BaseCase  # import lib.base_case as BaseCase
from lib.assertions import Assertions  # import lib.assertions as Assertions
import pytest

@allure.epic("Registration cases")
class TestUserAuth(BaseCase):
    required_params = [
        ("password"),
        ("username"),
        ("firstName"),
        ("lastName"),
        ("email")
    ]

    @allure.description("")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.description("")
    def test_create_user_with_existing_email(self):
        existing_email = 'vinkotov@example.com'
        data = self.prepare_registration_data(existing_email)

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{existing_email}' already exists", \
            f"Unexpected response content '{response.content}'"

    @allure.description("")
    def test_invalid_email_format(self):
        data = self.prepare_registration_data()
        data['email'] = data['email'].replace('@', '')

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode(
            "utf-8") == f"Invalid email format", f"Invalid email format {data['email']}"

    @allure.description("")
    @pytest.mark.parametrize('param', required_params)
    def test_required_params(self, param):
        data = self.prepare_registration_data()
        del data[param]

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_required_params(response, param)

    @allure.description("")
    def test_short_username(self):
        data = self.prepare_registration_data()
        param = 'username'
        data[param] = 'a'

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_too_short_param_value(response, param, data[param])

    @allure.description("")
    def test_too_long_username(self):
        data = self.prepare_registration_data()
        param = 'username'
        data[param] = 'a' * 251

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_too_long_param_value(response, param, data[param])
