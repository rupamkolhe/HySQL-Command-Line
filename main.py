
from hysql import HySQL
import mysql.connector
import pandas as pd
import openpyxl
import pwinput
import glob
import os
import re 

hysql = HySQL()

host = input('host : ').strip()
user = input('user : ').strip()
password = pwinput.pwinput('enter password : ', mask='*')

try:
    connection = mysql.connector.connect(host=host,
                                         user=user,
                                         password=password)
    if connection.is_connected():
        commit = input('enable autocommit(y/n) : ').casefold()
        print(f'''Welcome to HySQL monitor, by RSK .
hysql Commands are written 
after sql command between ~~.
connected to {connection.server_host} at {connection.server_port}
                 ''')
        if commit != 'n':
            connection.autocommit = True
        else:
            connection.autocommit = False
        cursor = connection.cursor()
        while True:
            query = input('Hysql> ').strip()
            if query == 'exit':
                break
            else :
                try:
                    hysql.execute(query,cursor,connection)
                except Exception as error:
                    print(error)
        cursor.close()
    connection.close()
except Exception as error:
    print(error)

