# -*- coding: utf-8 -*-
# @Author   :qzhang
# @Date     :2020-04-07

import logging
from functools import partial

from .logger import __log,init_app_logger

__all__ = ['debug','info','warning','error','logger','critical','init_app_logger']

debug = partial(__log,logging.DEBUG)
info = partial(__log,logging.INFO)
error = partial(__log,logging.ERROR)
warning = partial(__log,logging.WARNING)
critical = partial(__log,logging.CRITICAL)