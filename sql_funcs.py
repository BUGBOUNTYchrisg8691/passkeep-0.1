#!/usr/bin/env python3

import datetime
import os
import pymysql

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


def add_entry(conn, service, username, passwd, salt):

    try:
        cursor = conn.cursor()

        sql_query = "insert into entries(service, username, password, salt) " \
            "values('%s', '%s', '%s', '%s')" % (service, username, passwd,
                                              salt)

        #  entry = tuple(service, username, passwd, salt)

        cursor.execute(sql_query)
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

        sql_query = 'select (*) from entries;'
    
        cursor.execute(sql_query)

    except ValueError as v_e:
        print(f'ValueError occured: {v_e}')

    except Exception as e:
        print(f'Exception occurred: {e}')

    finally:
        conn.close()

    return cursor

def query_entries(conn, query):

    try:
        cursor = conn.cursor()

        sql_query = 'select service, username, password, salt from entries where service = ?;'
    
        cursor.execute(sql_query, query)

    except ValueError as v_e:
        print(f'ValueError occured: {v_e}')

    except Exception as e:
        print(f'Exception occurred: {e}')

    finally:
        conn.close()

    return cursor
