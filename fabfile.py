import os
from functools import wraps

from fabric.api import cd, env, run, task

@task
def alpheus():
    """Select the ohoh server for future commands."""
    env.hosts = ['represent-alpheus.opennorth.ca']
    env.user = 'represent'
    env.read_only_db = False
    _env_init()

@task
def tempeh():
    """Select the tofu server for future commands."""
    env.hosts = ['represent-tempeh.opennorth.ca']
    env.user = 'represent'
    env.read_only_db = True
    _env_init()


def _env_init():
    env.home_dir = '/home/' + env.user
    env.python = os.path.join(env.home_dir, 'represent-env', 'bin', 'python')
    env.base_dir = os.path.join(env.home_dir)
    env.django_dir = os.path.join(env.base_dir, 'app')
    env.pip = env.python.replace('bin/python', 'bin/pip')
    env.data_dir = os.path.join(env.django_dir, 'data')


@task
def deploy(ref='master'):
    """Perform all the steps in a standard deployment"""
    pull(ref)
    update_requirements()
    if not env.read_only_db:
        migrate()
    update_statics()
    restart()

def _require_db(target):
    """Decorator to enforce env.read_only_db"""
    @wraps(target)
    def inner(*args, **kwargs):
        if env.read_only_db:
            raise Exception("This task cannot be performed on an environment with a read-only database.")
        return target(*args, **kwargs)
    return inner

@task
def pull(ref='master'):
    """Update the git repository to the given branch or tag"""
    with cd(env.django_dir):
        run('git fetch')
        run('git fetch --tags')
        run('git checkout %s' % ref)

        is_tag = (ref == run('git describe --all %s' % ref).strip())
        if not is_tag:
            run('git pull origin %s' % ref)


@task
def update_requirements():
    """Update dependencies."""
    with cd(env.django_dir):
        run(env.pip + ' install -r requirements.txt')


@task
@_require_db
def migrate():
    """Update database schema."""
    with cd(env.django_dir):
        run(env.python + ' manage.py migrate')


@task
def update_statics():
    """Update static files."""
    with cd(env.django_dir):
        run(env.python + ' manage.py collectstatic --noinput')


@task
def restart():
    """Restart gunicorn."""
    with cd(env.base_dir):
        run('kill -HUP `cat gunicorn.pid`')


@task
@_require_db
def update_boundaries(args=''):
    """Pull data repositories and load shapefiles."""
    _recursive_pull(env.data_dir)
    with cd(env.django_dir):
        run(env.python + ' manage.py loadshapefiles ' + args)


@task
@_require_db
def update_representatives():
    """Update all representatives."""
    with cd(env.django_dir):
        run(env.python + ' manage.py updaterepresentatives')


@task
@_require_db
def update_concordances(args=''):
    """Pull data repositories and load postcode concordances."""
    _recursive_pull(env.data_dir)
    with cd(env.django_dir):
        run(env.python + ' manage.py loadpostcodeconcordance ' + args)


@task
@_require_db
def update_postcodes(args=''):
    """Pull data repositories and load postcodes."""
    _recursive_pull(env.data_dir)
    with cd(env.django_dir):
        run(env.python + ' manage.py loadpostcodes ' + args)


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
