import os


bind = '0.0.0.0:4000'
workers = os.getenv('GUNICORN_WORKERS', 10)
errorlog = '-'
reload = True
