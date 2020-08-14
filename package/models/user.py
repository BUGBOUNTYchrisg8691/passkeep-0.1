#!/usr/bin/env python3

import os
import sys
import pymysql
from bcrypt import gensalt
from package.models.sql import DatabaseInteraction


class User:
    def __init__(self, first_name, last_name, email, master_password,
                 master_salt=None, user_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.__master_password = master_password
        
        if master_salt is None:
            self.__master_salt = gensalt(rounds=12)
        else:
            self.__master_salt = master_salt
        
        self.user_id = user_id

    def get_user_id(self):
        ''' Get an existing users user id.
        '''
        DB_CREDS = {
            'host': os.environ.get('SQL_DO_HOST'),
            'port': int(os.environ.get('SQL_DO_PORT')),
            'user': os.environ.get('SQL_DO_USER'),
            'password': os.environ.get('SQL_DO_PASS'),
            'db': os.environ.get('SQL_DO_DB')
        }
        
        sql_statement = '''SELECT id FROM users WHERE email=%s'''

        try:
            conn = pymysql.Connect(**DB_CREDS)
            cursor = conn.cursor()
            cursor.execute(sql_statement, (self.email))
            self.user_id = cursor.fetchone()[0]
        except Exception as e:
            sys.exit('An exception has occurred: ' + str(e))
