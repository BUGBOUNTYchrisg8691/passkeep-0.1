#!/usr/bin/env python3

import json
import os
import pymysql

FPATH = '/home/chrisg/projects/passkeep/database.json'


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
    port = os.environ.get('SQL_DO_PORT')
    dbname = os.environ.get('SQL_DO_DB')

    try:
        conn = pymysql.Connect(host=host, port=port, user=user,
                               password=password, database=dbname)
        print('Connected to database.')

        cursor = conn.cursor()

        sql_query = 'create table if not exists entries( primary_key int(4) ' \
            'PRIMARY KEY, service varchar(64), username varchar(64), passwor' \
            'd varchar(64), salt varchar(64));'

        cursor.execute(sql_query)

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
