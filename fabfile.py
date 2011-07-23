import os
from fabric.api import *
from fabric.contrib import files, console
from fabric import utils
from launcher import launch_deployment

def launch():
    #where your projects live:
    env.project_root = "/home/wsgi/srv"
    
    #the URL for this project
    env.hostname = "www.example.com"
    
    #the admin email (used in the apache config file)
    env.admin_email = "someone@example.com"
    
    #the user that the server will run as (used in the apache config)
    env.server_user = "wsgi"
    
    #the name of this project
    # everything will be installed in "/%{project_root}/${install_name}"
    env.install_name = "xls2xform_dev"
    
    #the repository's name (e.g. xyz.git => xyz)
    env.proj_name = "xls2xform"
    env.git_repo = "git://github.com/mvpdev/xls2xform.git"
    env.git_branch = "develop"
    
    #python version (used in the virtualenv)
    env.python_version = "python2.7"
    
    launch_deployment(env)