from collections import defaultdict

from yandex_lyceum_api import User, TITLES

user = User().load_credentials().auth()
course_id, group_id = user.get_course()

lesson_ids = user.get_lesson_ids(course_id, group_id)
tasks_number = defaultdict(int)
task_groups_number = defaultdict(int)
scores = defaultdict(int)

for lesson_id in lesson_ids:
    lesson_info = user.get_all_tasks(lesson_id, course_id)
    for task_group in lesson_info:
        task_groups_number[task_group['type']] += 1
        for task in task_group['tasks']:
            type = task['tag']['type']
            score = task['scoreMax']
            tasks_number[type] += 1
            scores[type] += score

print("Количество задач\n")
print(*(f"{TITLES[key]}:\t{item}" for key, item in tasks_number.items()), sep='\n')
print("=========\n")

print("Количество блоков\n")
print(*(f"{TITLES[key]}:\t{item}" for key, item in task_groups_number.items()), sep='\n')
print("=========\n")

print("Первичные баллы\n")
print(*(f"{TITLES[key]}:\t{item}" for key, item in scores.items()), sep='\n')

input('\nЖмякай Enter')
