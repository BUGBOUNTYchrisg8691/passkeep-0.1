#!/usr/bin/env python3

import datetime
import os
import pymysql

FPATH = ''


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
    port = os.environ.get('SQL_DO_PORT')
    dbname = os.environ.get('SQL_DO_DB')

    conn = pymysql.connect(host=host, user=user, password=password, port=port,
        database=dbname)

    return conn


def add_entry(conn, service, username, passwd, salt):

    try:
        cursor = conn.cursor()

        sql_query = 'insert into entries( service, username, password, salt )' \
            ' values(?,?,?,?);'

        entry = tuple(service, username, passwd, salt)

        cursor.execute(sql_query, entry)

    except ValueError as ve:
        print(f'ValueError occured: {ve}')

    except Exception as e:
        print(f'Exception occurred: {e}')

    else:
        print(f'Entry successfully added: {service} | {username} | {passwd}')

    finally:
        conn.close()

def get_all_entries(conn):

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

def query_entries(conn, service):

    try:
        cursor = conn.cursor()

        sql_query = 'select username, password from entries where service = ?;'
    
        entry = [service]
        entry.append(cursor.execute(sql_query, service))

        return entry

    except ValueError as v_e:
        print(f'ValueError occured: {v_e}')

    except Exception as e:
        print(f'Exception occurred: {e}')

    finally:
        conn.close()

