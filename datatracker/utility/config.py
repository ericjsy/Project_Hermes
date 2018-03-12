#!/usr/bin/python

"""Configures datahub connection settings.

Separates the database logic by passing on the credentials to establish a
successful connection from a separate file.
"""

from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
    """Database connection method.

    Passes on the connection string from a separate file.

    :param filename: file that contains the database information
    :param section: the database type
    :return: the connection string
    """

    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception("Section {0} not found in the {1} file".format(section, filename))

    return db
