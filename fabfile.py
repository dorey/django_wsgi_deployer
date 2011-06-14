import os
from fabric.api import *
from fabric.contrib import files, console
from fabric import utils

def launch():
    env.project_root = os.path.dirname(os.path.abspath(__file__))
    env.hostname = "www.example.com"
    env.admin_email = "someone@example.com"
    env.install_name = "nmis_staging"
    env.proj_name = "nmis"
    env.git_repo = "git://github.com/mvpdev/nmis.git"
    
    from launcher import launch_deployment
    launch_deployment(env)