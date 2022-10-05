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


def post_to_webhook():
    requests.post(secrets.WEBHOOK_URL, json={
        'content': '@everyone registration has started'
    })


if __name__ == '__main__':
    i = 0
    while True:
        print(f'Trial #{i}')
        try:
            authentication_res = requests.post('http://newecom.fci-cu.edu.eg/api/authenticate', json={
                'username': secrets.STUDENT_ID,
                'password': secrets.STUDENT_PASSWORD
            })
            authentication_json = authentication_res.json()

            if 'AuthenticationException' in authentication_json:
                print('Authentication error')
                print(authentication_json)
                break

            auth_token = authentication_res.json()['id_token']
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
                post_to_webhook()
                break
            print('Registration has not started')
            i += 1
            time.sleep(15)
        except TimeoutError:
            print('Timeout Error')
            continue
        except ConnectionError:
            print('Connection error')
            continue