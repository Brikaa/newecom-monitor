import requests
import secrets
from main_loop import main_loop


REGISTRATION_DATA = [
    'maxElectiveHours',
    'maxMandatoryHours',
    'maxRegisteredHoursPerTerm',
    'minRegisteredHoursPerTerm',
    'pendingCourses'
]


def has_registration_started(registration_json):
    if any(registration_json[i] is not None for i in REGISTRATION_DATA):
        print('Registration has started')
        return True
    print('Registration has not started')
    return False


if __name__ == '__main__':
    main_loop(has_registration_started)
