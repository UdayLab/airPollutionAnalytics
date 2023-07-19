import csv
import sys
from os import listdir
from os.path import isfile, join

import pandas as pd
import psycopg2

from config import config
from storingZipFileInDatabase.unZipAirPollution import getFolder


class insertDataIntoDatabaseFromZipFile:
    """
    Unzips soramame data and inserts the data into database and stores uninserted files in a CSV file.

    inputZipFile : Zip folder containing soramame data
    tempFolder   : Path to store unzipped files
    NOTE : Specify the name of the database in database.ini file
    
    """

    def __init__(self, inputZipFile, tempFolder, tableName="data"):
        self.inputFolder = getFolder(inputZipFile, tempFolder)
        self.table = tableName
        self.unsuccessfulInsertionFiles = []

    def insertData(self):
        inputFileName = self.inputFolder
        files = [f for f in listdir(self.inputFolder) if isfile(join(self.inputFolder, f))]
        for file in files:
            inputFileName = inputFileName + '/' + file

            # Connect to the PostgreSQL database server
            conn = None
            try:
                # read connection parameters
                params = config()

                # connect to the PostgreSQL server
                print('Connecting to the PostgreSQL database...')
                conn = psycopg2.connect(**params)

                # create a cursor
                cur = conn.cursor()

                # reading csv file
                csv_file = open(self.inputFileName, encoding="cp932", errors="", newline="")

                f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"',
                               skipinitialspace=True)

                header = next(f)
                for row in f:
                    for i in range(len(row)):

                        # filling missing values
                        # print(row[i])
                        if row[i] == '' or row[i] == '-' or '#' in row[i]:
                            row[i] = '9999'

                        # writing query
                    query = 'insert into ' + self.table + ' values(' + row[0] + ',\'' + row[1] + ' ' + row[
                        2] + ':00:00\'' + ',' + \
                            row[3] + ',' + row[4] + ',' + row[5] + ',' \
                            + row[6] + ',' + row[7] + ',' + row[8] + ',' + row[9] + ',' + row[10] + ',' + row[
                                11] + ',' + \
                            row[12] + ',' + row[13] + ',' + row[14] + ',-1' + ',' + row[16] + ',' + row[17] + ',' + row[
                                18] + ")"

                    # executing the query
                    cur.execute(query)
                conn.commit()
                print('Success')

                # close the communication with the PostgreSQL
                cur.close()

            except (Exception, psycopg2.DatabaseError) as error:
                print(error, self.inputFileName)
                self.unsuccessfulInsertionFiles.append(self.inputFileName + ' ' + str(error))

            finally:
                if conn is not None:
                    conn.close()
                    print('Database connection closed.')
                pd.DataFrame(self.unsuccessfulInsertionFiles).to_csv('unsuccessfulInsertionFiles.csv')


if __name__ == '__main__':
    if len(sys.argv) == 4:
        soramameDataInsertion = insertDataIntoDatabaseFromZipFile(sys.argv[1], sys.argv[2], sys.argv[3])
        soramameDataInsertion.insertData()
    elif len(sys.argv) == 3:
        soramameDataInsertion = insertDataIntoDatabaseFromZipFile(sys.argv[1], sys.argv[2], tableName='data')
        soramameDataInsertion.insertData()
    else:
        print("Error : Incorrect number of input parameters given : " + str(len(sys.argv) - 1))
        print("Input Parameters-> Zip Folder path, temporary folder path, table name (default = data) ")
