import warnings
from getpass import getpass
from io import StringIO
from sys import stderr

from api import User

warnings.filterwarnings("ignore")

user = User()
user.login = input("Введите логин: ")
print("Пароль: ", end='', flush=True)
user.password = getpass(stream=StringIO())
print()
print("Авторизуемся...")
try:
    user.auth()
except ValueError:
    print("Ошибка! неверный логин или пароль!", file=stderr)
    exit(1)
print("Вы успешно авторизовались! Сохраняем данные...")
user.save_credentials()
print("Данные сохранены!")
