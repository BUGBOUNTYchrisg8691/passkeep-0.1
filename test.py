#!/usr/bin/env python3

from creds_handler import Credentials
import bcrypt

salt = bcrypt.gensalt()
creds = Credentials('google', 'chrisg', 'password1', salt)

print(creds)
creds.hash_entry('pass')
print(creds.__repr__())
