from pprint import pprint
import datetime
from methods import *


s = get_and_auth()
course_id, group_id, rating = get_course(s)
lesson_ids = get_lesson_ids(s, course_id, group_id)

for lesson_id in lesson_ids:
    lesson = get_lesson_info(s, lesson_id, group_id, course_id)
    now = datetime.datetime.now().isoformat()
    if now > lesson['deadline']:
        continue
    all_tasks = get_all_tasks(s, lesson_id, course_id)
    for task_type in all_tasks:
        type_title = titles[task_type['type']]
        for task in task_type['tasks']:
            if not task['solution'] is None:
                continue
            task_id = task['id']
            lesson_title = task['lesson']['title']
            task_title = task['title']
            link = f"https://lyceum.yandex.ru/courses/{course_id}/groups/{group_id}/lessons/{lesson_id}/tasks/{task_id}"
            print(f"\"{lesson_title}\" -  {type_title} - {task_title}\n {link}", end='\n=====\n')
