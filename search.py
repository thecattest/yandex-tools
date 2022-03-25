from methods import *
from Errors import (ForbiddenError)


def search_tasks(lessons, search_part):
    found = []
    search_part = search_part.lower()

    for lesson_title, tasks in lessons:
        for tasks_group in tasks:
            for task in tasks_group['tasks']:
                task_title = task['title']
                if search_part in task_title.lower():
                    if not (sol := task['solution']):
                        found.append((lesson_title, task_title, False))
                    else:
                        found.append((lesson_title, task_title, bool(sol['score'])))
    return found


def prepare(s, course_id, group_id):
    lessons = []
    print("Получаю информацию об уроках, это занимает примерно 5-10 секунд...")
    lessons_info = get_all_lessons(s, course_id, group_id)
    if lessons_info['code'] != 200:
        raise ForbiddenError(lessons_info['code'])
    for lesson in lessons_info:
        lesson_title = lesson['title']
        lesson_id = lesson['id']
        tasks = get_all_tasks(s, lesson_id, course_id)
        lessons.append([lesson_title, tasks])
    print("Закончил")
    print("===========\n")
    return lessons


if __name__ == '__main__':
    s = get_and_auth()
    course_id, group_id = get_course(s)

    lessons = prepare(s, course_id, group_id)

    print(r'Для остановки ввода введите \\')
    print("Часть названия задачи, которую нужно найти: ")
    search_part = input()

    while search_part != r'\\':
        fd = search_tasks(lessons, search_part)
        if not fd:
            print('Не удалось найти задачу')
        else:
            for lesson_name, task_title_full, is_solved in fd:
                print(f'Урок: "{lesson_name}", Задача: "{task_title_full}" '
                      f'({"" if is_solved else "не"} решена)')
        print('===========\n')

        print(r'Для остановки ввода введите \\')
        print("Часть названия задачи, которую нужно найти: ")
        search_part = input()
