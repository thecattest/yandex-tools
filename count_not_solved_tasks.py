import requests
import datetime
from methods import *


s = requests.Session()

login = input('Login: ')
password = input('Password: ')
course = int(input('Your course(1/2): ')) - 1
auth(s, login, password)

ids = get_courses_groups_ids(s)[course]
course_id = ids['course_id']
group_id = ids['group_id']

lesson_ids = get_lesson_ids(s, course_id, group_id)
points = dict()

for lesson_id in lesson_ids:
    all_tasks = get_all_tasks(s, lesson_id, course_id)
    for task_type in all_tasks:
        type_title = titles[task_type['type']]
        for task in task_type['tasks']:
            if not task['solution'] is None:
                continue
            now = datetime.datetime.now().isoformat()
            if now > task['deadline']:
                break
            task_id = task['id']
            lesson_title = task['lesson']['title']
            task_title = task['title']
            link = f"https://lyceum.yandex.ru/courses/{course_id}/groups/{group_id}/lessons/{lesson_id}/tasks/{task_id}"
            print(f"\"{lesson_title}\" -  {type_title} - {task_title}\n {link}", end='\n=====\n')
