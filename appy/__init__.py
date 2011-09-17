#! /usr/bin/env python
#
# Appy: A simple framework that provides all the basic functionalities needed for
#    simple python applications
#
# @author: Sreejith K
# Created On 6th Sep 2011


from __future__ import with_statement
import os
import sys
import logging
import signal

from cli import CliParser

# Default daemon parameters.
# File mode creation mask of the daemon.
UMASK = 0

# Default maximum for the number of available file descriptors.
MAXFD = 1024

# The standard I/O file descriptors are redirected to /dev/null by default.
if (hasattr(os, "devnull")):
    REDIRECT_TO = os.devnull
else:
    REDIRECT_TO = "/dev/null"


class App(object):
    """ The Application class. All applications should inherit from this class
    """
    def __init__(self, daemon=False, pidfile=None, logfile=None, loglevel=logging.INFO):
        self.daemon = daemon
        if not pidfile:
            self.pidfile = os.path.join(os.path.dirname(__file__), 
                                   '%s.pid' % self.__class__.__name__)
        if not logfile:
            self.logfile = os.path.join(os.path.dirname(__file__), 
                                   '%s.log' % self.__class__.__name__)

    def set_daemon(self):
        """ Sets whether the application should be a daemon process.
        """
        self.daemon = True

    def daemonize(self, workdir=os.path.dirname(__file__)):
        """ Detach a process from the controlling terminal and run it in the
        background as a daemon.
        """
        try:
            pid = os.fork()
        except OSError, e:
            raise Exception, "%s [%d]" % (e.strerror, e.errno)
    
        if (pid == 0):    # The first child.
            # become the leader of the session
            os.setsid()

            try:
                pid = os.fork()    # Fork a second child.
            except OSError, e:
                raise Exception, "%s [%d]" % (e.strerror, e.errno)
    
            if (pid == 0):    # The second child.
                # Since the current working directory may be a mounted filesystem, we
                # avoid the issue of not being able to unmount the filesystem at
                # shutdown time by changing it to the root directory.
                os.chdir(workdir)
                # We probably don't want the file mode creation mask inherited from
                # the parent, so we give the child complete control over permissions.
                os.umask(UMASK)
            else:
                os._exit(0)    # Exit parent (the first child) of the second child.
        else:
            os._exit(0)    # Exit parent of the first child.
    
        # Close all open file descriptors.  This prevents the child from keeping
        import resource        # Resource usage information.
        maxfd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
        if (maxfd == resource.RLIM_INFINITY):
            maxfd = MAXFD
      
        # Iterate through and close all file descriptors.
        for fd in range(0, maxfd):
            try:
                os.close(fd)
            except OSError:    # ERROR, fd wasn't open to begin with (ignored)
                pass
    
        # This call to open is guaranteed to return the lowest file descriptor,
        # which will be 0 (stdin), since it was closed above.
        os.open(REDIRECT_TO, os.O_RDWR)    # standard input (0)
    
        # Duplicate standard input to standard output and standard error.
        os.dup2(0, 1)            # standard output (1)
        os.dup2(0, 2)            # standard error (2)
    
        return(0)

    def start_command_prompt(self):
        """ Starts the command prompt.
        """

    def is_running(self, pid):
        """ Checks whether the pid is actually running.
        """
        return os.path.exists('/proc/%d' %pid)

    def get_pid(self):
        """ Return this process' id. 0 if not running.
        """
        try:
            with open(self.pidfile, 'r') as f:
                pid = int(f.read().strip())
        except:
            pid = 0
        return pid

    def remove_pid(self):
        """ Removes the pidfile.
        """
        try:
            os.remove(self.pidfile)
        except:
            pass

    def write_pid(self, pid):
        """ Writes the pid to file.
        """
        with open(self.pidfile, 'w') as f:
            f.write('%d' %pid)

    def stop(self):
        """ Stop the application by raising SIGTERM.
        """
        pid = self.get_pid()
        if self.is_running(pid):
            try:
                os.kill(pid, signal.SIGTERM)
            except:
                pass
        else:
            logging.warning('Process %d already stopped' %pid)
        self.remove_pid()

    def start(self):
        """ Start the application. Do not override this method.
        """
        # parse the commandline arguments. Does callbacks.
        CliParser().parse()
        # daemonize if needed
        if self.daemon:
            self.daemonize()
        # write to pidfile
        pid = os.getpid()
        self.write_pid(pid)
        # run the application code
        self.run()

    def run(self):
        """ This is where you should write the application code. Called automatically
        by start().
        """
        pass
