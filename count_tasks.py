from methods import *
from collections import defaultdict


s = get_and_auth()
course_id, group_id, rating = get_course(s)

lesson_ids = get_lesson_ids(s, course_id, group_id)
tasks_number = defaultdict(int)
scores = defaultdict(int)


for lesson_id in lesson_ids:
    lesson_info = get_all_tasks(s, lesson_id, course_id)
    for task_group in lesson_info:
        for task in task_group['tasks']:
            type = task['tag']['type']
            score = task['scoreMax']
            tasks_number[type] += 1
            scores[type] += score

tasks_number['control-work'] += tasks_number['additional-3']
del tasks_number['additional-3']
scores['control-work'] += scores['additional-3']
del scores['additional-3']

print("=========\n")
print("Количество задач\n")
print(*list(f"{titles[key]}:\t{item}" for key, item in tasks_number.items()), sep='\n')
print("=========\n")
print("Первичные баллы\n")
print(*list(f"{titles[key]}:\t{item}" for key, item in scores.items()), sep='\n')

input('Жмякай Enter')