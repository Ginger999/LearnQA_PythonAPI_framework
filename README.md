# LearnQA_PythonAPI_framework

python -m pytest -s tests/test_user_auth.py -k test_auth_user

python -m pytest -s tests/test_user_register.py
python -m pytest -s tests/test_user_register.py -k test_create_user_successfully 
python -m pytest -s tests/test_user_register.py -k test_create_user_with_existing_email
python -m pytest -s tests/test_user_register.py -k test_invalid_email_format
python -m pytest -s tests/test_user_register.py -k test_required_params
python -m pytest -s tests/test_user_register.py -k test_short_username  
python -m pytest -s tests/test_user_register.py -k test_too_long_username


