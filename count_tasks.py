import requests
from methods import *


s = requests.Session()

login = input('Login: ')
password = input('Password: ')
auth(s, login, password)

ids = get_courses_groups_ids(s)[1]
course_id = ids['course_id']
group_id = ids['group_id']

lesson_ids = get_lesson_ids(s, course_id, group_id)
points = dict()

for lesson_id in lesson_ids:
    lesson_info = get_all_tasks(s, lesson_id, course_id)
    for tasks in lesson_info:
        n = len(tasks['tasks'])
        type = tasks['type']
        if type in points:
            points[type] += n
        else:
            points[type] = n


print(points)
