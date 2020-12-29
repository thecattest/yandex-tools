from collections import defaultdict

from api import *

user = User().load_credentials().auth
course_id, group_id, rating = user.get_course(with_rating=True)
lesson_ids = user.get_lesson_ids(course_id, group_id)

primary_points_unchecked = defaultdict(int)
primary_points_all = defaultdict(int)
lessons_with_work_type = defaultdict(int)

for lesson_id in lesson_ids:
    tasks_groups = user.get_all_tasks(lesson_id, course_id)
    for tasks_group in tasks_groups:
        lessons_with_work_type[tasks_group['type']] += 1
        for task in tasks_group['tasks']:
            if (sol := task['solution']) and sol['status']['type'] == 'review':
                primary_points_unchecked[task['tag']['type']] += task['scoreMax']

classwork_score_unchecked = (primary_points_unchecked['classwork'] / 100) * (10 / lessons_with_work_type['classwork'])
homework_score_unchecked = (primary_points_unchecked['homework'] / 100) * (10 / lessons_with_work_type['homework'])
additional_score_unchecked = (primary_points_unchecked['additional'] / 100) * (
            40 / lessons_with_work_type['additional'])

impulse_score = classwork_score_unchecked + homework_score_unchecked + additional_score_unchecked

print('Непроверенные задачи:')
print(f"Классные задачи:\t{primary_points_unchecked['classwork']:.2f} {classwork_score_unchecked:.2f}")
print(f"Домашние задачи:\t{primary_points_unchecked['homework']:.2f} {homework_score_unchecked:.2f}")
print(f"Дополнительные задачи:\t{primary_points_unchecked['additional']:.2f} {additional_score_unchecked:.2f}")

print('--------------------------')

print(f'Баллы без проверки:\t{rating:.2f}')
print(f'Баллы для проверки:\t{impulse_score}')
print(f'Баллы с проверкой:\t{rating + impulse_score:.2f}')
print()
input('Жмякай Enter')
