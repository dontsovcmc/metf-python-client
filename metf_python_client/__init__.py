
from metf_python_client.core import METFClient, LOW, HIGH, OUTPUT, INPUT, INPUT_PULLUP
from metf_python_client.logger import log
from metf_python_client.utils import str2hex, hex2str


VERSION_MAJOR = 0
VERSION_MINOR = 0
BUILD_NUMBER = 2

__version__ = '.'.join(map(str, (VERSION_MAJOR, VERSION_MINOR, BUILD_NUMBER)))
