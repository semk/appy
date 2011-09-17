#! /usr/bin/env python
#
# Decorators for asynchronous methods
#
# @author: Sreejith K
# Created On 6th Sep 2011


import functools
import threading
import multiprocessing


def thread(func):
    """ All the methods decorated with this will be run asynchronously in
    a seperate thread when that method gets called.
    """
    @functools.wraps(func)
    def _thread(*args, **kwargs):
        thd = threading.Thread(target=func, args=args, kwargs=kwargs)
        thd.start()
        return thd
    return _thread


def process(func):
    """ All the methods decorated with this will be run asynchronously in
    a seperate process when that method gets called.
    """
    @functools.wraps(func)
    def _process(*args, **kwargs):
        proc = multiprocessing.Process(target=func, args=args, kwargs=kwargs)
        proc.start()
        return proc
    return _process