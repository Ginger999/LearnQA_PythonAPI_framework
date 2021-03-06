from requests import Response
import json


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON does not have key '{name}'"
        assert response_as_dict[name] == expected_value, f"Expected: '{expected_value}' | Actual: '{response_as_dict[name]}' {error_message} "

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON does not have key '{name}'"

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        for name in names:
            assert name in response_as_dict, f"Response JSON does not have key '{name}'"

    @staticmethod
    def assert_json_has_not_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name not in response_as_dict, f"Response JSON shouldn't have key '{name}', but it's present"

    @staticmethod
    def assert_json_has_not_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        for name in names:
            assert name not in response_as_dict, f"Response JSON shouldn't have key '{name}', but it's present"

    @staticmethod
    def assert_status_code(response: Response, expected_status_code, error_message=""):
        assert response.status_code == expected_status_code,\
            f"Unexpected status code! Expected: {expected_status_code} Actual: {response.status_code} {error_message}"

    @staticmethod
    def assert_unexpected_status_code(response: Response, unexpected_status_code, error_message=""):
        assert response.status_code != unexpected_status_code, \
            f"Status code should not be equal {unexpected_status_code} {error_message}"

    @staticmethod
    def assert_required_params(response: Response, param):
        assert response.content.decode("utf-8") == f"The following required params are missed: {param}", \
            f"The following required params are missed: '{param}"

    @staticmethod
    def assert_too_long_param_value(response: Response, param, value):
        assert response.content.decode("utf-8") == f"The value of '{param}' field is too long", \
            f"The value of '{param}' field is too long {value.__len__()}"

    @staticmethod
    def assert_auth_token_not_supplied(response: Response, param, value):
        assert response.content.decode("utf-8") == f"Auth token not supplied", \
            f"The attempt to changed '{param}' with '{value}' for unlogged user"

    @staticmethod
    def assert_invalid_email_format(response: Response, email):
        assert response.content.decode("utf-8") == f"Invalid email format", \
            f"Invalid email format '{email}'"

    @staticmethod
    def assert_too_short_param_value(response: Response, param, value):
        err_msg_1 = f"The value of '{param}' field is too short"
        err_msg_2 = f"Too short value for field {param}"

        content = response.content.decode("utf-8")

        assert (content.find(err_msg_1) > -1 or content.find(err_msg_2) > -1), f"{err_msg_1} '{value}'"
