import json
from main_loop import main_loop

registered_courses_json = None

def has_response_changed(registration_json):
    global registered_courses_json

    registration_json.pop('registeredCourses')
    registered_courses_response = json.dumps(registration_json)
    if registered_courses_json is None:
        registered_courses_json = registered_courses_response
    if registered_courses_response == registered_courses_json:
        print('Response has not changed')
        return False
    else:
        print('Response has changed')
        return True

if __name__ == '__main__':
    main_loop(has_response_changed)
