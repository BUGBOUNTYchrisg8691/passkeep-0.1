#!/usr/bin/env python3

import os
import pymysql
import sys
import time
from encryption import *

#  FPATH = ''


def connect():

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

    conn = pymysql.Connect(host=host, user=user, password=password, port=port,
                           database=dbname)

    return conn


def add_user(conn, first_name, last_name, hsh_mast_pass, salt):
    try:
        cursor = conn.cursor()

        #  usr_stmnt = '''INSERT INTO users (first_name, last_name)
        #  VALUES ("%s", "%s") % (first_name, last_name);'''
#
        #  crd_stmnt = '''INSERT INTO creds (master_password, mast_pass_salt)
        #  VALUES ("%s", "%s") % (master_password, salt);'''

        #  cursor.execute(usr_stmnt)
        #  cursor.execute(crd_stmnt)
        cursor.execute('''INSERT INTO users (first_name, last_name)
                      VALUES (%s, %s);''', (first_name, last_name))
        cursor.execute('''INSERT INTO creds (master_password, mast_pass_salt)
                       VALUES (%s, %s);''', (hsh_mast_pass, salt))
        conn.commit()

    except ValueError as v_e:
        print(f'ValueError occured: {v_e}')

    except Exception as e:
        print(f'Exception occurred: {e}')

    else:
        print('Entry successfully added to DB. Returning to main menu.')

    finally:
        conn.close()


def login(conn, full_name, password):
    split_name = full_name.split()
    fname = split_name[0]
    lname = split_name[1]

    cursor = conn.cursor()
    id_query = '''SELECT id FROM users WHERE first_name=%s AND last_name=%s;'''
    cursor.execute(id_query, (fname, lname))
    uid = cursor.fetchone()[0]

    vrfy_query = '''SELECT master_password, mast_pass_salt FROM creds
    WHERE user_id=%s'''
    cursor.execute(vrfy_query, (uid))
    hsh_mast_pass, mast_pass_salt = cursor.fetchone()
    qrd_mast_pass = decrypt(input_str=hsh_mast_pass, mast_pass=password,
                            salt=mast_pass_salt.encode())
    if (password == qrd_mast_pass):
        pass

    else:
        print('Login failed... Exiting...')
        time.sleep(3)
        sys.exit()


def add_entry(conn, service, username, passwd, salt):
    try:
        cursor = conn.cursor()

        ent_stmnt = '''INSERT INTO entries (service, username, password, salt)
        VALUES (%s, %s, %s);'''

        slt_stmnt = '''INSERT INTO salts (salt) VALUES (%s);'''

        #  entry = tuple(service, username, passwd, salt)

        cursor.execute(ent_stmnt, (service, username, passwd))
        cursor.execute(slt_stmnt, [salt])
        conn.commit()

    except ValueError as v_e:
        print(f'ValueError occured: {v_e}')

    except Exception as e:
        print(f'Exception occurred: {e}')

    else:
        print('Entry successfully added to DB. Returning to main menu.')

    finally:
        conn.close()


def query_all_entries(conn):
    try:
        cursor = conn.cursor()

        sql_query = 'select * from entries;'

        cursor.execute(sql_query)
        entries = cursor.fetchall()

    except ValueError as v_e:
        print(f'ValueError occured: {v_e}')

    except Exception as e:
        print(f'Exception occurred: {e}')

    finally:
        conn.close()

    return entries


def query_entries(conn, query):
    try:
        cursor = conn.cursor()

        sql_query = 'select service, username, password, salt from entries w' \
            'here service=%s;'

        cursor.execute(sql_query, query)
        entry = cursor.fetchone()

    except ValueError as v_e:
        print(f'ValueError occured: {v_e}')

    except Exception as e:
        print(f'Exception occurred: {e}')

    finally:
        conn.close()

    return entry
