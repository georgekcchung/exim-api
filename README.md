# exim-api
API for exim server

forked from https://github.com/icetemple/exim-api

credit: pleshevskiy 

The API server is to provide mail queue information of exim by API


# API documentation
---
Get mail queue information

GET /queue
response:
```
{
  "code": 0,
  "message": "OK",
  "queue": [
    {
      "mailSize": "695",
      "messageId": "1jJjLG-0000AG-2Y",
      "queueTime": "3d",
      "status": "frozen",
      "toAddress": "<root@>"
    },
    {
      "mailSize": "695",
      "messageId": "1jK5Mj-0003Ag-PV",
      "queueTime": "60h",
      "status": "frozen",
      "toAddress": "<root@>"
    }
  ]
}
```

---
Get mail queue count

GET /queue/count

response:
```
{
  "code": 0,
  "count": 9,
  "message": "OK"
}
```


---
Get messageId in the mail queue

GET /queue/messageId/<messageId>
response:

```
{
  "code": 0,
  "message": "found",
  "queue": [
    {
      "mailSize": "2.5K",
      "messageId": "1jKtdt-0003vq-EI",
      "queueTime": "6h",
      "status": "frozen",
      "toAddress": "<>"
    }
  ]
}
```
if the response code is 404, it means the messageId is not found in the mailqueue It could mean the mail was sent successfully.

---
Get healthcheck information

GET /
GET /healthcheck

response:
```
{
  "code": 0,
  "message": "OK"
}
```

---
check if the email address is routable to destination from exim's perspective

POST /check/route/

request payload
```
{ "email" : "email@domain.com" }
```

response:
```
{
  "code": 0,
  "message": "found routable"
}
```

# Requirement:
Python 3.6 (3.4-3.8 could work)
OS: CentOS 8.1 ( CentOS 7 should also work)

# Installation 
run as root
```
pip3 install pipenv
useradd exim-api
```

run as exim-api user
```
cd exim-api/
/usr/local/bin/pipenv install
```

edit gunicorn.conf.py and config.py for binding IP address

## Run in commandline:
/usr/local/bin/pipenv run gunicorn -c gunicorn.conf.py flasky:app

## Run as service in systemd:

add exim-api.service in /lib/systemd/system
```
[Unit]
Description=My Python Service
After=network.target

[Service]
User=exim-api
Restart=always
Type=simple
WorkingDirectory=/opt/exim-api
ExecStart=/usr/local/bin/pipenv run gunicorn -c gunicorn.conf.py flasky:app

[Install]
WantedBy=multi-user.target
```

```
systemctl daemon-reload
systemctl start exim-api
```
