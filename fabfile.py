from fabric.api import *

import os


def ohoh():
    """Select the ohoh server for future commands."""
    env.hosts = ['represent-ohoh.opennorth.ca']
    env.user = 'represent'
    _env_init('app35')


def tofu():
    """Select the tofu server for future commands."""
    env.hosts = ['represent-tofu.opennorth.ca']
    env.user = 'represent'
    _env_init('app34')


def _env_init(virtualenv):
    env.home_dir = '/home/' + env.user
    env.python = os.path.join(env.home_dir, '.virtualenvs', virtualenv, 'bin', 'python')
    env.base_dir = os.path.join(env.home_dir)
    env.django_dir = os.path.join(env.base_dir, 'app')
    env.pip = env.python.replace('bin/python', 'bin/pip')
    env.data_dir = os.path.join(env.django_dir, 'data')


def deploy(ref='master'):
    """Perform all the steps in a standard deployment"""
    pull(ref)
    update_requirements()
    if env.host != 'represent-tofu.opennorth.ca':
        migrate()
    update_statics()
    restart()


def pull(ref='master'):
    """Update the git repository to the given branch or tag"""
    with cd(env.django_dir):
        run('git fetch')
        run('git fetch --tags')
        run('git checkout %s' % ref)

        is_tag = (ref == run('git describe --all %s' % ref).strip())
        if not is_tag:
            run('git pull origin %s' % ref)


def update_requirements():
    """Update dependencies."""
    with cd(env.django_dir):
        run(env.pip + ' install -r requirements.txt')


def migrate():
    """Update database schema."""
    with cd(env.django_dir):
        run(env.python + ' manage.py migrate')


def update_statics():
    """Update static files."""
    with cd(env.django_dir):
        run(env.python + ' manage.py collectstatic --noinput')


def restart():
    """Restart gunicorn."""
    with cd(env.base_dir):
        run('kill -HUP `cat gunicorn.pid`')


def update_boundaries(args=''):
    """Pull shapefiles repository and load shapefiles."""
    _recursive_pull(env.data_dir)
    with cd(env.django_dir):
        run(env.python + ' manage.py loadshapefiles ' + args)


def update_representatives():
    """Update all representatives."""
    with cd(env.django_dir):
        run(env.python + ' manage.py updaterepresentatives')


def _recursive_pull(base_dir):
    """Find and pull all git repositories in a directory tree."""
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
