#!/usr/bin/env python

from fabric.api import *

"""
Base configuration
"""
env.project_name = 'hacktyler_boundaryservice'
env.user = 'ubuntu'
env.database_password = 'oZGWDn7y0L'
env.path = '/home/ubuntu/src/%(project_name)s' % env
env.log_path = '/var/log/src/%(project_name)s' % env
env.env_path = '/home/ubuntu/.virtualenvs/%(project_name)s' % env
env.repo_path = '%(path)s' % env
env.server_config_path = '/etc/nginx/sites-enabled/%(project_name)s' % env
env.python = 'python2.7'
env.repository_url = "git@github.com:hacktyler/hacktyler-boundaryservice.git"
env.hosts = ["ec2-75-101-203-238.compute-1.amazonaws.com"]
    
"""
Branches
"""
def stable():
    """
    Work on stable branch.
    """
    env.branch = 'stable'

def master():
    """
    Work on development branch.
    """
    env.branch = 'master'

def branch(branch_name):
    """
    Work on any specified branch.
    """
    env.branch = branch_name
    
"""
Commands - setup
"""
def setup():
    """
    Setup a fresh virtualenv, install everything we need, and fire up the database.
    """
    require('branch', provided_by=[stable, master, branch])

    setup_directories()
    setup_virtualenv()
    clone_repo()
    checkout_latest()
    install_requirements()
    destroy_database()
    create_database()
    syncdb()
    install_server_conf()
    collect_static_files()
    reload_app();

def setup_directories():
    """
    Create directories necessary for deployment.
    """
    run('mkdir -p %(path)s' % env)
    sudo('mkdir -p /var/log/sites/%(project_name)s' % env, user='uwsgi')
    
def setup_virtualenv():
    """
    Setup a fresh virtualenv.
    """
    run('virtualenv -p %(python)s --no-site-packages %(env_path)s;' % env)
    run('source %(env_path)s/bin/activate;' % env)

def clone_repo():
    """
    Do initial clone of the git repository.
    """
    run('git clone %(repository_url)s %(repo_path)s' % env)

def checkout_latest():
    """
    Pull the latest code on the specified branch.
    """
    require('branch', provided_by=[stable, master, branch])
    
    run('cd %(repo_path)s; git checkout %(branch)s; git pull origin %(branch)s' % env)

def install_requirements():
    """
    Install the required packages using pip.
    """
    run('%(env_path)s/bin/pip install -r %(repo_path)s/requirements.txt' % env)

def install_server_conf():
    """
    Install the server config file.
    """
    with settings(warn_only=True):
        sudo('ln -s %(repo_path)s/config/deployed/nginx %(server_config_path)s' % env)
        sudo('ln -s %(repo_path)s/config/deployed/uwsgi.conf /etc/init/%(project_name)s.conf' % env)

    sudo('initctl reload-configuration' % env)
    sudo('service %(project_name)s start' % env)
    sudo('service nginx restart' % env)

"""
Commands - deployment
"""
def deploy():
    """
    Deploy the latest version of the site to the server and restart the web server.
    
    Does not perform the functions of load_new_data().
    """
    require('branch', provided_by=[stable, master, branch])
    
    checkout_latest()
    collect_static_files()
    reload_app()

def collect_static_files():
    """
    Collect static files on the server.
    """
    sudo('cd %(repo_path)s; %(env_path)s/bin/python manage.py collectstatic --noinput' % env, user="uwsgi")

def reload_app(): 
    """
    Restart the uwsgi server.
    """
    sudo('service %(project_name)s restart' % env)
    
def update_requirements():
    """
    Update the installed dependencies the server.
    """
    run('%(env_path)s/bin/pip install -U -r %(repo_path)s/requirements.txt' % env)

"""
Commands - data
"""
def reset_database():
    """
    Drop and recreate the project database.
    """
    pgpool_down()
    destroy_database()
    create_database()
    syncdb()
    pgpool_up()

def create_database():
    """
    Creates the user and database for this project.
    """
    sudo('echo "CREATE USER %(project_name)s WITH PASSWORD \'%(database_password)s\';" | psql postgres' % env, user='postgres')
    sudo('createdb -T template_postgis -O %(project_name)s %(project_name)s' % env, user='postgres')
    
def destroy_database():
    """
    Destroys the user and database for this project.
    
    Will not cause the fab to fail if they do not exist.
    """
    pgpool_down()

    with settings(warn_only=True):
        sudo('dropdb %(project_name)s' % env, user='postgres')
        sudo('dropuser %(project_name)s' % env, user='postgres')
    
    pgpool_up()
        
def syncdb():
    """
    Sync the Django models to the database.
    """
    sudo('cd %(repo_path)s; %(env_path)s/bin/python manage.py syncdb --noinput' % env, user="uwsgi")

def pgpool_down():
    """
    Stop pgpool so that it won't prevent the database from being rebuilt.
    """
    sudo('service pgpool2 stop')
    
def pgpool_up():
    """
    Start pgpool.
    """
    sudo('service pgpool2 start')

"""
Commands - local
"""
def local_reset():
    """
    Reset the local database instance.
    """
    local_reset_database()

def local_reset_database():
    """
    Reset the local database.
    """
    with settings(warn_only=True):
        local('dropdb %(project_name)s' % env)
        local('dropuser %(project_name)s' % env)

    local('echo "CREATE USER %(project_name)s WITH PASSWORD \'%(database_password)s\';" | psql postgres' % env)
    local('createdb -O %(project_name)s %(project_name)s -T template_postgis' % env)
    local('python manage.py syncdb --noinput' % env) 

"""
Deaths, destroyers of worlds
"""
def shiva_the_destroyer():
    """
    Remove all directories, databases, etc. associated with the application.
    """
    with settings(warn_only=True):
        run('rm -Rf %(path)s' % env)
        run('rm -Rf %(log_path)s' % env)
        run('rm -Rf %(env_path)s' % env)
        pgpool_down()
        run('dropdb %(project_name)s' % env)
        run('dropuser %(project_name)s' % env)
        pgpool_up()
        sudo('rm %(server_config_path)s' % env)
        reload_app()

