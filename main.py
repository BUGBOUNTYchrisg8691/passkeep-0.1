#!/usr/bin/env python3

from creds_handler import Credentials
from encryption import *
from getpass import getpass
from sql_funcs import *
import bcrypt
import pymysql
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

    print('------------------Login-------------------')
    name = str(input('Enter name: '))
    mast_pass = str(getpass('Enter master password: '))
    conn = connect()
    login(conn=conn, full_name=name, password=mast_pass)

    action = str(input('Would you like to (a)dd an entry, (e)dit an entry, or '
                       '(d)isplay all entries?\n---> '))

    if (action.lower() == 'a'):
        creds = Credentials()
        creds.set_service()
        creds.set_username()
        creds.set_password()
        print('New entry: ' + creds.__str__())

        creds.hash_entry()
        conn = connect()

        service = creds.get_service()
        username = creds.get_username()
        passwd = creds.get_password()
        salt = creds.get_salt().decode()

        add_entry(conn=conn, service=service, username=username, passwd=passwd,
                  salt=salt)

        time.sleep(5)
        main()

    elif (action.lower() == 'e'):
        service = str(input('Enter service: '))
        mast_pass = str(getpass('Enter master password: '))
        confirm = str(getpass('Confirm master password: '))

        if (mast_pass == confirm):
            pass
            #  query = encrypt()

        else:
            print('Passwords did not match... Returning to main menu...')
            time.sleep(3)
            main()

        try:
            conn = connect()
            entry = query_entries(conn, service)
            print(entry)

            creds = Credentials(service=entry[1], username=[2],
                                password=entry[3], salt=entry[4].encode())

            creds.unhash_entry(mast_pass=mast_pass)

            print(creds)

        except Exception as e:
            print(e)

    elif (action.lower() == 'd'):
        try:
            conn = connect()
            print('Connected to database...')

            entries = query_all_entries(conn)

            entry_list = []
            mast_pass = str(getpass('Enter master password: '))
            confirm = str(getpass('Confirm master password: '))
            if (mast_pass == confirm):
                pass

            else:
                print('Passwords did not match... Returning to main menu...')
                time.sleep(3)
                main()

            for entry in entries:
                creds = Credentials(service=entry[1], username=entry[2],
                                    password=entry[3], salt=entry[4].encode())

                creds.unhash_entry(mast_pass=mast_pass)

                entry_list.append(creds)

            for entry in entry_list:
                print(entry)

        except Exception as e:
            print(e)

    else:
        print('An error occurred...')
        time.sleep(5)
        main()


if (__name__ == '__main__'):
    main()
