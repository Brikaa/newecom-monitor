import time
import requests
import secrets
from typing import Callable
from datetime import datetime


def main_loop(change_checker: Callable[[str], bool]):
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
                })
                authentication_json = authentication_res.json()
                if 'AuthenticationException' in authentication_json:
                    print('Authentication error')
                    sys.exit(1)
                auth_token = authentication_res.json()['id_token']
                print("Refreshed auth token")

            if change_checker(auth_token):
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
