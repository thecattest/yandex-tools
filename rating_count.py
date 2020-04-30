import requests
from collections import defaultdict
import sys

assert sys.version_info >= (3, 8), "Нужен Python 3.8 или выше!"
print('Для корректного вычисления рейтинга должны быть открыты все уроки!')
login = input('Login: ')
password = input('Password: ')

primary_points_unchecked = defaultdict(int)
primary_points_all = defaultdict(int)

s = requests.Session()
auth = s.post(
    'https://passport.yandex.ru/passport?mode=auth',
    data={'login': login, 'passwd': password}
)
if auth.url == 'https://passport.yandex.ru/profile':
    print('Авторизация прошла успешно')
    print('--------------------------')
else:
    if 'Неправильный' in auth.text:
        raise Exception('Неправильные логин или пароль')
    raise Exception('Неизвестная ошибка авторизации')

courses = s.get(
    url='https://lyceum.yandex.ru/api/profile',
    params={
        'onlyActiveCourses': True,
        'withCoursesSummary': True,
        'withExpelled': True
    }
).json()['coursesSummary']['student']

for c in courses:
    if 'Основы программирования на языке Python' in c['title']:
        course = c
        break
else:
    raise Exception('Курс не найден')

course_id = course['id']
group_id = course['group']['id']

lessons = s.get(
    url='https://lyceum.yandex.ru/api/student/lessons',
    params={'courseId': course_id, 'groupId': group_id}
).json()

lessons_with_work_type = defaultdict(int)

for lesson in lessons:
    lesson_id = lesson['id']
    tasks_groups = s.get(
        'https://lyceum.yandex.ru/api/student/lessonTasks',
        params={'courseId': course_id, 'lessonId': lesson_id}
    ).json()
    for tasks_group in tasks_groups:
        lessons_with_work_type[tasks_group['type']] += 1
        for task in tasks_group['tasks']:
            if (sol := task['solution']) and sol['status']['type'] == 'review':
                primary_points_unchecked[task['tag']['type']] += task['scoreMax']
            primary_points_all[task['tag']['type']] += task['scoreMax']

rating = course['rating']

rating_all = (primary_points_all['classwork'] / 100) * (10 / lessons_with_work_type['classwork']) \
             + (primary_points_all['homework'] / 100) * (10 / lessons_with_work_type['homework']) \
             + (primary_points_all['additional'] / 100) * (40 / lessons_with_work_type['additional']) \
             + (primary_points_all['individual-work'] / 100) * (20 / lessons_with_work_type['individual-work']) \
             + (primary_points_all['control-work'] / 100) * (40 / lessons_with_work_type['control-work'])

classwork_score_unchecked = (primary_points_unchecked['classwork'] / 100) * (10 / lessons_with_work_type['classwork'])
homework_score_unchecked = (primary_points_unchecked['homework'] / 100) * (10 / lessons_with_work_type['homework'])
additional_score_unchecked = (primary_points_unchecked['additional'] / 100) * (40 / lessons_with_work_type['additional'])

impulse_score = classwork_score_unchecked + homework_score_unchecked + additional_score_unchecked

print('Непроверенные задачи:')
print(f"Классные задачи:       {primary_points_unchecked['classwork']:.2f} {classwork_score_unchecked:.2f}")
print(f"Домашние задачи:       {primary_points_unchecked['homework']:.2f} {homework_score_unchecked:.2f}")
print(f"Дополнительные задачи: {primary_points_unchecked['additional']:.2f} {additional_score_unchecked:.2f}")

print('--------------------------')

print(f'Баллы без проверки: {rating:.2f}')
print(f'Баллы для проверки: {impulse_score}')
print(f'Баллы с проверкой:  {rating + impulse_score:.2f}')
print(dict(primary_points_all))
print(f'Возможные баллы с проверкой: {rating_all:.2f}')
input('Жмякай Enter')