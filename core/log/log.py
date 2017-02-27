# -*- coding: UTF-8 -*-


import logging
import os

import sys

__authors__ = "Shanming Liu"


class LoggerException(Exception):
    pass


class Logger(object):
    def __init__(self, name, level=logging.INFO, console=True, file_path=None):
        self.name = name
        self.level = level
        self.logger_formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)-5s] %(message)s')
        self.console = console

        self.logger = None
        self._init_logger()

        if console:
            self.enable_console_handle()

        if file_path:
            self.enable_log_file_handle(file_path)

    def _init_logger(self):
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.level)

    def enable_console_handle(self, formatter=None):
        console_handle = logging.StreamHandler(stream=sys.stdout)
        console_handle.setFormatter(self.get_log_formatter(formatter))
        self.logger.addHandler(console_handle)

    def enable_log_file_handle(self, filename, mode='w', formatter=None):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError:
            pass

        file_handle = logging.FileHandler(filename, mode=mode)
        file_handle.setFormatter(self.get_log_formatter(formatter))
        self.logger.addHandler(file_handle)

    def get_log_formatter(self, formatter):
        return self.logger_formatter if formatter is None else formatter

    def get_child(self, suffix, console=False, file_path=None):
        if self.logger.root is not self.logger:
            suffix = '.'.join((self.name, suffix))

            return self.__class__(suffix, level=self.level, console=console, file_path=file_path)

    def __getattr__(self, item):
        try:
            return getattr(self.logger, item)
        except AttributeError:
            raise LoggerException("No Attribute name of {}".format(str(item)))


if __name__ == '__main__':
    logger1 = Logger('aaaa', level='DEBUG', file_path='test1.log')
    logger2 = logger1.getChild('bbb', file_path='test2.log')
    # logger2.addHandler(console_handle)

    logger1.debug('aa')
    logger2.debug('bb')
