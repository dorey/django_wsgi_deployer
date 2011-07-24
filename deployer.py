import os
import re
import sys
from subprocess import call

try:
    import yaml
except ImportError:
    print "ERROR: Cannot read configuration file. Please install YAML"
    print "       try 'easy_install pyyaml'"
    sys.exit(0)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SKELETON_DIR = os.path.join(CURRENT_DIR, 'skeleton')

class BadConfigurationError(Exception):
    pass

def run():
    with open('configs.yaml') as f:
        configs = yaml.load(f.read())
    ensure_necessary_configs_are_set(configs)

    #setting some variables based on configs
    new_proj = os.path.join(configs['project_root'], configs['install_name'])
    code_src = os.path.join(new_proj, configs['git']['name'])
    virtualenv_path = os.path.join(new_proj, 'project_env')
    apache_dir = os.path.join(new_proj, 'apache')
    log_dir = os.path.join(new_proj, 'logs')
    wsgi_file_path = os.path.join(apache_dir, 'environment.wsgi')
    error_log = os.path.join(log_dir, 'error_log.log')
    access_log = os.path.join(log_dir, 'access_log.log')
    
    make_directory(new_proj)
    os.chdir(new_proj)
    call(["virtualenv", "--no-site-packages", "project_env"])
    make_subdirectories(new_proj, 
        ["apache", "backups", "logs"]
        )
    pull_code(new_proj, configs['git'])

    # a dict used to replace valuesin the skeleton files.
    file_var_replacements = {
        'PROJ_DIR': configs['project_root'],
        'STATIC_DIR': "env.static_root",
        'INSTALL_ROOT': code_src,
        'GIT_REPO': configs['git']['name'],
        'VROOT': virtualenv_path,
        'SERVER_NAME': configs['hostname'],
        'ADMIN_EMAIL': configs['admin_email'],
        'WSGI_FILE': wsgi_file_path,
        'ERROR_LOG': error_log,
        'ACCESS_LOG': access_log,
        'APACHE_DIR': apache_dir,
        'SERVER_USER': configs['server_user'],
        'PYTHON_VERSION': configs['python_version'],
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
    copy_skeleton_to_path(SKELETON_DIR, apache_dir, 'environment.wsgi', file_var_replacements)
    copy_skeleton_to_path(SKELETON_DIR, apache_dir, 'site.conf', file_var_replacements)

def ensure_necessary_configs_are_set(configs):
    if configs['hostname'] == "www.example.com":
        raise BadConfigurationError("hostname must be changed from www.example.com")
    if configs['admin_email'] == "someone@example.com":
        raise BadConfigurationError("email must be changed from someone@example.com")
    if configs['project_root'] == "/path/to/projects":
        raise BadConfigurationError("the path to the projects root must be specified")
    if configs['install_name'] == "install_name":
        raise BadConfigurationError("the install_name must be specified")

def make_directory(directory):
    if os.path.exists(directory):
        raise Exception("'project_root'/'install_name' already exists: %s" % directory)
    os.mkdir(directory)

def make_subdirectories(proj, sd_list):
    for dirname in sd_list:
        dir_path = os.path.join(proj, dirname)
        os.mkdir(dir_path)

def pull_code(directory, git):
    call(["git", "clone",
            git['repo'],
            "-b%s" % git['branch'],
            git['name']])

if __name__=="__main__":
    run()