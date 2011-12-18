from fabric.api import *

import os

def prod():
    """Select the prod environment for future commands."""
    env.hosts = ['theelect.openparliament.ca', 'boundaries.opennorth.ca']
    env.user = 'deployer'
    env.python = '/home/deployer/.virtualenvs/repdb/bin/python'
    env.base_dir = '/home/deployer/repdb' # base_dir should contain canada-boundaryservice
    _env_init()
    
def _env_init():
    env.django_dir = os.path.join(env.base_dir, 'canada-boundaryservice')
    
def pull(ref='master'):
    """Update the git repository to the given branch or tag"""
    with cd(env.django_dir):
        run('git fetch')
        run('git fetch --tags')
        run('git checkout %s' % ref)
    
        is_tag = (ref == run('git describe --all %s' % ref).strip())
        if not is_tag:
            run('git pull origin %s' % ref)
            
        run('git submodule update')
        
def reload_code():
    """Send gunicorn a signal to restart its Python processes"""
    with cd(env.base_dir):
        run('kill -HUP `cat gunicorn.pid`')
        
def update_statics():
    """Tell Django staticfiles to update said files."""
    with cd(env.django_dir):
        run(env.python + ' manage.py collectstatic --noinput')
        
def deploy():
    """Perform all the steps in a standard deployment"""
    pull()
    update_statics()
    reload_code()