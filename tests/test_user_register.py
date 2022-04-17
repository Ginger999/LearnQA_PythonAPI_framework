import requests
from lib.base_case import BaseCase  # import lib.base_case as BaseCase
from lib.assertions import Assertions  # import lib.assertions as Assertions
from datetime import datetime
import pytest


class TestUserAuth(BaseCase):
    required_params = [
        ("password"),
        ("username"),
        ("firstName"),
        ("lastName"),
        ("email")
    ]

    def setup(self):
        base_part = 'learnqa'
        domain = 'example.com'
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"

        self.data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

    def test_create_user_successfully(self):
        response = requests.post("https://playground.learnqa.ru/api/user/", data=self.data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        existing_email = 'vinkotov@example.com'
        self.data['email'] = existing_email

        response = requests.post("https://playground.learnqa.ru/api/user/", data=self.data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{existing_email}' already exists", \
            f"Unexpected response content '{response.content}'"

    def test_invalid_email_format(self):
        self.data['email'] = self.email.replace('@', '')

        response = requests.post("https://playground.learnqa.ru/api/user/", data=self.data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode(
            "utf-8") == f"Invalid email format", f"Invalid email format {self.data['email']}"

    @pytest.mark.parametrize('param', required_params)
    def test_required_params(self, param):
        del self.data[param]

        response = requests.post("https://playground.learnqa.ru/api/user/", data=self.data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {param}", \
            f"The following required params are missed: '{param}"

    def test_short_username(self):
        self.data['username'] = 'a'

        response = requests.post("https://playground.learnqa.ru/api/user/", data=self.data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too short", \
            f"The value of 'username' field is too short '{self.data['username']}'"

    def test_too_long_username(self):
        self.data['username'] = 'a' * 251

        response = requests.post("https://playground.learnqa.ru/api/user/", data=self.data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too long", \
            f"The value of 'username' field is too long {self.data['username'].__len__()}"
