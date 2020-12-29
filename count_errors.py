from api import *

try:
    user = User().load_credentials().auth()

    notifications = user.get_notifications()
    errors = dict()
    for one_id in notifications['notificationMap']:
        one = notifications['notificationMap'][one_id]
        if one['type'] == "submission-checked" and one['objectData']['verdict'] != 'ok':
            error = one['objectData']['verdict']
            errors[error] = errors.get(error, 0) + 1

    for one in sorted(errors.items(), reverse=True, key=lambda x: x[1]):
        print(f"{one[0]}\t{one[1]}")
except IndexError as e:
    print(e)
    print(type(e))
print()
input('Жмякай Enter')
