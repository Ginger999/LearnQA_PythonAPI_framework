import allure
import pytest
from lib.assertions import Assertions  # import lib.assertions as Assertions
from lib.base_case import BaseCase  # import lib.base_case as BaseCase
from lib.my_requests import MyRequests  # import lib.my_requests as MyRequests


@allure.epic("User info getting cases")
class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_keys(response, ["email", "firstName", "lastName"])

        # print(response.content)

    @allure.description("This test loggings by user and read expected user info")
    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(
            f"/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.description("This test logins by User1 and tries to get User2 info")
    def test_get_user_details_auth_as_another_user(self):
        # Register User1
        register_data = self.prepare_registration_data()
        response_1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_status_code(response_1, 200)
        Assertions.assert_json_has_key(response_1, "id")

        user_id_1 = self.get_json_value(response_1, "id")

        # Login by existing User2
        response_2_1 = MyRequests.post("/user/login", data={'email': 'vinkotov@example.com', 'password': '1234'})

        Assertions.assert_status_code(response_2_1, 200)

        token_2 = self.get_header(response_2_1, "x-csrf-token")
        user_id_from_auth_method_2 = self.get_json_value(response_2_1, "user_id")

        # Get User1 data fields
        response_2_2 = MyRequests.get(
            f"/user/{user_id_from_auth_method_2}",
            headers={"x-csrf-token": token_2},
            cookies={"auth_sid": user_id_1}
        )

        expected_fields = ["username"]
        Assertions.assert_json_has_keys(response_2_2, expected_fields)

        unexpected_fields = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_not_keys(response_2_2, unexpected_fields)
