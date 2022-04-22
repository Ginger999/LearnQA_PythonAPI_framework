import allure
import pytest
from lib.assertions import Assertions  # import lib.assertions as Assertions
from lib.base_case import BaseCase  # import lib.base_case as BaseCase
from lib.my_requests import MyRequests  # import lib.my_requests as MyRequests


@allure.epic("Editing cases")
class TestUserEdit(BaseCase):
    @pytest.fixture()
    def created_user(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)
        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        email = register_data['email']
        first_Name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")
        return {'email': email, 'first_Name': first_Name, 'password': password, 'user_id': user_id}

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
        # Register
        created_user_id = created_user.get('user_id')

        # Edit
        new_name = 'Changed Name'
        response2 = MyRequests.put(
            f"/user/{created_user_id}",
            headers={"x-csrf-token": ""},
            cookies={"auth_sid": created_user_id},
            data={"firstName": new_name}
        )
        Assertions.assert_status_code(response2, 400)
        Assertions.assert_auth_token_not_supplied(response2, created_user.get('email'))
