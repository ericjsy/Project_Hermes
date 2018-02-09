#!/usr/bin/python

import os
import errno
from datetime import datetime


class Log():
    def __init__(self, name, status_code, headers):
        self.name = name
        self.status_code = status_code
        self.headers = headers

    def add_entry(self):
        timestamp = datetime.now().replace(microsecond=0)

        try:
            os.makedirs("logs")
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        f = open("logs\\" + self.name + "_errors.txt", "a+")

        if self.headers is not None:
            f.write("[{0}] - {1} {2}\n".format(timestamp, self.status_code, self.headers))
        else:
            f.write("[{0}] - {1}".format(timestamp, self.status_code))
        f.close()
