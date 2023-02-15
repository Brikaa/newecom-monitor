### Newecom Notifier

Monitor the registration status in http://newecom.fci-cu.edu.eg/

## Running

```shell
$ pip install requests
$ cp secrets.py.sample secrets.py
```

and edit `secrets.py` with your own data then:

```shell
$ python3 main.py
```

The process will exit with 0 status once done. You can chain it with other commands like:

```shell
$ python3 main.py && python3 extras/discord_webhook.py WEBHOOK_URL MESSAGE && notify-send "Registration has started"
```
