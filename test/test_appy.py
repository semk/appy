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
import appy.cli
import appy.async


class SampleApplication(appy.App):

    def __init__(self):
        super(SampleApplication, self).__init__()
        self.thd = None
        self.proc = None

    def do_task(self):
        res = 0
        for i in range(3):
            sleep(1)
            res += i
        return res

    @appy.cli.option('--test')
    def test(option, opt_str, value, parser):
        self.test_called = True
        assert opt_str == '--test'

    @appy.async.thread
    def do_async_test_thread(self):
        self.do_task()

    @appy.async.process
    def do_async_test_process(self):
        self.do_task()

    def run(self):
        self.thd = self.do_async_test_thread()
        self.proc = self.do_async_test_process()


class AppyApplicationTestCase(unittest.TestCase):

    def setUp(self):
        self.app = SampleApplication()
        self.app.start()

    def tearDown(self):
        self.app.thd.join()
        self.app.proc.join()
        self.app.stop()
    
    def testAsyncThread(self):
        #self.assertTrue(self.app.thd.is_alive())
        self.assertNotEqual(self.app.thd.ident, threading.current_thread().ident)
    
    def testAsyncProcess(self):
        #self.assertTrue(self.app.proc.is_alive())
        self.assertNotEqual(self.app.proc.pid, os.getpid())

if __name__ == '__main__':
    unittest.main()