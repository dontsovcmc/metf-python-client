
from core import METFClient, LOW, HIGH, OUTPUT, INPUT, INPUT_PULLUP
from logger import log
from utils import str2hex, hex2str


VERSION_MAJOR = 0
VERSION_MINOR = 0
BUILD_NUMBER = 1

__version__ = '.'.join(map(str, (VERSION_MAJOR, VERSION_MINOR, BUILD_NUMBER)))
