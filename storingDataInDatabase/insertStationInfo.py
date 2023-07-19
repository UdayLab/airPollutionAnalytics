#!/usr/bin/python
import csv
import re
import matplotlib.pyplot as plt
import psycopg2
from config import config

# SQL query to create stationInformation table
# query = CREATE TABLE stationInfo(sid int not null, geog geography(POINT,4326), addressInfo varchar)

def stationInfoInsertion(inputFile):

    """
    Inserts station information into the database (database connection params specified in database.ini file).
    
    inputFile : File containing station information (-stationAdd.txt file in Data folder) 
    """
    
    # Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        csv_file = open("stationInfo.csv", encoding="utf-8", errors="",
                        newline="")
        f = csv.reader(csv_file, delimiter=",")
        for row in f:
            for i in range(len(row)):
                query = "insert into station_info values("+row[1]+','+row[2]+',\''+row[3]+'\''+")"
            
            # executes query
            cur.execute(query)
        conn.commit()
        cur.close()
    
    # Exception handling
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            # close database connection
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error : Incorrect number of input parameters given : "+ str(len(sys.argv) - 1))
        print("Input Parameters-> input FileName")
    else:
        stationInfoInsertion(sys.argv[1])

    
