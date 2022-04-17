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
        assert response_as_dict[name] == expected_value, error_message

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
    def assert_status_code(response: Response, expected_status_code):
        assert response.status_code == expected_status_code,\
            f"Unexpected status code! Expected: {expected_status_code} Actual: {response.status_code}"

    @staticmethod
    def assert_required_params(response: Response, param):
        assert response.content.decode("utf-8") == f"The following required params are missed: {param}",\
            f"The following required params are missed: '{param}"

    @staticmethod
    def assert_too_short_param_value(response: Response, param, value):
        assert response.content.decode("utf-8") == f"The value of '{param}' field is too short", \
             f"The value of '{param}' field is too short '{value}'"

    @staticmethod
    def assert_too_long_param_value(response: Response, param, value):
        assert response.content.decode("utf-8") == f"The value of '{param}' field is too long",\
            f"The value of '{param}' field is too long {value.__len__()}"
