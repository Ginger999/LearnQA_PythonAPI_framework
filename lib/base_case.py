import json.decoder
from datetime import datetime
from requests import Response


class BaseCase:
    existing_user_data = {
        'email': 'vinkotov@example.com',
        'password': '1234'
    }
    existing_user_id = 2

    too_short_first_name = 'a'
    changed_user_params = {}

    def setup(self):
        self.changed_user_params = self.prepare_changed_user_data()

    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot find header with name {headers_name} in the last response"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON does not have key '{name}'"

        return response_as_dict[name]

    def prepare_registration_data(self, email=None):
        if email is None:
            random_part = datetime.now().strftime("%m%d%Y%H%M%S__%f")
            email = f"learnqa{random_part}@example.com"
        return {
            'password': '1234',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

    def prepare_changed_user_data(self):
        random_part = datetime.now().strftime("%m%d%Y%H%M%S__%f")
        email = f"workqa{random_part}@example.com"

        return {'email': email,
                'firstName': 'ChangedName',
                'lastName': 'ChangedLastName',
                'password': '^%#E^47',
                'username': 'workqa'
                }

    def prepare_invalid_format_email(self, email=None):
        if email is None:
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"learnqa{random_part}@example.com"

        email = email.replace('@', '')

        return email
