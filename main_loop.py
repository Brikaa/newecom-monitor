import time
import requests
import secrets
from typing import Callable
from datetime import datetime


def main_loop(change_checker: Callable[[dict], bool]):
    auth_token = None
    no_trials = 0
    time_since_last_reset = datetime.now()
    while True:
        print(f'Trial #{no_trials}')
        try:
            if auth_token is None or (datetime.now() - time_since_last_reset).seconds >= secrets.RESET_TOKEN_INTERVAL:
                # Refresh auth_token
                time_since_last_reset = datetime.now()
                authentication_res = requests.post('http://newecom.fci-cu.edu.eg/api/authenticate', json={
                    'username': secrets.STUDENT_ID,
                    'password': secrets.STUDENT_PASSWORD
                }, timeout=secrets.TIMEOUT)
                authentication_json = authentication_res.json()
                if 'AuthenticationException' in authentication_json:
                    print('Authentication error')
                    sys.exit(1)
                auth_token = authentication_res.json()['id_token']
                print("Refreshed auth token")

            registration_res = requests.get(
                f'http://newecom.fci-cu.edu.eg/api/student-courses-eligible',
                params={
                    'studentId': secrets.STUDENT_ID
                },
                headers={
                    'Authorization': f'Bearer {auth_token}'
                },
                timeout=secrets.TIMEOUT
            )
            registration_json = registration_res.json()
            print(registration_json)

            if change_checker(registration_json):
                break

        except requests.exceptions.Timeout:
            print('Timeout Error')
        except requests.exceptions.ConnectionError:
            print('Connection error')
        except Exception as error:
            print("Unknown error")
            print(error)
            time.sleep(secrets.INTERVAL)

        no_trials += 1
        time.sleep(secrets.INTERVAL)
