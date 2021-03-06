#!/usr/bin/env python3

import os
import pymysql
import sys
import time


class DatabaseInteraction:
    def __init__(self):
        self.DB_CREDS = {
            'host': os.environ.get('SQL_DO_HOST'),
            'port': int(os.environ.get('SQL_DO_PORT')),
            'user': os.environ.get('SQL_DO_USER'),
            'password': os.environ.get('SQL_DO_PASS'),
            'db': os.environ.get('SQL_DO_DB')
        }

        try: 
            self.conn = pymysql.Connect(**self.DB_CREDS)

        except Exception as e:
            sys.exit('An exception has occurred: ' + str(e))

    def add_user(self, first_name, last_name, email, master_password,
                 master_salt, **user_info):
        users_statement = '''INSERT INTO users(
        first_name, last_name, email)
        VALUES(%s, %s, %s)'''

        user_creds_statement = '''INSERT INTO user_creds(
        user_id, master_password, master_salt)
        VALUES(%s, %s, %s)'''

        if self.conn.open:
            try:
                self.cursor = self.conn.cursor()
            except Exception as e:
                sys.exit('An exception has occurred: ' + str(e))
        else:
            try:
                print('Reconnecting...')
                self.conn = pymysql.Connect(**self.DB_CREDS)
                self.cursor = self.conn.cursor()
            except Exception as e:
                sys.exit('An exception has occurred: ' + str(e))
            else:
                print('Connected.')
    
        try:
            print('Adding new user...')
            self.cursor.execute(users_statement,
                                (first_name, last_name, email))
            self.conn.commit()
            self.cursor.execute('''SELECT id FROM users WHERE email = %s''',
                                email)
            uid = self.cursor.fetchone()[0]
            self.cursor.execute(user_creds_statement,
                                (int(uid), master_password, master_salt))
            self.conn.commit()
        except Exception as e:
            sys.exit('An exception has occurred: ' + str(e))
        else:
            print('New user successfully added.')

    def add_entry(self, email, user_id, service, username, hashed_password,
                  salt, **entry_info):
        entries_statement = '''INSERT INTO entries(
        user_id, service, username, password)
        VALUES(%s, %s, %s, %s)'''

        salts_statement = '''INSERT INTO salts(entry_id, salt)
        VALUES(%s, %s)'''

        if self.conn.open:
            try:
                self.cursor = self.conn.cursor()
            except Exception as e:
                sys.exit('An exception occured: ' + str(e))
        else:
            try:
                print('Reconnecting...')
                self.conn = pymysql.Connect(**self.DB_CREDS)
                self.cursor = self.conn.cursor()
            except Exception as e:
                sys.exit('An exception has occurred: ' + str(e))
            else:
                print('Connected.')

        try:
            self.cursor.execute(entries_statement, (user_id, service, username,
                                                hashed_password))
            self.conn.commit()
            self.cursor.execute('''SELECT entry_id FROM entries
            WHERE user_id = %s AND service = %s''', (int(user_id), service))
            entry_id = self.cursor.fetchone()[0]
            self.cursor.execute(salts_statement, (int(entry_id), salt))
            self.conn.commit()
        except Exception as e:
            sys.exit('An exception has occurred: ' + str(e))
        else:
            print('Entry successfully added.')

    def delete_entry(self, entry_id):
        entry_statement = '''DELETE FROM entries WHERE entry_id = %s'''
        salt_statement = '''DELETE FROM salts WHERE entry_id = %s'''

        if self.conn.open:
            try:
                self.cursor = self.conn.cursor()
            except Exception as e:
                sys.exit(f'An Exception occurred: ' + str(e))
        else:
            try:
                print('Reconnecting...')
                self.conn = pymysql.Connect(**self.DB_CREDS)
            except Exception as e:
                sys.exit('An Exception occurred: ' + str(e))
            else:
                print('Connected.')
        try:
            print(f'Deleting entry...')
            self.cursor.execute(entry_statement, (int(entry_id)))
            self.conn.commit()
        except Exception as e:
            sys.exit('An exception occurred: ' + str(e))
        else:
            print('Entry successfully deleted.')

    def edit_entry(self, option, entry_id, new_item, **new_entry_info):
        if option.lower() == 'username':
            sql_statement = '''UPDATE entries SET username = %s
            WHERE entry_id = %s'''
        elif option.lower() == 'password':
            sql_statement = '''UPDATE entries SET password = %s
            WHERE entry_id = %s'''
        else:
            sys.exit('An error occurred.')

        if self.conn.open:
            try:
                self.cursor = self.conn.cursor()
            except Exception as e:
                sys.exit('An exception occurred: ' + str(e))
        else:
            try:
                print('Reconnecting...')
                self.conn = pymysql.Connect(**self.DB_CREDS)
                self.cursor = self.conn.cursor()
            except Exception as e:
                sys.exit('An exception ovvurred: ' + str(e))
            else:
                print('Connected.')

        try:
            self.cursor.execute(sql_statement, (new_item, int(entry_id)))
            self.conn.commit()
        except Exception as e:
            sys.exit('An exception occurred: ' + str(e))
        else:
            print('Entry successfully updated.')


    def delete_user(self, user_id):
        sql_statement = '''DELETE FROM users WHERE user_id = %s'''

        if self.conn.open:
            try:
                self.cursor = self.conn.cursor()
            except Exception as e:
                sys.exit('An exception occurred: ' + str(e))
        else:
            try:
                print('Reconnecting...')
                self.conn = pymysql.Connect(**self.DB_CREDS)
                self.cursor = self.conn.cursor()
            except Exception as e:
                sys.exit('An exception has occurred: ' + str(e))
            else:
                print('Connected.')

        try:
            print('Deleting account...')
            self.cursor.execute(sql_statement, (user_id))
            self.conn.commit()
        except Exception as e:
            sys.exit('An exception occurred: ' + str(e))
        else:
            print('Account successfuly deleted.')
