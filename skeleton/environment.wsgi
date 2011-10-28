import os
import sys
import glob
import re

PROJ_DIR = "!PROJ_DIR!"
INSTALL_ROOT = "!INSTALL_ROOT!"
VENV_ROOT = "!VROOT!"

for pdir in glob.glob(os.path.join(VENV_ROOT, "src", "*")):
	if not re.search("\.txt$", pdir):
		sys.path.append(pdir)

sys.path.append(PROJ_DIR)
sys.path.append(INSTALL_ROOT)
sys.path.append(os.path.join(VENV_ROOT, 'lib', '!PYTHON_VERSION!', 'site-packages'))

os.environ['DJANGO_SETTINGS_MODULE'] = '!GIT_REPO!.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()