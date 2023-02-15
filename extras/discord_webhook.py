import sys
import requests

if __name__ == '__main__':
    webhook_url = sys.argv[1]
    message = sys.argv[2]
    requests.post(webhook_url, json={'content': message})
