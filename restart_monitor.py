import requests
from main_loop import main_loop


registered_courses_count = None


def has_registration_restarted(registration_json):
    global registered_courses_count
    if 'registeredCourses' not in registration_json:
        print('No registered courses')
        return True
    registered_courses = registration_json['registeredCourses']
    print(f'Registered courses count: {len(registered_courses)}')
    if registered_courses_count is None:
        registered_courses_count = len(registered_courses)
        return False
    return len(registered_courses) != registered_courses_count


if __name__ == '__main__':
    main_loop(has_registration_restarted)
