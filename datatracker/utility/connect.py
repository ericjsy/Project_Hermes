#!/usr/bin/python

from datatracker.utility.log import Log


def connect_to_api(self, response):
    try:
        response.raise_for_status()
    except Exception as e:
        log = Log(self.name, e, response.headers)
        log.add_entry()
        response.close()
        return 0

    return 1
