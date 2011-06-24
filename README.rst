A WSGI Deployment Script (using fabric)
=======================================

This code probably shouldn't depend on fabric, but right now it does.

You might find it useful for deploying multiple django wsgi projects that have their own 'virtualenv's.

Edit the configurations in "fabfile.py" and run "fab launch". This script will create a directory with the following files:

 * apache/environment.wsgi: a wsgi config file with necessary extensions to sys.path to get your django app running off in a virtualenv
 * apache/site.conf: an apache config file with hard-coded links to the project's environment.wsgi file (and virtualenv)
 * logs: an empty directory for apache logs
 * backups: an empty directory for backups
 * project_env: your virtualenv
 * %(project): a 'git clone' of your project