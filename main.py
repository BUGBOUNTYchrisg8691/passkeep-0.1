#!/usr/bin/env python3

from sql_funcs import *
from encryption import *
from creds_handler import Credentials
import bcrypt
import pymysql
from pymysql.err import OperationalError
import time

def main():
    print('----------Welcome to PassKeep.py----------')
    print('---------A Python Password Manager--------')
    print('------------------------------------------')
    print('If this is your first time using this program, you will need to thi'
          'nk of a secure master password. Your master password will not be st'
          'ored, so if you forget it, you will lose access to all of you crede'
          'ntials. Please write it down somewhere and keep it somewhere safe')
    print('------------------------------------------')

    action = str(input('Would you like to (a)dd an entry, (e)dit an entry, or '
                       '(d)isplay all entries?\n---> ' ))

    if (action.lower() == 'a'):
        creds = Credentials()
        creds.set_service()
        creds.set_username()
        creds.set_password()
        print('New entry: ' + creds.__str__())
        
        creds.hash_entry()
        conn = connect()

        service = creds.get_service()
        print(len(service))
        username = creds.get_username()
        print(len(username))
        passwd = creds.get_password()
        print(len(passwd))
        salt = creds.get_salt()
        print(len(salt))

        add_entry(conn=conn, service=service, username=username, passwd=passwd,
                  salt=salt)
        
    elif (action.lower() == 'e'):
        service = str(input('Enter service: '))

        conn = connect()
        entry = query_entries(conn, service)
        print(entry)

    elif (action.lower() == 'd'):
        try:
            conn = connect()
            print('Connected to database...')

            entries = query_all_entries(conn)
        
            print(entries)

        except Exception as e:
            print(e)

    else:
        print('An error occurred...')
        time.sleep(3)
        main()

if __name__ == '__main__':
    main()
