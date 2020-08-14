#!/usr/bin/env python3

import base64
import os
import sys
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class MasterCreds:
    def __init__(self, salt=None):
        if salt is None:
            self.__master_salt = bcrypt.gensalt(rounds=16)
        else:
            self.__master_salt = salt

        self.kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.__master_salt,
            backend=default_backend()
        )

    def get_master_salt(self):
        return self.__master_salt

    def hash(self, input_str, password):
        key = base64.urlsafe_b64encode(
            self.kdf.derive(password.encode('utf-8'))
        )
        f = Fernet(key)

        return f.encrypt(input_str.encode('utf-8')).decode('utf-8')

    def unhash(self, input_str, password):
        key = base64.urlsafe_b64encode(
            self.kdf.derive(password.encode('utf-8'))
        )
        f = Fernet(key)

        return f.decrypt(input_str.encode('utf-8')).decode('utf-8')
