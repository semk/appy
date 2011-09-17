#! /usr/bin/env python
#
# Unit-tests for all appy functionalities
#
# @author: Sreejith K
# Created On 6th Sep 2011


import sys
import os
import unittest
from time import sleep
import threading

sys.path.append('../')

import appy


class SampleApplication(appy.App):
    
    def __init__(self):
        self.test_called = False

    def set_commandline_option(self, opt):
        sys.argv.append(opt)

    def do_task(self):
        res = 0
        for i in range(10):
            sleep(1)
            res += i
        return res

    @appy.cli.option('--test')
    def test(self, option, opt_str, value, parser):
        self.test_called = True
        assert opt_str == '--test'

    @appy.async.thread
    def do_async_test_thread(self):
        self.do_task()

    @appy.async.process
    def do_async_test_process(self):
        self.do_task()

    def run(self):
        pass


class AppyApplicationTestCase(unittest.TestCase):

    def setUp(self):
        self.app = SampleApplication()

    def tearDown(self):
        self.app.stop()

    def testCommandLine(self):
        self.assertFalse(self.app.test_called)
        self.app.set_commandline_option('--test')
        self.app.start()
        self.assertTrue(self.app.test_called)
    
    def testAsyncThread(self):
        thd = self.app.do_async_test_thread()
        self.assertTrue(thd.is_alive())
        self.assertNotEqual(thd.ident, threading.current_thread.ident())
    
    def testAsyncProcess(self):
        proc = self.app.do_async_test_process()
        self.assertTrue(proc.is_alive())
        self.assertNotEqual(proc.id, os.getpid())