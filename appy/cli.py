#! /usr/bin/env python
#
# Decorator for easy commandline options
#
# @author: Sreejith K
# Created On 6th Sep 2011


import functools
from optparse import OptionParser


class CliParser(object):
    """ Commandline parser for the application. Returns a single
    parser throughout.
    """
    __shared_state = {}

    def __init__(self):
        """ This is a BORG pattern.
        """
        self.__dict__ = self.__shared_state

    def parser(self):
        """ Creates an OptionParser instance only once.
        """
        if not hasattr(self, '_parser'):
            self._parser = OptionParser()
        return self._parser

    def register_func(self, func, args, kwargs):
        """ Registers the option with the parser provided by the decorator.
        Sets the callback function.
        """
        # add callback
        kwargs['action'] = 'callback'
        kwargs['callback'] = func
        self.parser().add_option(*args, **kwargs)

    def parse(self):
        """ Parse all the commandline arguments.
        """
        if not hasattr(self, '_parsed'):
            self._args, self._options = self.parser().parse_args()
            self._parsed = True


def option(*args, **kwargs):
    """ This decorator will make sure that the function will be called
    when the commandline option is matched.
    """
    def _option(callable):
        # register the commandline options with OptionParser
        CliParser().register_func(callable, args, kwargs)
        # wrapped function
        @staticmethod
        @functools.wraps(callable)
        def __option(option, opt_str, value, parser):
            # call the callback with default arguments
            return callable(option, opt_str, value, parser)
        return __option
    return _option
