import requests
from pprint import pprint
import os

from methods import *


def save_solutions(solutions, dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
    for lesson_title in solutions:
        if not solutions[lesson_title]:
            continue
        lesson_path = os.path.join(dir, lesson_title)
        os.mkdir(lesson_path)
        for type in solutions[lesson_title]:
            type_path = os.path.join(lesson_path, type)
            os.mkdir(type_path)
            for title in solutions[lesson_title][type]:
                solution_path = os.path.join(type_path, title)
                code, encoding, byte = solutions[lesson_title][type][title]
                if byte:
                    with open(solution_path, 'wb') as file:
                        file.write(code)
                else:
                    with open(solution_path, 'wt', encoding=encoding) as file:
                        file.write(code)


s = requests.Session()
login = input('Login: ')
password = input('Password: ')
dir = input('Директория для сохранения решений: ')
print('(пожалуйста будьте sure что папки не существует или она пустая, \nа иначе я за себя не ручаюсь)')
auth(s, login, password)

ids = get_courses_groups_ids(s)[1]
course_id = ids['course_id']
group_id = ids['group_id']

lesson_ids = get_lesson_ids(s, course_id, group_id)[20:24]
solutions = dict()
titles = {'classwork': 'Классная работа',
          'homework': 'Домашняя работа',
          'additional': 'Дополнительные задачи',
          'control-work': 'Контрольная',
          'individual-work': 'Самостоятельная работа'}
symb = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']

for lesson_id in lesson_ids:
    title = get_lesson_info(s, lesson_id, group_id, course_id)['title']
    solutions[title] = {}
    all_tasks = get_all_tasks(s, lesson_id, course_id)

    for tasks_type in all_tasks:
        type = tasks_type['type']
        type_title = titles[type]
        solutions[title][type_title] = dict()

        for task in tasks_type['tasks']:
            if not task['solution'] is None:
                task_solution = get_solution(s, task['solution']['id'])
                task_title = task['title']
                file = task_solution['file']
                if not file is None:
                    encoding = file['encoding']
                    file_type = os.path.split(file['name'])[1].split('.')[-1]
                    if file_type == 'py':
                        code = file['sourceCode'].replace('\n', '')
                        byte = 0
                    else:
                        code = requests.get(file['url']).content
                        byte = 1
                    for sym in symb:
                        task_title = task_title.replace(sym, ' ')
                    solutions[title][type_title][task_title + '.' + file_type] = [code, encoding, byte]
    print(f"Урок \"{title}\" скачан")

save_solutions(solutions, dir)
