from fabric.api import *

import os

def prod():
    """Select the prod environment for future commands."""
    env.hosts = ['represent.opennorth.ca']
    env.user = 'represent'
    _env_init()

def dev():
    """Select the dev environment for future commands."""
    env.hosts = ['represent-dev.opennorth.ca']
    env.user = 'represent-dev'
    _env_init()
    
def _env_init():
    env.home_dir = '/home/' + env.user
    env.python = os.path.join(env.home_dir, '.virtualenvs', 'repdb', 'bin', 'python')
    env.base_dir = os.path.join(env.home_dir, 'repdb')
    env.django_dir = os.path.join(env.base_dir, 'represent-canada')
    env.pip = env.python.replace('bin/python', 'bin/pip')
    env.data_dir = os.path.join(env.django_dir, 'data')
    
def deploy(ref='master'):
    """Perform all the steps in a standard deployment"""
    pull(ref)
    update_requirements()
    syncdb()
    update_statics()
    reload_code()
    
def pull(ref='master'):
    """Update the git repository to the given branch or tag"""
    with cd(env.django_dir):
        run('git fetch')
        run('git fetch --tags')
        run('git checkout %s' % ref)
    
        is_tag = (ref == run('git describe --all %s' % ref).strip())
        if not is_tag:
            run('git pull origin %s' % ref)
            
        #run('git submodule update')
        
def reload_code():
    """Send gunicorn a signal to restart its Python processes"""
    with cd(env.base_dir):
        run('kill -HUP `cat gunicorn.pid`')

def update_requirements():
    """Update Python dependencies"""
    with cd(env.django_dir):
        run(env.pip + ' install -r requirements.txt')

def syncdb():
    """Update database tables"""
    with cd(env.django_dir):
        run(env.python + ' manage.py syncdb --noinput')
        run(env.python + ' manage.py migrate')
        
def update_statics():
    """Tell Django staticfiles to update said files."""
    with cd(env.django_dir):
        run(env.python + ' manage.py collectstatic --noinput')

def _recursive_pull(base_dir):
    """Traverse a directory tree to find and pull all git repos."""
    with cd(base_dir):
        dirs = [
            d.strip()[:-1] for d in
            run('ls -aFL1').split('\n')
            if d.strip().endswith('/') and d.strip() not in ('./', '../')
        ]
        if '.git' in dirs:
            # This is a git repo, update it
            run('git pull')
        else:
            # Continue exploring
            for dir in dirs:
                _recursive_pull(os.path.join(base_dir, dir))

def update_shapes(args=''):
    """Pull our shapes repository and load the shapefiles."""
    _recursive_pull(env.data_dir)
    with cd(env.django_dir):
        run(env.python + ' manage.py loadshapefiles ' + args)

def update_reps():
    """Update all Representative data from ScraperWiki."""
    with cd(env.django_dir):
        run(env.python + ' manage.py updaterepresentatives')
