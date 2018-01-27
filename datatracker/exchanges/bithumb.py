#!/usr/bin/python

import psycopg2
from datetime import datetime


class Bithumb():
    def __init__(self, response):
        self.response = response

    print("Bithumb")

    def pull_data(self):
        print("Pulling")

