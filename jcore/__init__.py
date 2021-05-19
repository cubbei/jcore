# -*- coding: utf-8 -*-

"""
Twitch IRC & API Wrapper
~~~~~~~~~~~~~~~~~~~
A basic wrapper for the Twitch IRC channels and 
partial coverage of the Twitch API.
:copyright: (c) 2016-2019 Cubbei
:license: Restricted, direct inquiries to Cubbei.
"""

__title__ = 'Jarvis Core [Async]'
__author__ = 'cubbei'
__license__ = 'Restricted'
__copyright__ = 'Copyright 2016-2021 Cubbei'
__version__ = '0.1.1a'

from collections import namedtuple

from .jsocket import Socket
from .client import Client
from .message import *

# from .client import Client
# from .module import Module
# from .errors import *
# from .helpers import Helpers
# from .httpclient import HTTPClient, WebResponse
# from .log import Log
# from .message import *
# from .model import Model
# from .settings import Settings
# from .socket import Socket
# from .telemetry import Telemetry
# from .user import User
# from .modules import *







VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')

version_info = VersionInfo(major=0, minor=1, micro=1, releaselevel='alpha', serial=0)