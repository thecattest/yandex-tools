from getpass import getpass
import requests


titles = {'classwork': 'Классная работа',
          'homework': 'Домашняя работа',
          'additional': 'Дополнительные задачи',
          'additional-3': 'Дополнительные задачи',
          'control-work': 'Контрольная',
          'individual-work': 'Самостоятельная работа'}


def auth(s, login, password):
    auth = s.post('https://passport.yandex.ru/passport?mode=auth',
                  data={'login': login, 'passwd': password})
    if auth.url == 'https://passport.yandex.ru/profile':
        print('Авторизация прошла успешно')
    else:
        if 'Неправильный' in auth.text:
            raise Exception('Неправильные логин или пароль')
        raise Exception('Ошибка X')


def get_and_auth():
    login = input('Login: ')
    password = getpass()
    s = requests.Session()
    auth(s, login, password)
    return s


def get_lesson_ids(s, course_id, group_id):
    url = 'https://lyceum.yandex.ru/api/student/lessons'
    lessons = s.get(url, params={'groupId': group_id, 'courseId': course_id}).json()
    lesson_ids = list(lesson['id'] for lesson in lessons)
    return lesson_ids


def get_material_id(s, lesson_id):
    url = 'https://lyceum.yandex.ru/api/materials'
    material_info = s.get(url, params={'lessonId': lesson_id}).json()
    if material_info:
        material = material_info[0]
        if material['type'] != 'textbook':
            print(material_info)
            raise ValueError
        return material['id']
    else:
        return 0


def get_material_html(s, lesson_id, group_id, material_id):
    url = f"https://lyceum.yandex.ru/api/student/materials/{material_id}"
    material = s.get(url, params={'groupId': group_id, 'lessonId': lesson_id}).json()
    material_html = material['detailedMaterial']['content']
    return material_html


def get_all_tasks(s, lesson_id, course_id):
    url = 'https://lyceum.yandex.ru/api/student/lessonTasks'
    lesson_info = s.get(url, params={'courseId': course_id, 'lessonId': lesson_id}).json()
    return lesson_info


def get_lesson_info(s, lesson_id, group_id, course_id):
    url = f'https://lyceum.yandex.ru/api/student/lessons/{lesson_id}'
    lesson_info = s.get(url, params={'groupId': group_id, 'courseId': course_id}).json()
    return lesson_info


def get_solution(s, solution_id):
    url = f'https://lyceum.yandex.ru/api/student/solutions/{solution_id}'
    solution = s.get(url).json()
    return solution


def get_courses_groups_ids(s):
    url = r'https://lyceum.yandex.ru/api/profile'
    courses = s.get(url=url, params={'onlyActiveCourses': True,
                                     'withCoursesSummary': True,
                                     'withExpelled': True}).json()
    courses = courses['coursesSummary']['student']
    ids = list({'title': course['title'],
                'rating': course['rating'],
                'course_id': course['id'],
                'group_id': course['group']['id']}
               for course in courses)
    return ids


def get_course(s):
    courses = get_courses_groups_ids(s)
    print("\nВыберите курс")
    print(*list(f"{course['title']} - {n}" for n, course in enumerate(courses)), sep='\n')
    n = input()
    while not (n.isdigit() and -1 < int(n) < len(courses)):
        print("Ошибка. Введите только число")
        n = input()
    course = courses[int(n)]
    return course['course_id'], course['group_id'], course['rating']