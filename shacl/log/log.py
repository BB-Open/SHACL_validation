# -*- coding: utf-8 -*-
import datetime
import os
from logging import ERROR, Formatter, StreamHandler, getLogger
from logging.handlers import RotatingFileHandler
from pathlib import Path
from sys import stdout

import zope
from pkan_config.config import get_config
from zope import component
from zope import interface


# Log level codes according to DB-Definition and syslog
import shacl
from shacl.ustils.errors import LogPathNotExists
from shacl.ustils.helper import dir_not_found_hint

SYSLOG_ERROR = 3
SYSLOG_WARN = 4
SYSLOG_INFO = 6
SYSLOG_DEBUG = 7

class ILogger(interface.Interface):
    """
    Marker Interface for logger utility
    """


@zope.interface.implementer(ILogger)
class Logger:
    """
    Logger class for logging to console, file and DB
    """
    logger = None
    db_log_func = None
    db_log_level = None

    def __init__(self, visitor=None):
        self.cfg = get_config()
        self.setup_logger()
        self.visitor = visitor

    def log_message(self, msg, file_id=None):
        out_msg = '{}{}'.format(file_id or '', msg)
        return out_msg

    def critical(self, msg, file_id=None):
        self.logger.critical(self.log_message(msg, file_id))
        self.plone_log('error', msg)

    def fatal(self, msg, file_id=None):
        self.logger.fatal(self.log_message(msg, file_id))
        self.plone_log('error', msg)

    def error(self, msg, file_id=None):
        self.logger.error(self.log_message(msg, file_id))
        self.plone_log('error', msg)

    def warning(self, msg, file_id=None):
        self.logger.warning(self.log_message(msg, file_id))
        self.plone_log('warn', msg)

    def info(self, msg, file_id=None):
        self.logger.info(self.log_message(msg, file_id))
        self.plone_log('info', msg)

    def debug(self, msg, file_id=None):
        self.logger.debug(self.log_message(msg, file_id))
        self.db_log(SYSLOG_DEBUG, msg, file_id)

    def setLevel(self, level):
        self.logger.setLevel(level)
        self.db_log_level = level

    def get_logger_formatter(self):
        """
        Check if a colored log is possible. Return get_logger and formatter instance.
        """
        try:
            import colorlog  # noqa: I001
            from colorlog import ColoredFormatter  # noqa: I001

            formatter = ColoredFormatter(
                '%(log_color)s%(asctime)s [%(process)d] '
                '%(levelname)-8s %(message)s',
                datefmt=None,
                reset=True,
                log_colors=self.cfg.log_colors,
                secondary_log_colors={},
                style='%',
            )
            get_logger = colorlog.getLogger

        except Exception as e:  # noqa E841
            #   print(e)
            get_logger = getLogger
            formatter = Formatter(
                '%(asctime)s [%(process)d] '
                '%(levelname)-8s %(message)s',
                '%Y-%m-%d %H:%M:%S',
            )
        return get_logger, formatter

    def setup_console_logger(self, formatter):
        """Console logger"""
        console_handler = StreamHandler(stdout)
        console_formatter = formatter
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(self.cfg.log_level)
        self.logger.addHandler(console_handler)

    def setup_file_logger(self, formatter):
        """
        File logger
        Has to be setup when the output filename is known
        """
        if not os.path.exists(self.cfg.PKAN_LOG_DIR):
            msg = """Log file directory "{path}" does not exists""".format(path=self.cfg.PKAN_LOG_DIR)

            dir_not_found_hint(self.cfg.PKAN_LOG_DIR )
            raise LogPathNotExists(msg)

        log_file_path = os.path.join(
            self.cfg.PKAN_LOG_DIR, self.cfg.SHACL_LOG_FILE,
        )
        print(f'Log file is {log_file_path}')
        file_handler = RotatingFileHandler(log_file_path, backupCount=5, maxBytes=1000000)
        file_handler_formatter = formatter
        file_handler.setFormatter(file_handler_formatter)
        file_handler.setLevel(self.cfg.log_level)
        self.logger.addHandler(file_handler)

    def setup_logger(self):
        """
        Staggered setup of loggers.
        First the console logger will come up, then the file logger.
        The db logger has to be brought up via an external call after the DB connection is ensured-
        """
        get_logger, formatter = self.get_logger_formatter()
        self.logger = get_logger('shacl')
        self.logger.setLevel(self.cfg.log_level)

        self.setup_console_logger(formatter)
        self.setup_file_logger(formatter)

    def delete_formatter(self):
        for h in self.logger.handlers:
            self.logger.removeHandler(h)

    def plone_log(self, level, msg):
        if self.visitor:
            self.visitor.scribe.write(
                level=level,
                msg=msg,
            )


def get_logger(visitor=None):
    # prohibit more than one logger instance
    logger = component.queryUtility(ILogger)
    if logger is not None:
        return logger

    logger = Logger(visitor=visitor)
    component.provideUtility(logger, ILogger)
    return logger


def unregister_logger():
    logger = component.queryUtility(ILogger)
    if logger:
        logger.delete_formatter()
    component.provideUtility(None, ILogger)
