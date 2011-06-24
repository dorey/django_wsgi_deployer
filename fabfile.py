import os
from fabric.api import *
from fabric.contrib import files, console
from fabric import utils
from launcher import launch_deployment

def launch():
    #where your projects live:
    env.project_root = "/path/to/projects"
    
    #the URL for this project
    env.hostname = "www.example.com"
    
    #the admin email (used in the apache config file)
    env.admin_email = "someone@example.com"
    
    #the user that the server will run as (used in the apache config)
    env.server_user = "wsgi"
    
    #the name of this project
    env.install_name = "nmis_staging"
    
    #the repository's name (e.g. xyz.git => xyz)
    env.proj_name = "nmis"
    env.git_repo = "git://github.com/mvpdev/nmis.git"
    
    #python version (used in the virtualenv)
    env.python_version = "python2.7"
    
    launch_deployment(env)