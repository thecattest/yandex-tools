import requests

login, password = input('Введите логин: '), input('Введите пароль: ')

s = requests.Session()
auth = s.post('https://passport.yandex.ru/passport?mode=auth', data={'login': login, 'passwd': password})
if auth.url == 'https://passport.yandex.ru/profile':
    print('Авторизация прошла успешно')
else:
    raise Exception('ОШИБКА! Проверьте верность введённых данных и интернет соединение
