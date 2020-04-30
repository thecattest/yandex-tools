from methods import *
import os


style = '<head><link rel="stylesheet" href="https://yastatic.net/s3/lyceum/frontend/static/40.0-rc-39c44ae1/desktop-ru/client.css"><link rel="stylesheet" href="https://yastatic.net/s3/lyceum/frontend/static/40.0-rc-39c44ae1/desktop-ru/material.css"><link rel="stylesheet" type="text/css" href="https://yastatic.net/s3/lyceum/frontend/static/40.0-rc-39c44ae1/desktop-ru/code-mirror-editor.css"><link rel="stylesheet" href="https://yastatic.net/s3/lyceum/frontend/static/40.0-rc-39c44ae1/desktop-ru/vendors.css"></head>'
symb = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
global n

def save_lesson(lesson, lesson_title, dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
    if not lesson:
        return
    lesson_path = os.path.join(dir, lesson_title)
    os.mkdir(lesson_path)

    material = lesson['material']
    save_material(lesson_path, material)

    for type in lesson['tasks']:
        tasks = lesson['tasks'][type]
        type_path = os.path.join(lesson_path, type)
        save_task_type(tasks, type_path)


def save_material(lesson_path, material):
    for enc in ['utf-8', 'windows-1252', 'windows-1250', 'ascii']:
        try:
            material = style + material.replace('\n', '')
            with open(os.path.join(lesson_path, 'material.html'), 'wt', encoding=enc) as html:
                html.write(material)
            break
        except UnicodeEncodeError:
            print("Материал не получилось сохранить из-за Unicode ошибки")
            print("Пробую другую кодировку...")


def save_task_type(tasks, type_path):
    os.mkdir(type_path)
    for title in tasks:
        solution_path = os.path.join(type_path, title)
        task = tasks[title]
        save_task(solution_path, task)


def save_task(solution_path, task):
    code, encoding, byte = task
    try:
        if byte:
            with open(solution_path, 'wb') as file:
                file.write(code)
        else:
            for enc in ['utf-8', 'windows-1252', 'windows-1250', 'ascii']:
                try:
                    with open(solution_path, 'wt', encoding=enc) as file:
                        file.write(code)
                    break
                except Exception:
                    print("Материал не получилось сохранить из-за Unicode ошибки")
                    print("Пробую другую кодировку...")
    except Exception as e:
        print(e, solution_path, code, encoding, sep='\n', end='\n\n\n\n===================\n')


def get_dir():
    dir = input('Директория для сохранения решений: ')
    for sym in symb:
        dir = dir.replace(sym, ' ')
    print('(пожалуйста будьте sure что папки не существует или она пустая, \nа иначе я за себя не ручаюсь)')
    return dir


def get_ids():
    global n, s
    course_id, group_id, rating = get_course(s)
    lesson_ids = get_lesson_ids(s, course_id, group_id)
    n = len(lesson_ids)
    return course_id, group_id, lesson_ids


def download_lesson(lesson_n, lesson_id):
    lesson_title = get_lesson_info(s, lesson_id, group_id, course_id)['title']
    lesson_title = str(n - lesson_n) + '. ' + lesson_title
    for sym in symb:
        lesson_title = lesson_title.replace(sym, ' ')

    material_id = get_material_id(s, lesson_id)
    if material_id:
        material_html = get_material_html(s, lesson_id, group_id, material_id)
    else:
        material_html = ''

    lesson = {'material': material_html, 'tasks': {}}
    all_tasks = get_all_tasks(s, lesson_id, course_id)

    for tasks_type in all_tasks:
        lesson = download_type(lesson, tasks_type)

    return lesson, lesson_title


def download_type(lesson, tasks_type):
    type = tasks_type['type']
    type_title = titles[type]
    lesson['tasks'][type_title] = dict()

    for task in tasks_type['tasks']:
        lesson = download_task(lesson, task, type_title)

    return lesson


def download_task(lesson, task, type_title):
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
            lesson['tasks'][type_title][task_title + '.' + file_type] = [code, encoding, byte]

    return lesson


s = get_and_auth()
dir = get_dir()
course_id, group_id, lesson_ids = get_ids()

for lesson_n, lesson_id in enumerate(lesson_ids):
    lesson, lesson_title = download_lesson(lesson_n, lesson_id)

    try:
        print(f"Урок \"{lesson_title}\" скачан")
    except UnicodeError:
        print('unicode error, i dont know what to do', lesson_n)
    save_lesson(lesson, lesson_title, dir)
    try:
        print(f"Урок \"{lesson_title}\" сохранён")
    except UnicodeError:
        print('unicode error, i dont know what to do', lesson_n)

print('\n\n\n\nf r o m: https://github.com/ilya-vodopyanov/yandex-tools')

input('Жмякай Enter')
