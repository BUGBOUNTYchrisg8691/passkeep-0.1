#!/usr/bin/env python3

import json
import os
import pymysql

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
        id int NOT NULL AUTO_INCREMENT,
        first_name varchar(256) NOT NULL,
        last_name varchar(256) NOT NULL,
        PRIMARY KEY (id));'''

        creds_init = '''CREATE TABLE IF NOT EXISTS creds(
        user_id int,
        master_password varchar(256) NOT NULL,
        mast_pass_salt varchar(64) NOT NULL,
        PRIMARY KEY (user_id),
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE);'''

        entries_init = '''CREATE TABLE IF NOT EXISTS entries(
        entry_id int NOT NULL AUTO_INCREMENT,
        user_id int,
        service varchar(256) NOT NULL,
        username varchar(256) NOT NULL,
        password varchar(256) NOT NULL,
        PRIMARY KEY (entry_id),
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE);
                       '''

        salts_init = '''CREATE TABLE IF NOT EXISTS salts(
        salt_id int,
        salt varchar(64) NOT NULL,
        PRIMARY KEY (salt_id),
        FOREIGN KEY (salt_id) REFERENCES entries (entry_id)
            ON DELETE CASCADE);'''
        
        
        cursor.execute(users_init)
        cursor.execute(creds_init)
        cursor.execute(entries_init)
        cursor.execute(salts_init)

        #  cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                            #  id int NOT NULL AUTO_INCREMENT,
                            #  first_name varchar(256) NOT NULL,
                            #  last_name varchar(256) NOT NULL,
                            #  PRIMARY KEY (id));
                       #  ''')
#
        #  cursor.execute('''CREATE TABLE IF NOT EXISTS creds(
                            #  user_id int,
                            #  master_password varchar(256) NOT NULL,
                            #  mast_pass_salt varchar(64) NOT NULL,
                            #  PRIMARY KEY (user_id),
                            #  FOREIGN KEY (user_id) REFERENCES users (id)
                                #  ON DELETE CASCADE);
                       #  ''')
#
        #  cursor.execute('''CREATE TABLE IF NOT EXISTS entries(
                            #  entry_id int NOT NULL AUTO_INCREMENT,
                            #  user_id int,
                            #  service varchar(256) NOT NULL,
                            #  username varchar(256) NOT NULL,
                            #  password varchar(256) NOT NULL,
                            #  PRIMARY KEY (entry_id),
                            #  FOREIGN KEY (user_id),
                            #  FOREIGN KEY (user_id) REFERENCES users (id)
                                #  ON DELETE CASCADE);
                       #  ''')
#
        #  cursor.execute('''CREATE TABLE IF NOT EXISTS salts(
                            #  salt_id int,
                            #  salt varchar(64) NOT NULL,
                            #  PRIMARY KEY (salt_id),
                            #  FOREIGN KEY (salt_id) REFERENCES entries (entry_id)
                                #  ON DELETE CASCADE);
                       #  ''')

    except ValueError as v_e:
        print(f'ValueError occurred: {v_e}')

    except Exception as e:
        print(f'Exception occured: {e}')

    else:
        print("Table 'entries' created.")

    finally:
        conn.close()


if __name__ == '__main__':
    main()
