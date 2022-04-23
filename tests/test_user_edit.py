import allure
import pytest
from lib.assertions import Assertions  # import lib.assertions as Assertions
from lib.base_case import BaseCase  # import lib.base_case as BaseCase
from lib.my_requests import MyRequests  # import lib.my_requests as MyRequests
from tests.test_user_register import TestUserRegister   # import tests.test_user_register as TestUserRegister


@allure.epic("Editing cases")
class TestUserEdit(BaseCase):
    @pytest.fixture()
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

    @allure.description("This test edits just created user firstname and save edited data")
    def test_edit_just_created_user(self, created_user):
        # Register
        created_user_id = created_user.get('user_id')

        # Login
        response2 = MyRequests.post(
            "/user/login",
            data={'email': created_user.get('email'), 'password': created_user.get('password')}
        )
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        Assertions.assert_status_code(response2, 200)

        # Edit
        new_name = 'Changed Name'

        response3 = MyRequests.put(
            f"/user/{created_user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )
        Assertions.assert_status_code(response3, 200)

        # Get
        response4 = MyRequests.get(
            f"/user/{created_user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    @allure.description("This test tries edits just created user without login")
    def test_edit_just_created_user_without_login(self, created_user):
        """
        Попытаемся изменить данные пользователя не будучи авторизованными
        """
        # Register
        created_user_id = created_user.get('user_id')

        # Edit
        changed_user_params = {
            'firstName': 'ChangedName',
            'lastName': 'ChangedLastName',
            'email': '',
            'password': '^%#E^47'
        }
        for param in changed_user_params:
            param_value = changed_user_params.get(param)

            response2 = MyRequests.put(
                f"/user/{created_user_id}",
                headers={"x-csrf-token": ""},
                cookies={"auth_sid": created_user_id},
                data={param: param_value}
            )
            Assertions.assert_status_code(response2, 400)
            Assertions.assert_auth_token_not_supplied(response2, param, param_value)

    @allure.description("This test is logged in by User1 and tries change data of User2")
    def test_edit_just_created_user2_by_logged_user2(self, created_user):
        """
        Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
        """
        # Loging by User 1
        data = self.prepare_registration_email('vinkotov@example.com')
        response1 = MyRequests.post("/user/login", data=data)
        Assertions.assert_status_code(response1, 200)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # Register User 2
        created_user_id = created_user.get('user_id')

        # Edit User 2
        new_name = 'Changed Name'
        response2 = MyRequests.put(
            f"/user/{created_user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )
        Assertions.assert_status_code(response2, 400)
        # Assertions.assert_auth_token_not_supplied(response2, new_name)

    @allure.description("This test is logged in by User1 and tries replace email"
                        "with new email which doesn't contain '@'")
    def test_edit_just_created_user_with_invalid_format_email(self, created_user):
        """
        Попытаемся изменить email пользователя, будучи авторизованным тем же пользователем,
        на email без '@'
        """
        # Register
        created_user_id = created_user.get('user_id')

        # Login
        response2 = MyRequests.post(
            "/user/login",
            data={'email': created_user.get('email'), 'password': created_user.get('password')}
        )
        Assertions.assert_status_code(response2, 200)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Edit User 2
        new_email = self.prepare_invalid_format_email(created_user.get('email'))

        response2 = MyRequests.put(
            f"/user/{created_user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )
        Assertions.assert_status_code(response2, 400)
        Assertions.assert_invalid_email_format(response2, new_email)

    @allure.description("This test is logged in by User1 and tries replace firstName"
                        "with new firstName which has too short length")
    def test_edit_just_created_user_with_too_short_username(self, created_user):
        """
        Попытаемся изменить firstName пользователя, будучи авторизованным тем же пользователем,
        на очень короткое значение в 1 символ
        """

        # Register
        created_user_id = created_user.get('user_id')

        # Login
        response2 = MyRequests.post(
            "/user/login",
            data={'email': created_user.get('email'), 'password': created_user.get('password')}
        )
        Assertions.assert_status_code(response2, 200)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        new_first_name = self.too_short_first_name
        # Edit User 2
        response2 = MyRequests.put(
            f"/user/{created_user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_first_name}
        )
        Assertions.assert_status_code(response2, 400)
        Assertions.assert_invalid_email_format(response2, new_first_name)
