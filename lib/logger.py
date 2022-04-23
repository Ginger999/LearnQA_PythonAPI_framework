import os
import inspect
from datetime import datetime
from requests import Response
from environment import ENV_OBJECT


class Logger:
    file_name = f"\\logs\\log_" + str(datetime.now().strftime("%y-%m-%d_%H-%M-%S")) + ".log"
    # От каталога текущего модуля вверх по дереву каталогов
    full_file_name = os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], f"..{file_name}"))

    @classmethod
    def _write_log_to_file(cls, data: str):
        # print(f"os.path.exists(cls.file_name)")
        with open(cls.full_file_name, 'a', encoding='utf-8') as logger_file:
            logger_file.write(data)

    @classmethod
    def add_request(cls, url: str, data: dict, headers: dict, cookies: dict, method: str):
        testname = os.environ.get('PYTEST_CURRENT_TEST')
        data_to_add = "\n-----\n" + testname
        data_to_add += f"\n{ENV_OBJECT.env}\n"
        data_to_add += f"Test: {testname}\n"
        data_to_add += f"Time: {str(datetime.now())}\n"
        data_to_add += f"Request method: {method}\n"
        data_to_add += f"Request URL: {url}\n"
        data_to_add += f"Request data: {data}\n"
        data_to_add += f"Request headers: {headers}\n"
        data_to_add += f"Request cookies: {cookies}\n"
        data_to_add += "\n"

        cls._write_log_to_file(data_to_add)

    @classmethod
    def add_response(cls, response: Response):
        cookies_as_dict = dict(response.cookies)
        headers_as_dict = dict(response.headers)

        data_to_add = f"Response code: {response.status_code}\n"
        data_to_add += f"Response text: {response.text}\n"
        data_to_add += f"Response headers: {headers_as_dict}\n"
        data_to_add += f"Response cookies: {cookies_as_dict}\n"
        data_to_add += f"\n-----\n"

        cls._write_log_to_file(data_to_add)
