import time
import requests
import secrets

REGISTRATION_DATA = [
    'maxElectiveHours',
    'maxMandatoryHours',
    'maxRegisteredHoursPerTerm',
    'minRegisteredHoursPerTerm',
    'pendingCourses'
]


if __name__ == '__main__':
    auth_token = None
    no_trials = 0
    total_time_since_reset = 0
    while True:
        print(f'Trial #{no_trials}')
        try:
            if auth_token is None or total_time_since_reset >= secrets.RESET_TOKEN_INTERVAL:
                # Refresh auth_token
                total_time_since_reset = 0
                authentication_res = requests.post('http://newecom.fci-cu.edu.eg/api/authenticate', json={
                    'username': secrets.STUDENT_ID,
                    'password': secrets.STUDENT_PASSWORD
                })
                authentication_json = authentication_res.json()
                if 'AuthenticationException' in authentication_json:
                    print('Authentication error')
                    break
                auth_token = authentication_res.json()['id_token']
                print("Refreshed auth token")

            registration_res = requests.get(
                f'http://newecom.fci-cu.edu.eg/api/student-courses-eligible',
                params={
                    'studentId': secrets.STUDENT_ID
                },
                headers={
                    'Authorization': f'Bearer {auth_token}'
                }
            )
            registration_json = registration_res.json()
            print(registration_json)
            if any(registration_json[i] is not None for i in REGISTRATION_DATA):
                print('Registration has started')
                break
            print('Registration has not started')
        except requests.exceptions.Timeout:
            print('Timeout Error')
        except requests.exceptions.ConnectionError:
            print('Connection error')
        except Exception as error:
            print("Unknown error")
            print(error)
            time.sleep(secrets.INTERVAL)

        no_trials += 1
        total_time_since_reset += secrets.INTERVAL
        time.sleep(secrets.INTERVAL)
