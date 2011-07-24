A WSGI Deployment Script
========================

You might find it useful for deploying multiple django wsgi projects that have their own 'virtualenv's.

This script will create a directory with the following files:

* apache/environment.wsgi: a wsgi config file with necessary extensions to sys.path to get your django app running off in a virtualenv
* apache/site.conf: an apache config file with hard-coded links to the project's environment.wsgi file (and virtualenv)
* logs: an empty directory for apache logs
* backups: an empty directory for backups
* project_env: your virtualenv
* %(project): a 'git clone' of your project


Edit the configurations in "configs.yaml" and run "python deployer.py". (note: deployer.py requires "pyyaml")

After running, you will need to configure the database and create a symlink from the apache configurations to the "site.conf" file. For this, I'd recommend something like this:

* ln -s /path/to/proj/my_cool_proj/apache/site.conf /etc/apache/sites-available/my_cool_proj.conf
* ln -s /etc/apache/sites-available/my_cool_proj.conf /etc/apache/sites-enabled/my_cool_proj.conf