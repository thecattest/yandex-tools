import requests

titles = {'classwork': 'Классная работа',
          'homework': 'Домашняя работа',
          'additional': 'Дополнительные задачи',
          'additional-2': 'Дополнительные задачи 2 уровень',
          'additional-3': 'Итоговая контрольная',
          'control-work': 'Контрольная работа',
          'another': 'Другое',
          'individual-work': 'Самостоятельная работа'}


def auth(s, login, password):
    auth = s.post('https://passport.yandex.ru/passport?mode=auth',
                  data={'login': login, 'passwd': password})
    if auth.url == 'https://passport.yandex.ru/profile':
        print('Авторизация прошла успешно')
        print('===========\n')
    elif 'Неправильный' in auth.text:
        raise Exception('Неправильные логин или пароль')
    else:
        raise Exception('Ошибка X')


def get_and_auth():
    try:
        with open('credentials.txt') as file:
            login, password = file.read().split()
    except FileNotFoundError:
        print("Файл с логином и паролем не найден.\n"
              "Создайте файл 'credentials.txt' и сохраните в нем логин и пароль, разделённые пробелом.\n"
              "Так, во-первых, вам не придётся каждый раз его вводить.\n"
              "Во-вторых, даже если рядом и будет кто-то стоять, ваши данные в безопасности.\n"
              "Файл добавлен в .gitignore, так что с ним точно ничего не случится.")
        exit(1)
    s = requests.Session()
    auth(s, login, password)
    return s


def get_lesson_ids(s, course_id, group_id):
    url = 'https://lyceum.yandex.ru/api/student/lessons'
    lessons = s.get(url, params={'groupId': group_id, 'courseId': course_id}).json()
    return [lesson['id'] for lesson in lessons]


def get_material_id(s, lesson_id):
    url = 'https://lyceum.yandex.ru/api/materials'
    if not (
            material_info := s.get(url, params={'lessonId': lesson_id}).json()
    ):
        return 0
    material = material_info[0]
    if material['type'] != 'textbook':
        print(material_info)
        raise ValueError
    return material['id']


def get_material_html(s, lesson_id, group_id, material_id):
    url = f"https://lyceum.yandex.ru/api/student/materials/{material_id}"
    material = s.get(url, params={'groupId': group_id, 'lessonId': lesson_id}).json()
    return material['detailedMaterial']['content']


def get_all_tasks(s, lesson_id, course_id):
    url = 'https://lyceum.yandex.ru/api/student/lessonTasks'
    return s.get(url, params={'courseId': course_id, 'lessonId': lesson_id}).json()


def get_task(s, task_id, group_id):
    url = f'https://lyceum.yandex.ru/api/student/tasks/{task_id}'
    return s.get(url, params={'groupId': group_id}).json()


def get_lesson_info(s, lesson_id, group_id, course_id):
    url = f'https://lyceum.yandex.ru/api/student/lessons/{lesson_id}'
    return s.get(url, params={'groupId': group_id, 'courseId': course_id}).json()


def get_all_lessons(s, course_id, group_id):
    url = 'https://lyceum.yandex.ru/api/student/lessons'
    params = {'courseId': course_id,
              'groupId': group_id,
              'code': 200}
    return s.get(url, params=params).json()


def get_solution(s, solution_id):
    url = f'https://lyceum.yandex.ru/api/student/solutions/{solution_id}'
    return s.get(url).json()


def get_notifications(s):
    url = 'https://lyceum.yandex.ru/api/notifications'
    return s.get(url).json()


def get_courses_groups_ids(s):
    url = r'https://lyceum.yandex.ru/api/profile'
    courses = s.get(url=url, params={'onlyActiveCourses': True,
                                     'withCoursesSummary': True,
                                     'withExpelled': True}).json()
    courses = courses['coursesSummary']['student']
    return [{'title': course['title'],
             'rating': course['rating'],
             'course_id': course['id'],
             'group_id': course['group']['id']} for course in courses]


def get_course(s, with_rating=False):
    courses = get_courses_groups_ids(s)
    print("Выберите курс")
    print(
        *[f"{course['title']} - {n}" for n, course in enumerate(courses)],
        sep='\n',
    )

    n = input()
    while not (n.isdigit() and -1 < int(n) < len(courses)):
        print("Ошибка. Введите только число")
        n = input()
    print('===========\n')
    course = courses[int(n)]
    if with_rating:
        return course['course_id'], course['group_id'], course['rating']
    else:
        return course['course_id'], course['group_id']
