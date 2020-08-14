#!/usr/bin/env python3

import os
import sys
from bcrypt import gensalt


class Entries:
    def __init__(self, service, username, password, salt=None):
        self.service = service
        self.username = username
        self.password = password

        if salt is None:
            self.__salt = gensalt(round=8)
        else:
            self.__salt = salt

    def __str__(self):
        return 'Credentials({0}, {1}, {2})'.format(
            self.service, self.username, self.password
        )

    def __repr__(self):
        return 'Credentials(servcice: {0}, username: {1},' \
            ' password: {2}, salt: {3})'.format(
                self.service, self.username, self.password, self.__salt
        )
