from methods import *


try:
    s = get_and_auth()

    notifications = get_notifications(s)
    errors = dict()
    for one_id in notifications['notificationMap']:
        one = notifications['notificationMap'][one_id]
        if one['type'] == "submission-checked":
            if one['objectData']['verdict'] != 'ok':
                error = one['objectData']['verdict']
                errors[error] = errors.get(error, 0) + 1

    print('===========\n')
    for one in sorted(errors.items(), reverse=True, key=lambda x: x[1]):
        print(f"{one[0]}\t{one[1]}")
except IndexError as e:
    print(e)
    print(type(e))
print('\n')
input('Жмякай Enter')