import mysql.connector 
import pandas as pd
import openpyxl
import glob
import re
import os 

class HySQL:
    def __init__(self):
        self.columnName = []
        self.queryDict = {}
        self.cursor = ''
        self.adjust = 3
        self.result = []
        self.num = []
        self.connection = ''
    def drawLine(self):
        if len(self.num) != 0:
            for col in range(len(self.num)):
                if col == 0:
                    print('+',end='')
                    print('-'*self.num[col],end='')
                    if len(self.num) == 1:
                        print('+')
                    else :
                        print('+',end='')
                elif col == len(self.num)-1:
                    print('-'*self.num[col],end='')
                    print('+')
                else:
                    print('-'*self.num[col],end='')
                    print('+',end='')
    def dumpColumnData(self):
        if len(self.num) != 0:
            for col in range(len(self.columnName)):
                width = self.num[col]
                x = width - len(self.columnName[col])
                mid = int(x/2)
                right = x-mid
                left = mid
                if col == 0:
                    print('|',end='')
                    print(' '*left,end='')
                    print(self.columnName[col],end='')
                    print(' '*right,end='')
                    if len(self.columnName) == 1:
                        print('|')
                    else :
                        print('|',end='')
                elif col == len(self.columnName)-1:
                    print(' '*left,end='')
                    print(self.columnName[col],end='')
                    print(' '*right,end='')
                    print('|')
                else :
                    print(' '*left,end='')
                    print(self.columnName[col],end='')
                    print(' '*right,end='')
                    print('|',end='')
    def dumpData(self):
        if len(self.num) != 0:
            for loc in range(len(self.result)):
                info = self.result.iloc[loc]
                for col in range(len(info)):
                    width = self.num[col]
                    x = width - len(str(info[col]))
                    mid = int(x/2)
                    right = x-mid
                    left = mid
                    if col == 0:
                        print('|',end='')
                        print(' '*left,end='')
                        print(info[col],end='')
                        print(' '*right,end='')
                        if len(info) == 1:
                            print('|')
                    elif col == len(info)-1:
                        print('|',end='')
                        print(' '*left,end='')
                        print(info[col],end='')
                        print(' '*right,end='')
                        print('|')
                    else:
                        print('|',end='')
                        print(' '*left,end='')
                        print(info[col],end='')
                        print(' '*right,end='')
                        
    def display(self,x):
        self.result = x
        self.columnName = self.result.columns
        self.num = [max([len(str(x)) for x in [str(column)]+list(self.result[column])]) +self.adjust for column in self.columnName]
        if len(self.num) != 0:
            self.drawLine()
            self.dumpColumnData()
            self.drawLine()
            self.dumpData()
            self.drawLine()
        else :
            print([])
        
    def getQueryDict(self,query):
        query = query.strip()
        hysql = re.findall('~~.{1,500}~~',query)
        if len(hysql) != 0:
            hysql = hysql[0].strip()
        else:
            hysql = ''
        sql = query.replace(hysql,'').strip()
        return {'sql':sql, 'hysql':hysql}

    def rep(self,string):
        for s in ['[',']']:
            string = string.replace(s,'')
        return string
    
    def toWrite(self,file,tableData):
        supportedFile = ['csv','xlsx','json']
        for x in supportedFile:
            if file.endswith('.'+x):
                if x == 'csv':
                    tableData.to_csv(file)
                elif x == 'xlsx':
                    tableData.to_excel(file)
                elif x == 'json':
                    tableData.to_json(file)

    def toRead(self,file):
        supportedFile = ['csv','xlsx','json']
        if file in os.listdir():
            for x in supportedFile:
                if file.endswith('.'+x):
                    if x == 'csv':
                        df = pd.read_csv(file)
                        return df.head()
                    elif x == 'xlsx':
                        df = pd.read_excel(file)
                        return df.head()
                    elif x == 'json':
                        df = pd.read_json(file)
                        return df.head()
        else :
            return []
            
    def execHysql(self,hysql):
        hysql = hysql.replace('~~','').strip()
        if re.match('\s{0,4}(display|DISPLAY)\s{1,4}\[.{1,100}\]\s{0,4}',hysql):
            file = re.findall('\[[a-zA-Z_\.]{1,100}\]',hysql)
            if len(file) == 0:
                print('no file found')
                return None
            else :
                file = file[0]
                file = self.rep(file)
                df = self.toRead(file)
                if len(df) != 0:
                    self.display(df)
                else :
                    print('empty file/file does\'nt exists')
                    return None

        elif re.match('\s{0,4}(commit|COMMIT)\s{0,4}',hysql):
            self.connection.commit()
            print('commit successful')

        elif re.match('\s{0,4}(enable|ENABLE)\s{1,4}(autocommit|AUTOCOMMIT)\s{0,4}',hysql):
            self.connection.autocommit = True
            print('autocommit enabled')

        elif re.match('\s{0,4}(disable|DISABLE)\s{1,4}(autocommit|AUTOCOMMIT)\s{0,4}',hysql):
            self.connection.autocommit = False
            print('autocommit disabled')

        elif re.match('\s{0,4}(dump|DUMP)\s{1,4}(in|IN)\s{1,4}\[.{1,100}\]\s{0,4}',hysql):
            args = re.findall('\[[a-zA-Z_\.]{1,100}\]',hysql)
            if len(args) == 1:
                args = [self.rep(x) for x in args]
                file = args[-1]
                extension = re.findall('\.(csv|xlsx|json){1,100}',file)
                if len(extension) != 1:
                    print('cannot recognise file type')
                else :
                    if len(self.result) != 0:
                        if file in glob.glob('*'+extension[-1]):
                            print('file already exists')
                            perm = input('overwrite (y/n) : ').strip()
                            if perm == 'y':
                                self.toWrite(file,self.result)
                                print('data uploaded to file successfully')
                            else :
                                pass
                        else :
                            self.toWrite(file,self.result)
                            print('data uploaded to file successfully')
                    else :
                        print('empty table')
                
                
            else :
                print('file not specified')
                return None

        elif re.match('\s{0,4}(dump|DUMP)\s{1,4}\[.{1,100}\]\s{1,4}(in|IN)\s{1,4}\[.{1,100}\]\s{0,4}',hysql):
            args = re.findall('\[[a-zA-Z_\.]{1,100}\]',hysql)
            self.cursor.reset()
            if len(args) == 2:
                args = [self.rep(x) for x in args]
                file = args[-1]
                table = args[0]
                extension = re.findall('\.(json|csv|xlsx){1,100}',file)
                if extension :
                    extension = extension[-1]
                    self.cursor.execute(f'select * from {table};')
                    tableData = pd.DataFrame(self.cursor.fetchall(),
                                                 columns=self.cursor.column_names)
                    if file in glob.glob('*'+extension):
                        print('file already exists')
                        perm = input('overwrite (y/n) : ').strip()
                        if perm == 'y':
                            self.toWrite(file,tableData)
                        else:
                            pass
                    else :
                        self.toWrite(file,tableData)
                        print('data uploaded to file successfully')
                    
                else:
                    extension = re.findall('\.(json|csv|xlsx){1,100}',table)
                    if extension :
                        extension = extension[-1]
                        fileData = self.toRead(table)
                        self.cursor.execute(f'select * from {file};')
                        tc = list(self.cursor.column_names)
                        self.cursor.reset()
                        dc = list(fileData.columns)
                        tableColumn = []
                        dfColumn = []
                        for i in tc:
                            for j in dc:
                                if i.lower() == j.lower():
                                    tableColumn.append(i)
                                    dfColumn.append(j)
                        fileData = fileData[dfColumn]
                        # fillna with correspondin dtype
                        for col in fileData.columns:
                            dt = fileData[col].dtype
                            if dt == int or dt == float:
                                fileData[col].fillna(0,inplace=True)
                            else:
                                fileData[col].fillna('',inplace=True)
                        
                        tableColumn = f'{tuple(tableColumn)}'
                        tableColumn = tableColumn.replace('\'','')
                        for row in range(len(fileData)):
                            q = f'insert into {file} {tableColumn} values {tuple(fileData.iloc[row])};'
                            self.cursor.execute(q)
                        print('file uploaded to database')
                    else:
                        print('cannot recognise file type')
                        
            else:
                print('file/table not defined')
            
        elif hysql != '':
            print('HySQL syntax error')
        else :
            pass
        

    def execute(self,query,cursor,connection):
        self.cursor = cursor
        self.connection = connection
        self.queryDict = self.getQueryDict(query)
        self.cursor.execute(self.queryDict['sql'])
        if self.connection.result_set_available:
            self.columnName = self.cursor.column_names
            self.result = pd.DataFrame(self.cursor.fetchall(),
                                       columns=self.columnName)
            self.display(self.result)
        else :
            self.result = ''
        self.execHysql(self.queryDict['hysql'])
            




































    
                  
