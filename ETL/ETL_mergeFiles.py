import glob
import csv
import sys
import psycopg2
import pandas as pd
from os import listdir
import os 
from os.path import isfile, join
from config import config
import time

class soramameSensorData:
    def __init__(self):
        self.timeStamps = None
        self.stationIDs = None
        self.pm25Data = None
        self.param = 'pm25'
        self.time = []
        
    def getSensorData(self, tempPath,tableName = 'data', outputParam=13):
        """
        
        Connects to database to get distinct timestamps and stationIDs. 
        For each stationID execute sql query to get timeStamp and pm2.5 values and store it in a CSV file
        
        """
        self.time.append(time.time())
        #setting attribute 
        
        if outputParam != 13:
            if outputParam == 1:
                self.param = 'sname'
            elif outputParam == 2 :
                self.param = 'time'
            elif outputParam == 3 :
                self.param = 'so2'
            elif outputParam == 4 :
                self.param = 'no'
            elif outputParam == 5 :
                self.param = 'no2'
            elif outputParam == 6 :
                self.param = 'nox'
            elif outputParam == 7 :
                self.param = 'co'
            elif outputParam == 8 :
                self.param = 'ox'
            elif outputParam == 9 :
                self.param = 'nmhc'
            elif outputParam == 10 :
                self.param = 'ch4'
            elif outputParam == 11:
                self.param = 'thc'
            elif outputParam == 12:
                self.param = 'spm'
            elif outputParam == 14:
                self.param = 'sp'
            elif outputParam == 15:
                self.param = 'wd'
            elif outputParam == 16:
                self.param = 'ws'
            elif outputParam == 17:
                self.param = 'temp'
            elif outputParam == 18:
                self.param = 'hum'
            else:
                print('Error : parameter index'+str(outputParam)+' out of range')
        
        # Connecting to PostgreSQL server
        conn = None
        try:
            # read connection parameters
            params = config()
            
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)

            # create a cursor
            cur = conn.cursor()

            #Execute sql query to find distinct timestamps in database
            query = 'SELECT DISTINCT time FROM ' + tableName+ ' order by time asc'
            cur.execute(query)
            self.timeStamps = cur.fetchall()

            #Execute sql query to find  distinct sensors in database
            query = 'SELECT DISTINCT(sname) FROM ' + tableName + ' order by sname asc'
            cur.execute(query)
            self.stationIDs = cur.fetchall();
            self.time.append(time.time())
            print("stationIDs Length: ",len(self.stationIDs), 'TimeStamps Length: ',len(self.timeStamps))
            
            # query to get pm2.5 values for each unique station ID
            # NOTE : Change attribute names(time,pm25) according to your table attributes
            for station in self.stationIDs:
                query = 'select time,' +self.param+' from '+tableName +' where sname=\''+str(station[0]) + '\' ORDER BY time asc'
                # print(query)
                cur.execute(query)
                self.pm25Data = cur.fetchall()  
                
                self.temp = {}
                for sensorValue in self.pm25Data:
                    if sensorValue[1] in [-1000,9999]:
                        self.temp[str(sensorValue[0])] = 'NaN'
                    else : 
                        self.temp[str(sensorValue[0])] = str(sensorValue[1])
                self.sensorDf = pd.DataFrame({'TimeStamp': self.temp.keys(), station[0] : self.temp.values()})
                
                self.sensorDf.to_csv(tempPath+str(station[0])+'.csv',index=None)
            print("Created stationID Files")
            
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
        
    def mergeStationFiles(self,tempPath,outputFile):
        '''
            Merges each station File into single Dataframe and s
        '''
        self.time.append(time.time())
        self.dataframe = pd.DataFrame(self.timeStamps, columns= ['TimeStamp'])
        for filename in os.listdir(tempPath):
            if filename.endswith('.csv'):
                filePath = os.path.join(tempPath,filename)
                stationDf = pd.read_csv(filePath,parse_dates= [0])
                
                self.dataframe = pd.merge(self.dataframe, stationDf, on = 'TimeStamp', how= 'left')
                os.remove(filePath)
        self.dataframe.fillna('NaN', inplace = True)
        self.dataframe.to_csv(outputFile)
        print("Created soramame data file")
        self.time.append(time.time())
        print('-------time taken for execution-------')
        print('query execution :',self.time[1] - self.time[0],' sec')
        print('dataframe merge :',self.time[3] - self.time[2],' sec')
        print('Total time :',self.time[3] - self.time[0],' sec')
        # print('query execution :',self.time[1] - self.time[2],' sec')
        
if __name__ == "__main__":
    if len(sys.argv) == 3:
        print(len(sys.argv),"input args")  
        dataExtraction = soramameSensorData()
        dataExtraction.getSensorData(tempPath=sys.argv[1], tableName = str('data'),  outputParam = int(13))
        dataExtraction.mergeStationFiles(tempPath = sys.argv[1],outputFile= sys.argv[2])
    elif len(sys.argv) == 4:
        print(len(sys.argv),"input args") 
        dataExtraction = soramameSensorData()
        dataExtraction.getSensorData(tempPath=sys.argv[1], tableName = sys.argv[3],  outputParam = int(13))
        dataExtraction.mergeStationFiles(tempPath = sys.argv[1],outputFile= sys.argv[2])
    elif len(sys.argv) == 5:
        print(len(sys.argv),"input args") 
        dataExtraction = soramameSensorData()
        dataExtraction.getSensorData(tempPath=sys.argv[1], tableName = sys.argv[3],  outputParam = int(sys.argv[4]))
        dataExtraction.mergeStationFiles(tempPath = sys.argv[1],outputFile= sys.argv[2])
    else :
        print("Error : Incorrect number of input parameters given : "+ str(len(sys.argv) - 1))
        print("Input Parameters-> temporary file path , outputFileName, tablename (default = data), outputParam (default = pm25)")
    