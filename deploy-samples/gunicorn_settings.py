import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

try:
    NUM_CPUS = os.sysconf('SC_NPROCESSORS_ONLN')
except:
    NUM_CPUS = 2

bind = '127.0.0.1:10101'

workers = (NUM_CPUS * 2) + 1

pidfile = os.path.join(BASE_DIR, 'gunicorn.pid')

worker_class = 'gevent'
logfile = os.path.join(BASE_DIR, 'logs', 'gunicorn.log')

proc_name = 'repdb PROD'