import os


bind = '192.168.0.71:4000'
workers = os.getenv('GUNICORN_WORKERS', 10)
errorlog = '-'
reload = True
