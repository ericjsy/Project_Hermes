#!/usr/bin/python

"""API connection test.

Checks the HTTP response status code of a request.
"""

from datatracker.utility.log import Log


def connect_to_api(self, response):
    """Checks the API response status code.

    Determines if the request returns a 2XX status code.
    An invalid status code is recorded into a log for
    troubleshooting and closes the connection.

    :param self: object-binding reference
    :param response: server response from an API request
    :return: state of the request
    """

    try:
        response.raise_for_status()
    except Exception as e:
        log = Log(self.name, e, response.headers)
        log.add_entry()
        response.close()
        return 0

    return 1
