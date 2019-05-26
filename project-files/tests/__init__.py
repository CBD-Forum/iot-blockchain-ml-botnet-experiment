import os
import sys
import getpass

from unittest.mock import MagicMock

os.environ['VAGRANT_USER'] = getpass.getuser()
os.environ['PROJECT_DIR'] = os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))
)

sys.modules['docker'] = MagicMock()
