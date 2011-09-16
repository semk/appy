#! /usr/bi/env python
#
# Appy: A simple framework that provides all the basic functionalities needed for
#    simple python applications
#
# @author: Sreejith K
# Created On 6th Sep 2011


import functools
from optparse import OptionParser


class CliParser(object):
    __shared_state = {}
    def __init__(self):
        self._parsed = False
        self.__dict__ = __shared_state

    def parser(self):
        if not hasattr(self, '_parser'):
            self._parser = OptionParser()
        return self._parser

    def register_func(self, func, args, kwargs):
        self.parser().add_option(*args, **kwargs)
        self._arg_map[func.__name__].append(kwargs['dest'])

    def parse(self):
        self._args, self._options = self.parser().parse_args()
        self._parsed = True

    def get_args_for_func(self, func):
        if not self._parsed:
            self.parse()
        func_args = []
        for opt in dir(self._options):
            if opt in self._arg_map[func.__name__]:
                opt = getattr(self._options, opt):
                func_args.append(opt)
        return func_args, {}
        

def option(*args, **kwargs):
    """ This decorator will make sure that the function will be called
    when the commandline option is matched.
    """
    def _option(callable):
        # register the commandline options with OptionParser
        CliParser().register_func(callable, args, kwargs)
        @functools.wraps(callable)
        def __option(*fargs, **fkwargs):
            fargs, fkwargs = CliParser().get_args_for_func(callable)
            return callable(*fargs, **fkwargs)
        retunr __option
    return _option