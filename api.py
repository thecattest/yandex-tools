import json
import sys
from enum import Enum
from functools import wraps
from logging import Logger

import requests

assert sys.version_info >= (3, 8), "Необходим Python 3.8+"

log = Logger("yandex-tool")
TITLES = {
    'classwork': 'Классная работа',
    'homework': 'Домашняя работа',
    'additional': 'Дополнительные задачи',
    'additional-2': 'Дополнительные задачи 2 уровень',
    'additional-3': 'Итоговая контрольная',
    'control-work': 'Контрольная работа',
    'another': 'Другое',
    'individual-work': 'Самостоятельная работа',
}

CREDENTIALS_FILE_PATH = 'credentials.json'


class CredentialsType(Enum):
    json = "json"
    txt = "txt"
    text = txt


def auth_require(func):
    @wraps(func)
    def decorate(self, *args, **kwargs):
        if not self._authed:
            raise ValueError("Вы не авторизованы!")
        return func(self, *args, **kwargs)

    return decorate


class User:
    def __init__(self, login: str = None, password: str = None,
                 file_path: str = CREDENTIALS_FILE_PATH,
                 file_type: CredentialsType = CredentialsType.json
                 ):
        self.login, self.password = login, password
        self._authed = False
        self.session = requests.Session()

        self.file_path = file_path
        self.file_type = file_type

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['session']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.session = requests.Session()
        if self._authed:
            self.auth()

    def auth(self, login: str = None, password: str = None):
        if login is None:
            login = self.login
        else:
            self.login = login

        if password is None:
            password = self.password
        else:
            self.password = password

        auth = self.session.post('https://passport.yandex.ru/passport?mode=auth',
                                 data={'login': login, 'passwd': password})
        if auth.url == 'https://passport.yandex.ru/profile':
            log.debug('Авторизация прошла успешно')
            log.debug('===========\n')
            self._authed = True
            return self
        else:
            self._authed = False
            if 'Неправильный' in auth.text:
                raise ValueError('Неправильные логин или пароль')
            raise ValueError('Ошибка X')

    def load_credentials(self, file_path: str = None,
                         file_type: CredentialsType = None):

        if file_path is None:
            file_path = self.file_path
        if file_type is None:
            file_type = self.file_type

        try:
            with open(file_path, 'r') as file:
                self.file_path = file_path
                self.file_type = file_type
                if file_type == CredentialsType.json:
                    data = json.load(file)
                    self.login = data['login']
                    self.password = data['password']
                else:
                    self.login, self.password = file.read().split()
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл '{file_path}' не был найден!")
        return self

    def save_credentials(self, file_path: str = None,
                         file_type: CredentialsType = None):

        if file_path is None:
            file_path = self.file_path
        if file_type is None:
            file_type = self.file_type

        with open(file_path, 'w') as file:
            if file_type == CredentialsType.json:
                json.dump({
                    "login": self.login,
                    "password": self.password
                }, file)
            else:
                file.write(f"{self.login} {self.password}")
        return self

    @auth_require
    def get_lesson_ids(self, course_id: int, group_id: int):
        url = 'https://lyceum.yandex.ru/api/student/lessons'
        lessons = self.session.get(url, params={'groupId': group_id, 'courseId': course_id}).json()
        lesson_ids = list(lesson['id'] for lesson in lessons)
        return lesson_ids

    @auth_require
    def get_material_id(self, lesson_id: int):
        url = 'https://lyceum.yandex.ru/api/materials'
        material_info = self.session.get(url, params={'lessonId': lesson_id}).json()
        if material_info:
            material = material_info[0]
            if material['type'] != 'textbook':
                log.debug(material_info)
                raise ValueError
            return material['id']
        else:
            return 0

    @auth_require
    def get_material_html(self, lesson_id: int, group_id: int, material_id: int):
        url = f"https://lyceum.yandex.ru/api/student/materials/{material_id}"
        material = self.session.get(url, params={'groupId': group_id, 'lessonId': lesson_id}).json()
        material_html = material['detailedMaterial']['content']
        return material_html

    @auth_require
    def get_all_tasks(self, lesson_id: int, course_id: int):
        url = 'https://lyceum.yandex.ru/api/student/lessonTasks'
        lesson_info = self.session.get(url, params={'courseId': course_id, 'lessonId': lesson_id}).json()
        return lesson_info

    @auth_require
    def get_task(self, task_id: int, group_id: int):
        url = f'https://lyceum.yandex.ru/api/student/tasks/{task_id}'
        task = self.session.get(url, params={'groupId': group_id}).json()
        return task

    @auth_require
    def get_lesson_info(self, lesson_id: int, group_id: int, course_id: int):
        url = f'https://lyceum.yandex.ru/api/student/lessons/{lesson_id}'
        lesson_info = self.session.get(url, params={'groupId': group_id, 'courseId': course_id}).json()
        return lesson_info

    @auth_require
    def get_all_lessons(self, course_id: int, group_id: int):
        url = 'https://lyceum.yandex.ru/api/student/lessons'
        params = {'courseId': course_id,
                  'groupId': group_id}
        lessons = self.session.get(url, params=params).json()
        return lessons

    @auth_require
    def get_solution(self, solution_id: int):
        url = f'https://lyceum.yandex.ru/api/student/solutions/{solution_id}'
        solution = self.session.get(url).json()
        return solution

    @auth_require
    def get_notifications(self):
        url = 'https://lyceum.yandex.ru/api/notifications'
        notifications = self.session.get(url).json()
        return notifications

    @auth_require
    def get_courses_groups_ids(self):
        url = r'https://lyceum.yandex.ru/api/profile'
        courses = self.session.get(url=url, params={'onlyActiveCourses': True,
                                                    'withCoursesSummary': True,
                                                    'withExpelled': True}).json()
        courses = courses['coursesSummary']['student']
        ids = [{'title': course['title'],
                'rating': course['rating'],
                'course_id': course['id'],
                'group_id': course['group']['id']}
               for course in courses]
        return ids

    @auth_require
    def get_course(self, with_rating: bool = False):
        courses = self.get_courses_groups_ids()
        print("Выберите курс:")
        print(*(f"  {course['title']} - {n}" for n, course in enumerate(courses)), sep='\n')
        n = input()
        while not (n.isdigit() and -1 < int(n) < len(courses)):
            print("Ошибка! Введите число от 0 до", len(courses) - 1, file=sys.stderr)
            n = input()
        print('===========\n')
        course = courses[int(n)]
        if with_rating:
            return course['course_id'], course['group_id'], course['rating']
        else:
            return course['course_id'], course['group_id']
