# mail-queue-api
Mail queue API for exim/postfix server

forked from https://github.com/icetemple/exim-api

credit: pleshevskiy 

The API server is to provide mail queue information of exim/postfix  
It supports postfix and exim. Please check config.py to configure the mail server  


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
check if the email address is routable to destination from mail server's perspective

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

tested in  
Exim 4.92.3  
postfix  3.3.0 (probably work in 2.10.x)  

# Installation 
run as root
```
cd /opt
git clone https://github.com/georgekcchung/mail-queue-api.git
pip3 install pipenv
useradd mail-queue-api
```

run as mail-queue-api user
```
cd /opt/mail-queue-api/
/usr/local/bin/pipenv install
```

edit gunicorn.conf.py and config.py for binding IP address  
change mailServer variable in config.py for correct mail server support  

## Run in commandline:
/usr/local/bin/pipenv run gunicorn -c gunicorn.conf.py flasky:app

## Run as service in systemd:

add mail-queue-api.service in /lib/systemd/system
```
[Unit]
Description=My Python Service
After=network.target

[Service]
User=mail-queue-api
Restart=always
Type=simple
WorkingDirectory=/opt/mail-queue-api
ExecStart=/usr/local/bin/pipenv run gunicorn -c gunicorn.conf.py flasky:app

[Install]
WantedBy=multi-user.target
```

```
systemctl daemon-reload
add exim group to mail-queue-api user by editting /etc/group file
systemctl start mail-queue-api
```
## speed up with Meinheld,  a high-performance WSGI-compliant web server, optional
run as root
```
yum group install "Development Tools"
yum install python36-devel
```
run as mail-queue-api user
```
/usr/local/bin/pipenv shell
pip3 install meinheld
```
run as root

edit /lib/systemd/system/mail-queue-api.service

change ExecStart to

/usr/local/bin/pipenv run gunicorn --worker-class="egg:meinheld#gunicorn_worker" -c gunicorn.conf.py flasky:app

systemctl daemon-reload

systemctl restart mail-queue-api

