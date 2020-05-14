# -*- coding: utf-8 -*-
# @Author  : qzhang
# @Date    : 2020-04-07

import sys
import logging

def __dict2str(target_dict):
    """
    按log格式将target_dict转换为字符串

    Args:
        target_dict: 要转换的dict

    Returns:
        target_dict转换出的字符串
    """
    acc = []
    for k, v in target_dict.iteritems():
        acc.append('%s=%s' % (k, v))
    return ', '.join(acc)

def __log(logging_level, msg, dt=None, is_monitor=False, caller_file=None, caller_fun=None):
    """
    输出log

    Args:
        logging_level: logging包相应的level值,如logging.DEBUG
        msg: 要打印的字符串信息
        dt: 要打印的dict
        is_monitor: 是否为监控log
        caller_file: 调用者所在的文件名, 为None则自动检测调用者文件名
        caller_fun: 调用者函数名, 为None则自动检测调用者函数名
    """
    if caller_file is None:
        caller_file = sys._getframe().f_back.f_code.co_filename
        caller_file = str(caller_file).split('/')[-1]

    if caller_fun is None:
        caller_fun = sys._getframe().f_back.f_code.co_name

    dt_str = None
    if isinstance(dt, dict):
        dt_str = __dict2str(dt)

    lineno = sys._getframe().f_back.f_lineno

    monitor_str = ''
    if is_monitor is True:
        monitor_str = ' [MONITOR-LOG]'

    if dt_str:
        out_log_str = '[%s:%s:%s] %s\t%s, %s' % (caller_file, lineno, caller_fun, monitor_str, msg, dt_str)
    else:
        out_log_str = '[%s:%s:%s] %s\t%s' % (caller_file, lineno, caller_fun, monitor_str, msg)

    logging.getLogger('rises').log(logging_level, out_log_str)

class IntoLogFormat(object):
    log_format = '[%(asctime)s] [%(process)d:%(thread)d] [%(name)s] [%(levelname)s] %(message)s '

def init_app_logger(app, conf):
    """
    按给定配置log_conf, 配置app的logger
    如果app为debug模式，则不配置,直接返回
    """
    from logging import FileHandler

    # 用到的配置
    log_path = conf.PATH
    log_level = conf.LEVEL
    log_format = IntoLogFormat.log_format

    # 配置log格式
    formatter = logging.Formatter(log_format)

    # 获取容器的logger
    werkzeug_logger = logging.getLogger('nlp.QA')
    werkzeug_logger.setLevel(log_level)

    logger = logging.getLogger('nlp.QA')
    logger.setLevel(log_level)
    log_handler = FileHandler(log_path, encoding='utf-8')
    log_handler.setFormatter(formatter)
    # 设置容器logger
    werkzeug_logger.addHandler(log_handler)
    # 设置自己使用的logger
    logger.addHandler(log_handler)
    # 设置flask的logger
    app.logger.addHandler(log_handler)
