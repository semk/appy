## About
Appy: A simple framework that provides all the basic functionalities (logging, threads, cli etc.) needed for simple python applications.

## Usage
    import appy
	import appy.async
	import appy.cli
    from time import sleep
    
    class SampleApplication(appy.App):
    
        def do_task(self):
            res = 0
            for i in range(10):
                sleep(1)
                res += i
            return res
    
        @appy.cli.option('--test', help='This is a sample commandline option')
        def test(option, opt_str, value, parser): # NOTE: this is a staticmethod
            parser.print_help()

        @appy.async.thread
        def do_async_test_thread(self):
            self.do_task()
    
        @appy.async.process
        def do_async_test_process(self):
            self.do_task()
    
        def run(self):
            # directly run the method. blocks till completion
            self.do_task()
            # this will run asynchronously in a seperate thread
            thd = self.do_async_test_thread()
            # this will run asynchronously in a seperate process
            proc = self.do_async_test_process()
			# wait for the thread to complete its task
			thd.join()
			# wait for the process to complete its task
			proc.join()
    
    if __name__ == '__main__':
        app = Application()
        app.start()

If you do,

    python my_app.py test

It'll show,

    Options:
      -h, --help  show this help message and exit
      --test      This is a sample commandline option

## Developer

Sreejith K <sreejithemk@gmail.com>

http://foobarnbaz.com