import allure
import pytest
from datetime import datetime
from lib.assertions import Assertions  # import lib.assertions as Assertions
from lib.base_case import BaseCase  # import lib.base_case as BaseCase
from lib.my_requests import MyRequests  # import lib.my_requests as MyRequests


@allure.epic("Registration cases")
class TestUserRegister(BaseCase):
    required_params = [
        ("password"),
        ("username"),
        ("firstName"),
        ("lastName"),
        ("email")
    ]

    @allure.suite("create_001")
    @allure.title("Valid user creation")
    @allure.description("This test creates user successfully")
    def test_create_user_successfully(self):
        """
        :return: JSON {'data': data, 'response': response}
        """
        data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")
        return {'data': data, 'response': response}

    @allure.suite("create_002")
    @allure.title("Invalid user creation with an existing email")
    @allure.description("This test tries to create a user that already exists")
    def test_create_user_with_existing_email(self):
        existing_email = self.existing_user_data['email']
        data = self.prepare_registration_data(existing_email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{existing_email}' already exists", \
            f"Unexpected response content '{response.content}'"

    @allure.suite("create_003")
    @allure.title("Invalid user creation with invalid email format")
    @allure.description("This test tries to create a user using invalid email format")
    def test_invalid_email_format(self):
        data = self.prepare_registration_data()
        data['email'] = self.prepare_invalid_format_email(data['email'])

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode(
            "utf-8") == f"Invalid email format", f"Invalid email format {data['email']}"

    @allure.suite("create_004")
    @allure.title("Invalid user creation with insufficient params")
    @allure.description("This test checks that the needed param of user is present")
    @pytest.mark.parametrize('param', required_params)
    def test_required_params(self, param):
        data = self.prepare_registration_data()
        del data[param]

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_required_params(response, param)

    @allure.suite("create_005")
    @allure.title("Invalid user creation with too short username")
    @allure.description("This test tries to create a user using too short username")
    def test_short_username(self):
        data = self.prepare_registration_data()
        param = 'username'
        data[param] = self.too_short_first_name

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_too_short_param_value(response, param, data[param])

    @allure.suite("create_006")
    @allure.title("Invalid user creation with too long username")
    @allure.description("This test tries to create a user using too long username")
    def test_too_long_username(self):
        data = self.prepare_registration_data()
        param = 'username'
        data[param] = 'a' * 251

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_too_long_param_value(response, param, data[param])
