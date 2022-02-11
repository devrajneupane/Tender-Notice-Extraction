import mysql.connector
from pathlib import Path
from dotenv import dotenv_values
import os
import sys

from log import Logger


path = Path(__file__).parent

dir_lst=os.listdir(path)
if ".env" not in dir_lst:
    print(f"==>\n.env file not found in: \n{path}\n<==")
    exit()
env_path = path.joinpath(".env")

#load values form .env file
try:
    tesseract_exec = dotenv_values(env_path)["TESSERACT_EXECUTABLE"]
except KeyError:
    print("TESSERACT_EXECUTABLE not found in .env file")
    exit()

try:
    USER_NAME=dotenv_values(env_path)["SQL_USER_NAME"]
except KeyError:
    print("SQL_USER_NAME not found in .env file")
    exit()

try:
    USER_PASS=dotenv_values(env_path)["SQL_USER_PASS"]
except KeyError:
    print("SQL_USER_PASS not found in .env file")
    exit()

try:    
    HOST=dotenv_values(env_path)["SQL_HOST"]
except KeyError:
    print("SQL_HOST not found in .env file")
    exit()

def sql_initialize():
    sys.stdout=Logger()
    # Connect to the database
    try:
        mydb = mysql.connector.connect(
            host=HOST,
            user=USER_NAME,
            passwd=USER_PASS,
        )
    except mysql.connector.Error as err:
        print(err)

    mycursor = mydb.cursor()
    # Create a database if it doesn't exist
    myquery = "CREATE DATABASE IF NOT EXISTS tender"
    mycursor.execute(myquery)
    # use the database
    myquery = "USE tender"
    mycursor.execute(myquery)
    # create a table
    myquery = "CREATE TABLE IF NOT EXISTS tender_details(\
                id int AUTO_INCREMENT PRIMARY KEY,\
                img_id int,\
                dat DATE,\
                newspaper varchar(255),\
                page int,\
                imageName varchar(255))"

    mycursor.execute(myquery)

def sql_insert(img_id,dat, newspaper, page, imageName):
    """
    This function inserts the data into the database:
    1) img_id: id of the image
    2) dat: date of the tender
    3) newspaper: name of the newspaper
    4) page: page number of the newspaper where the tender was found
    5) imageName: name of the image 
    """
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user=USER_NAME,
            passwd=USER_PASS,
        )
    except mysql.connector.Error as err:
        print(err)

    mycursor = mydb.cursor()
    myquery = "USE tender"
    mycursor.execute(myquery)

    #insert the values passed to the function
    myquery = "INSERT INTO tender_details (img_id,dat, newspaper, page, imageName) VALUES (%s,%s, %s, %s, %s)"
    mycursor.execute(myquery, (img_id,dat, newspaper, page, imageName))
    mydb.commit()
    print(f"\t\t\t==>{mycursor.rowcount} record inserted")


def sql_query_date():
    """
    This function returns the date of the last tender added to the database
    """
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user=USER_NAME,
            passwd=USER_PASS,
        )
    except mysql.connector.Error as err:
        print(err)

    mycursor = mydb.cursor()
    myquery = "USE tender"
    mycursor.execute(myquery)
    myquery="SELECT dat FROM tender_details ORDER BY id DESC LIMIT 1"
    mycursor.execute(myquery)
    for x in mycursor:
        return x

