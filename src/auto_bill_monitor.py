#!/usr/bin/env python

import os
import time
import subprocess
from ConfigParser import SafeConfigParser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class NewBillEventHandler(FileSystemEventHandler):

    def __init__(self, config, script_path='.'):
        super(NewBillEventHandler, self).__init__()
        self.__config = config
        self.__script = os.path.abspath(os.path.join(script_path, self.__config.get('options', 'file-script')))
        self.__ext = self.__config.get('options', 'file-extension')

    def on_created(self, event):
        evt = event.__dict__
        path_tail = evt['_src_path'][(0 - len(self.__ext)):]
        if evt['_is_directory'] == False and self.__ext == path_tail:
            subprocess.Popen([self.__script, evt['_src_path']])


if __name__ == '__main__':
    config = SafeConfigParser({'file-path': '.'})
    script_path = os.path.dirname(__file__)
    config.read(os.path.abspath(os.path.join(script_path, 'auto_bill.cfg')))
    path = config.get('options', 'file-path')
    handler = NewBillEventHandler(config, script_path)
    observer = Observer()
    observer.schedule(handler, path=path)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
