from __future__ import absolute_import, unicode_literals

import logging

from exts.wechatpy.client import WeChatClient  # NOQA
from exts.wechatpy.component import ComponentOAuth, WeChatComponent  # NOQA
from exts.wechatpy.exceptions import WeChatClientException, WeChatException, WeChatOAuthException, WeChatPayException  # NOQA
from exts.wechatpy.oauth import WeChatOAuth  # NOQA
from exts.wechatpy.parser import parse_message  # NOQA
from exts.wechatpy.pay import WeChatPay  # NOQA
from exts.wechatpy.replies import create_reply  # NOQA

__version__ = '1.8.2'
__author__ = 'messense'

# Set default logging handler to avoid "No handler found" warnings.
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
