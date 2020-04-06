import requests
from pprint import pprint


def auth(s):
    auth = s.post('https://passport.yandex.ru/passport?mode=auth',
                  data={'login': login, 'passwd': password})
    if auth.url == 'https://passport.yandex.ru/profile':
        print('Авторизация прошла успешно')
    else:
        if 'Неправильный' in auth.text:
            raise Exception('Неправильные логин или пароль')
        raise Exception('Ошибка X')


def get_lesson_ids(s):
    url = 'https://lyceum.yandex.ru/api/student/lessons'
    lessons = s.get(url, params={'groupId': group_id, 'courseId': course_id}).json()
    lesson_ids = list(lesson['id'] for lesson in lessons)
    return lesson_ids


def get_material_id(s, lesson_id):
    url = 'https://lyceum.yandex.ru/api/materials'
    material_info = s.get(url, params={'lessonId': lesson_id}).json()
    material_id = material_info[0]['id']
    return material_id


def get_material_html(s, lesson_id, material_id):
    url = f"https://lyceum.yandex.ru/api/student/materials/{material_id}"
    material = s.get(url, params={'groupId': group_id, 'lessonId': lesson_id}).json()
    material_html = material['detailedMaterial']['content']
    return material_html


def get_lesson_info(s, lesson_id):
    url = 'https://lyceum.yandex.ru/api/student/lessonTasks'
    lesson_info = s.get(url, params={'courseId': course_id, 'lessonId': lesson_id}).json()
    return lesson_info


group_id = 1264
course_id = 165

s = requests.Session()

login = input('Login: ')
password = input('Password: ')
auth(s)

lesson_ids = get_lesson_ids(s)
points = dict()

for lesson_id in lesson_ids:
    lesson_info = get_lesson_info(s, lesson_id)
    for tasks in lesson_info:
        n = len(tasks['tasks'])
        type = tasks['type']
        if type in points:
            points[type] += n
        else:
            points[type] = n


print(points)
