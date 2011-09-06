#! /usr/bi/env python
#
# Appy: A simple framework that provides all the basic functionalities needed for
#    simple python applications
#
# @author: Sreejith K
# Created On 6th Sep 2011


class App(object):
    """ The Application class. All application should inherit from this class
    """
    def __init__(self):
        self.daemon = False

    def set_daemon(self):
        self.daemon = True

    def start(self):
        """ Start the application. Do not override this method.
        """
        pass

    def run(self):
        """ This is where you should write the application code. Called automatically
        by start().
        """
        pass

# TODO: Need to implement the following decorators
#@appy.logger.log()
#@appy.async.thread()
#@appy.async.process()
#@appy.cli.option()
#@appy.cli.command()
#@appy.task()
#@appy.finish()