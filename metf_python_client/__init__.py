
from metf_python_client.core import METFClient
from metf_python_client.logger import log
from metf_python_client.utils import str2hex, hex2str


VERSION_MAJOR = 0
VERSION_MINOR = 2

__version__ = '.'.join(map(str, (VERSION_MAJOR, VERSION_MINOR)))
