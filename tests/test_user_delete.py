import allure
import pytest
from datetime import datetime
from lib.assertions import Assertions  # import lib.assertions as Assertions
from lib.base_case import BaseCase  # import lib.base_case as BaseCase
from lib.my_requests import MyRequests  # import lib.my_requests as MyRequests


@allure.epic("Deleting cases")
class TestUserDelete(BaseCase):
    def create_user(self):
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
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

        user_id = self.get_json_value(response, "id")
        data['user_id'] = user_id

        return data

    def login_by_user(self, email, password):
        """
        :return: response
        """
        response = MyRequests.post(
            "/user/login",
            data={'email': email, 'password': password})

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

    def delete_user(self, user_id, token, auth_sid):
        response = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        return response

    @allure.description("This test tries to remove a protected user that cannot be removed")
    def test_delete_user_with_existing_email(self):
        user_id = self.existing_user_id
        email = self.existing_user_data['email']
        password = self.existing_user_data['password']

        # Login
        logged_user = self.login_by_user(email, password)
        auth_sid = self.get_cookie(logged_user, "auth_sid")
        token = self.get_header(logged_user, "x-csrf-token")
        Assertions.assert_status_code(logged_user, 200)

        # Delete
        response = self.delete_user(user_id, token, auth_sid)
        Assertions.assert_status_code(response, 400, f"{response.text}")

    @allure.description("This test deletes just created user")
    def test_delete_just_created_user(self):
        # Register
        created_user = self.create_user()
        user_id = created_user.get('user_id')
        email = created_user.get('email')

        # Login
        logged_user = self.login_by_user(created_user.get('email'), created_user.get('password'))
        auth_sid = self.get_cookie(logged_user, "auth_sid")
        token = self.get_header(logged_user, "x-csrf-token")
        Assertions.assert_status_code(logged_user, 200)

        # Delete
        deleted_user = self.delete_user(user_id, token, auth_sid)
        Assertions.assert_status_code(deleted_user, 200, f"Failed to delete user id={user_id} {email}")

        # Get User
        resulted_user = self.get_user(user_id, token, auth_sid)
        Assertions.assert_status_code(resulted_user, 404, f"{resulted_user.text}")

    @allure.description("This test is logged in by User1 and tries delete data of User2")
    def test_delete_user2_by_logged_user1(self):
        # Register User1 and User2
        created_user_1 = self.create_user()
        created_user_2 = self.create_user()
        user_id_1 = created_user_1.get('user_id')
        user_id_2 = created_user_2.get('user_id')

        # Login by User1
        logged_user_1 = self.login_by_user(created_user_1.get('email'), created_user_1.get('password'))
        auth_sid_1 = self.get_cookie(logged_user_1, "auth_sid")
        token_1 = self.get_header(logged_user_1, "x-csrf-token")
        Assertions.assert_status_code(logged_user_1, 200)

        # Delete User2
        deleted_user_2 = self.delete_user(user_id_2, token_1, auth_sid_1)
        # Assertions.assert_unexpected_status_code(deleted_user_2, 200)  # Отловим при проверке, удалились ли данные

        # Get User2 - user should be
        resulted_user_2 = self.get_user(user_id_2, None, None)
        Assertions.assert_status_code(resulted_user_2, 200, f"{resulted_user_2.text}")

        # Get User1 - user should be
        resulted_user_1 = self.get_user(user_id_1, token_1, auth_sid_1)
        Assertions.assert_status_code(resulted_user_1, 200, f"User id = {user_id_1} should not have been deleted!")
