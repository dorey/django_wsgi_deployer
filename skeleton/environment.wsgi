import os
import sys
import glob
import re

PROJ_ROOT = "!ENV_PROJ_DIR!"
INSTALL_ROOT = "!ENV_INSTALL_ROOT!"
VENV_ROOT = "!ENV_VENV_ROOT!"

for pdir in glob.glob(os.path.join(VENV_ROOT, "src", "*")):
	if not re.search("\.txt$", pdir):
		sys.path.append(pdir)

sys.path.append(PROJ_ROOT)
sys.path.append(INSTALL_ROOT)
sys.path.append(os.path.join(VENV_ROOT, 'lib', '!ENV_PYTHON_VERSION!', 'site-packages'))

os.environ['DJANGO_SETTINGS_MODULE'] = '!ENV_GIT_REPO!.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()