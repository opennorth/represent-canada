import os.path

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

workers = 5

worker_class = 'eventlet'

bind = '127.0.0.1:59000'

pidfile = os.path.join(BASE_DIR, 'gunicorn.pid')

errorlog = os.path.join(BASE_DIR, 'logs', 'gunicorn-error.log')

proc_name = 'represent'
