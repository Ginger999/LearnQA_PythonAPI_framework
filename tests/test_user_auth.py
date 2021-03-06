import allure
import pytest
from lib.assertions import Assertions  # import lib.assertions as Assertions
from lib.base_case import BaseCase  # import lib.base_case as BaseCase
from lib.my_requests import MyRequests  # import lib.my_requests as MyRequests


@allure.epic("Authorization cases")
class TestUserAuth(BaseCase):
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup(self):
        response1 = MyRequests.post("/user/login", data=self.existing_user_data)

        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")
        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")

    @allure.suite("auth_001")
    @allure.title("Authorization by valid User")
    @allure.description("This test successfully authorizes user by email and password")
    def test_auth_user(self):
        response2 = MyRequests.get(
            "/user/auth",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )
        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            self.user_id_from_auth_method,
            f"User id from auth is not equal to user id from check method"
        )

    @allure.suite("auth_002")
    @allure.title("Authorization with insufficient parameters")
    @allure.description("This test authorization status w/o sending auth cookie or token")
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_user(self, condition):
        if condition == "no_cookie":
            response2 = MyRequests.get(
                "/user/auth",
                headers={"x-csrf-token": self.token},
            )
        else:
            response2 = MyRequests.get(
                "/user/auth",
                cookies={"auth_id": self.auth_sid}
            )
        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            0,
            f"User is authorized with condition '{condition}'"
        )
