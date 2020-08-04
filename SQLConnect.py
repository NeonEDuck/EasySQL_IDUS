#!/usr/bin/env python3

from contextlib import contextmanager
import psycopg2
import sys


@contextmanager
def SQL_Manager(connInfo, commit=False):
    connection = psycopg2.connect(
        host= connInfo['host'],
        port= connInfo['port'],
        user= connInfo['user'],
        password= connInfo['password'],
        database= connInfo['database']
    )
    cursor = connection.cursor()
    try:
        yield connection, cursor
    except psycopg2.DatabaseError as err:
        error, = err.args
        sys.stderr.write(error)
        connection.rollback()
        raise err
    else:
        if commit:
            connection.commit()
        else:
            connection.rollback()
    finally:
        cursor.close()
        connection.close()

class SQLConnect():

    status_code = 'OK'

    def __init__(self, *args, **kwargs):
        
        if len(args) == 1:
            self.connInfo = args[0]
        elif len(args) > 1:
            self.connInfo = {
                'host':     args[0],
                'port':     args[1],
                'user':     args[2],
                'password': args[3],
                'database': args[4] 
            }
        else:
            self.connInfo = kwargs.get('connInfo', None)

            print(self.connInfo)
            if not self.connInfo:
                self.connInfo = {
                    'host':     kwargs.get('host', None),
                    'port':     kwargs.get('port', None),
                    'user':     kwargs.get('user', None),
                    'password': kwargs.get('password', None),
                    'database': kwargs.get('database', None) 
                }
            
        # print(self.connInfo)

        self.table_list = {}
        try:
            with SQL_Manager(self.connInfo) as (conn, cursor):
                #init table list
                query = "SELECT DISTINCT table_name FROM information_schema.columns WHERE table_schema='public'"
                cursor.execute(query)
                table_name = list(map(lambda x: x[0], cursor.fetchall()))

                for t in table_name:
                    cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name='{t}'")
                    self.table_list[t] = cursor.fetchall()

                
        except psycopg2.DatabaseError as err:
            self.status_code = err.args[0]

    def connect(self):
        return SQL_Manager(self.connInfo)