# /home/represent/gunicorn_settings.py

workers = 8

worker_class = 'eventlet'

bind = '127.0.0.1:59000'

pidfile = '/home/represent/gunicorn.pid'

errorlog = '/home/represent/logs/gunicorn-error.log'

proc_name = 'represent'
