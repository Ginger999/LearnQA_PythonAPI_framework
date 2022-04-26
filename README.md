# LearnQA_PythonAPI_framework

// Проверка версии python
python --version

// Запуск тестов
python -m pytest -s tests/test_user_auth.py -k test_auth_user

// Allure
Документация: https://docs.qameta.io/allure/#_pytest
Установка allure: scoop install allure
Запуск тестов: python -m pytest --alluredir=test_results/ -s tests/test_user_auth.py
Сгенерировать отчеты: allure serve test_results

// Переменная окружения ENV
Запускать через cmd (через терминал не работает)
set ENV=dev // set ENV=prod
echo %ENV%

//Docker
docker pull python 

docker build -t pytest_runner

docker run --rm --mount type=bind,src=C:\SW\LearnQA_PythonAPI_framework target=/tests_project/ pytest_runner

docker-compose up --build