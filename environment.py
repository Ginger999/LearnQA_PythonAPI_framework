import os


class Environment:
    dev = "DEV"
    prod = "PROD"
    env = ""

    URLS = {
        dev: 'https://playground.learnqa.ru/api_dev',
        prod: 'https://playground.learnqa.ru/api'
    }

    def __init__(self):
        try:
            self.env = os.environ['ENV']
        except KeyError:
            self.env = self.dev
            print(f"{self.env}")

    def get_base_url(self):
        if self.env in self.URLS:
            return self.URLS[self.env]
        else:
            raise Exception(f"Unknown variable of ENV variable {self.env}")

ENV_OBJECT = Environment()
