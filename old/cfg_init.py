#!/usr/bin/env python3

import json
import os
import pymysql
import time
from bcrypt import gensalt
from encryption import *
from getpass import getpass
from sql_funcs import add_user

#  FPATH = ''


def config():
    configuration = {'mysql': {
        'user': '',
        'pass': '',
        'host': '',
        'port': '',
        'database': ''
        }}

    with open(FPATH, 'w') as file:
        file.write(json.dumps(configuration, indent=4))


def main():
    #  if not os.path.exists(FPATH):
        #  config()
#
    #  with open(FPATH, 'r') as file:
        #  contents = json.load(file)

    #  args = contents['mysql']
    #  user = args['user']
    #  password = args['pass']
    #  host = args['host']
    #  port = int(args['port'])
    #  dbname = args['database']

    user = os.environ.get('SQL_DO_USER')
    password = os.environ.get('SQL_DO_PASS')
    host = os.environ.get('SQL_DO_HOST')
    port = int(os.environ.get('SQL_DO_PORT'))
    dbname = os.environ.get('SQL_DO_DB')

    try:
        conn = pymysql.Connect(host=host, port=port, user=user,
                               password=password, database=dbname)
        print('Connected to database.')

        cursor = conn.cursor()

        users_init = '''CREATE TABLE IF NOT EXISTS users(
        id INT NOT NULL AUTO_INCREMENT,
        first_name VARCHAR(256) NOT NULL,
        last_name VARCHAR(256) NOT NULL,
        email VARCHAR(64) NOT NULL,
        PRIMARY KEY (id));'''

        creds_init = '''CREATE TABLE IF NOT EXISTS creds(
        cred_id INT NOT NULL AUTO_INCREMENT,
        master_password varchar(256) NOT NULL,
        mast_pass_salt varchar(64) NOT NULL,
        user_id INT NOT NULL AUTO_INCREMENT,
        PRIMARY KEY (cred_id),
        FOREIGN KEY (user_id) REFERENCES users (id) ON UPDATE CASCADE);'''

        entries_init = '''CREATE TABLE IF NOT EXISTS entries(
        entry_id int(16) NOT NULL AUTO_INCREMENT,
        user_id int(16) NOT NULL,
        service varchar(256) NOT NULL,
        username varchar(256) NOT NULL,
        password varchar(256) NOT NULL,
        PRIMARY KEY (entry_id),
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE);
                       '''

        salts_init = '''CREATE TABLE IF NOT EXISTS salts(
        salt_id int(16) NOT NULL AUTO_INCREMENT,
        salt varchar(64) NOT NULL,
        PRIMARY KEY (salt_id),
        FOREIGN KEY (salt_id) REFERENCES entries (entry_id)
            ON DELETE CASCADE);'''

        cursor.execute(users_init)
        cursor.execute(creds_init)
        cursor.execute(entries_init)
        cursor.execute(salts_init)

    except ValueError as v_e:
        print(f'ValueError occurred: {v_e}')

    except Exception as e:
        print(f'Exception occured: {e}')

    else:
        print("Tables created.")

    finally:
        conn.close()

    fname = str(input('Enter your first name: '))
    lname = str(input('Enter your last name: '))
    mast_pass = str(getpass(
        'Please choose a master password: '
    ))
    confirm = str(getpass(
        'Please confirm master password: '
    ))

    if (mast_pass == confirm):
        salt = gensalt()

        try:
            conn = pymysql.Connect(host=host, port=port, user=user,
                                   password=password, database=dbname)
        
            enc_mast_pass = encrypt(input_str=mast_pass, mast_pass=mast_pass,
                                    salt=salt)
            add_user(conn=conn, first_name=fname, last_name=lname,
                     hsh_mast_pass=enc_mast_pass, salt=salt)

        except ValueError as v_e:
            print(f'Value Error occurred: {v_e}')

        except Exception as e:
            print(f'Exception occurred: {e}')

        else:
            print('User succesfully added.')

    else:
        print('An error occurred... Restarting...')
        time.sleep(3)
        main()


if __name__ == '__main__':
    main()
