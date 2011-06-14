import os
import re
from fabric.api import *
from fabric.contrib import files, console
from fabric import utils

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SKELETON_DIR = os.path.join(CURRENT_DIR, 'skeleton')

def launch_deployment(env):
    env.new_proj = os.path.join(env.project_root, env.install_name)
    env.apache_dir = os.path.join(env.new_proj, 'apache')
    env.code_src = os.path.join(env.new_proj, env.proj_name)
    env.static_root = os.path.join(env.code_src, 'static')
    env.virtualenv_path = os.path.join(env.new_proj, 'project_env')
    env.log_dir = os.path.join(env.new_proj, 'logs')
    env.error_log = os.path.join(env.log_dir, 'error_log.log')
    env.access_log = os.path.join(env.log_dir, 'access_log.log')
    env.wsgi_file_path = os.path.join(env.apache_dir, 'environment.wsgi')
    
    #create directories and virtual environment
    os.mkdir(env.new_proj)
    local("virtualenv %s --no-site-packages" % env.virtualenv_path)
    for dirname in ["apache", "backups", "logs"]:
        dir_path = os.path.join(env.new_proj, dirname)
        os.mkdir(dir_path)
    #pull code
    _pull_code(env)
    
    file_var_replacements = {
        'ENV_PROJ_ROOT': env.project_root,
        'ENV_STATIC_DIR': env.static_root,
        'ENV_INSTALL_ROOT': env.code_src,
        'ENV_GIT_REPO': env.proj_name,
        'ENV_VENV_ROOT': env.virtualenv_path,
        'ENV_SERVER_NAME': env.hostname,
        'ENV_ADMIN_EMAIL': env.admin_email,
        'ENV_WSGI_FILE': env.wsgi_file_path,
        'ENV_ERROR_LOG': env.error_log,
        'ENV_ACCESS_LOG': env.access_log,
        'ENV_APACHE_DIR': env.apache_dir,
    }
    
    def copy_skeleton_to_path(src_dir, dest_dir, file_name, substitutions):
        src = os.path.join(src_dir, file_name)
        dest = os.path.join(dest_dir, file_name)
        def substitute_text(key, val, text):
            return re.sub("!%s!" % key, val, text)
        with open(dest, 'w') as f:
            skel = open(src, 'r')
            skel_txt = skel.read()
            for key, val in substitutions.items():
                skel_txt = substitute_text(key, val, skel_txt)
            f.write(skel_txt)
            skel.close()
    copy_skeleton_to_path(SKELETON_DIR, env.apache_dir, 'environment.wsgi', file_var_replacements)
    copy_skeleton_to_path(SKELETON_DIR, env.apache_dir, 'site.conf', file_var_replacements)

def _pull_code(env):
    local("cd %s && git clone %s" % (env.new_proj, env.git_repo))
    local("ls %s" % env.new_proj)

