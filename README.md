### Newecom Notifier
Monitor the registration status in http://newecom.fci-cu.edu.eg/ and post to a Discord webhook when the registration starts

## Running
```shell
$ pip install requests
$ cp secrets.py.sample secrets.py
```
and edit `secrets.py` with your own data then:
```shell
$ python3 main.py
```
