import allure
import pytest
from datetime import datetime
from lib.assertions import Assertions  # import lib.assertions as Assertions
from lib.base_case import BaseCase  # import lib.base_case as BaseCase
from lib.my_requests import MyRequests  # import lib.my_requests as MyRequests
from tests.test_user_register import TestUserRegister   # import tests.test_user_register as TestUserRegister


@allure.epic("Editing cases")
class TestUserEdit(BaseCase):
    include_params = [
        ("email"),
        ("firstName"),
        ("lastName"),
        ("username")]

    def created_user(self):
        """
        Create User using the exiting test
        :return: JSON {
            'password': password,
            'username': username,
            'firstName': firstName,
            'lastName': lastName,
            'email': email,
            'user_id': user_id}
        """
        # Register User using existing test
        user_created_by_test = TestUserRegister.test_create_user_successfully(self)

        # Get user registered data
        registered_data = user_created_by_test.get('data')

        # Get response after user registration
        response = user_created_by_test.get('response')

        # Add useful info of 'user_id' into 'registered_data' dictionary
        user_id = self.get_json_value(response, "id")
        registered_data['user_id'] = user_id

        return registered_data

    def login_by_user(self, email, password):
        """
        :return: response
        """
        response = MyRequests.post(
            "/user/login",
            data={'email': email, 'password': password})

        return response

    def edit_user(self, user_id, token, auth_sid, param, param_value):
        """
        :return: response
        """
        response = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={param: param_value}
        )
        return response

    def get_user(self, user_id, token, auth_sid):
        """
        :return: response
        """
        response = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        return response

    @allure.description("This test edits just created user firstname and save edited data")
    @pytest.mark.parametrize('param', include_params)
    def test_edit_just_created_user(self, param):
        # Register
        created_user = self.created_user()
        user_id = created_user.get('user_id')

        # Login
        logged_user = self.login_by_user(created_user.get('email'), created_user.get('password'))
        auth_sid = self.get_cookie(logged_user, "auth_sid")
        token = self.get_header(logged_user, "x-csrf-token")
        Assertions.assert_status_code(logged_user, 200)

        # Edit
        new_param_value = self.changed_user_params.get(param)
        edited_user = self.edit_user(user_id, token, auth_sid, param, new_param_value)
        Assertions.assert_status_code(edited_user, 200)

        # Get
        resulted_user = self.get_user(user_id, token, auth_sid)
        Assertions.assert_status_code(resulted_user, 200)
        Assertions.assert_json_value_by_name(resulted_user, param, new_param_value, "")

    @allure.description("This test tries edits just created user without login")
    @pytest.mark.parametrize('param', include_params)
    def test_edit_user_without_login(self, param):
        """
        Попытаемся изменить данные пользователя не будучи авторизованными
        """
        # Register
        created_user = self.created_user()
        user_id = created_user.get('user_id')

        # Edit
        new_param_value = self.changed_user_params.get(param)
        edited_user = self.edit_user(user_id, None, None, param, new_param_value)
        Assertions.assert_status_code(edited_user, 400)
        Assertions.assert_auth_token_not_supplied(edited_user, param, new_param_value)

    @allure.description("This test is logged in by User1 and tries change data of User2")
    @pytest.mark.parametrize('param', include_params)
    def test_edit_user2_by_logged_user1(self, param):
        """
        Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
        """
        # Register User1 and User2
        created_user_1 = self.created_user()
        created_user_2 = self.created_user()
        user_id_1 = created_user_1.get('user_id')
        user_id_2 = created_user_2.get('user_id')
        old_param_value_1 = created_user_1.get(param)
        old_param_value_2 = created_user_2.get(param)

        # Login by User1
        logged_user_1 = self.login_by_user(created_user_1.get('email'), created_user_1.get('password'))
        auth_sid_1 = self.get_cookie(logged_user_1, "auth_sid")
        token_1 = self.get_header(logged_user_1, "x-csrf-token")
        Assertions.assert_status_code(logged_user_1, 200)

        # Edit User2
        new_param_value = self.changed_user_params.get(param)
        edited_user_2 = self.edit_user(user_id_2, token_1, auth_sid_1, param, new_param_value)
        # Assertions.assert_unexpected_status_code(edited_user, 200)  # Отловим при проверке, отредактировались ли данные

        # Get User1 - param value should not be changed
        resulted_user_1 = self.get_user(user_id_1, token_1, auth_sid_1)
        Assertions.assert_status_code(resulted_user_1, 200)
        Assertions.assert_json_value_by_name(resulted_user_1, param, old_param_value_1, "")

        # Login by User2
        logged_user_2 = self.login_by_user(created_user_2.get('email'), created_user_2.get('password'))
        auth_sid_2 = self.get_cookie(logged_user_2, "auth_sid")
        token_2 = self.get_header(logged_user_2, "x-csrf-token")
        Assertions.assert_status_code(logged_user_2, 200)

        # Get User2 - param value should not be changed
        resulted_user_2 = self.get_user(user_id_2, token_2, auth_sid_2)
        Assertions.assert_status_code(resulted_user_2, 200)
        Assertions.assert_json_value_by_name(resulted_user_2, param, old_param_value_2, "")

    @allure.description("This test is logged in by User1 and tries replace email"
                        "with new email which doesn't contain '@'")
    def test_edit_user_with_invalid_format_email(self):
        """
        Попытаемся изменить email пользователя, будучи авторизованным тем же пользователем,
        на email без '@'
        """
        # Register
        created_user = self.created_user()
        user_id = created_user.get('user_id')

        # Login
        logged_user = self.login_by_user(created_user.get('email'), created_user.get('password'))
        auth_sid = self.get_cookie(logged_user, "auth_sid")
        token = self.get_header(logged_user, "x-csrf-token")
        Assertions.assert_status_code(logged_user, 200)

        # Edit
        param = 'email'
        new_param_value = self.prepare_invalid_format_email(created_user.get('email'))
        edited_user = self.edit_user(user_id, token, auth_sid, param, new_param_value)

        Assertions.assert_status_code(edited_user, 400)
        Assertions.assert_invalid_email_format(edited_user, new_param_value)

    @allure.description("This test is logged in by User1 and tries replace firstName"
                        "with new firstName which has too short length")
    def test_with_too_short_firstname(self):
        """
        Попытаемся изменить firstName пользователя, будучи авторизованным тем же пользователем,
        на очень короткое значение в 1 символ
        """
        # Register
        created_user = self.created_user()
        user_id = created_user.get('user_id')

        # Login
        logged_user = self.login_by_user(created_user.get('email'), created_user.get('password'))
        auth_sid = self.get_cookie(logged_user, "auth_sid")
        token = self.get_header(logged_user, "x-csrf-token")
        Assertions.assert_status_code(logged_user, 200)

        # Edit
        param = 'firstName'
        new_param_value = self.too_short_first_name
        edited_user = self.edit_user(user_id, token, auth_sid, param, new_param_value)

        # Assertions.assert_status_code(edited_user, 400)
        Assertions.assert_too_short_param_value(edited_user, param, new_param_value)
