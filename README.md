## About
Appy: A simple framework that provides all the basic functionalities (logging, threads, cli etc.) needed for simple python applications.

## Usage
    import appy
    
    class Application(appy.App):
    
        @appy.cli.option('help', text='Print the help and exit')
        def help(self):
            self.print_usage()
            
        @appy.cli.option('run', text='Run the application')
        def run_app(self):
            self.run()
    
        @appy.async.thread()
        def do_background_op(self):
            for num in range(100):
                print num % 2
    
        def run(self):
            print 'app started'
            status = self.do_background_op()
            print 'thread running'
            if status.finished():
                print 'thread operation completed'
    
        def finish(self):
            print 'application stopped'
    
    if __name__ == '__main__':
        app = Application()
        app.start()

If you do,

    python my_app.py help

It'll show,

    Usage:

    my_app.py:
        Option          Operation
        ======          =========
        help            Print the help and exit
        run             Run the application

## Developer

Sreejith K <sreejithemk@gmail.com>

http://foobarnbaz.com