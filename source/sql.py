import mysql.connector
from pathlib import Path
from dotenv import dotenv_values

path = Path(__file__).parent
tesseract_exec = dotenv_values(path.joinpath(".env"))["TESSERACT_EXECUTABLE"]
USER_NAME="anuj"
USER_PASS="anuj123"

def sql_initialize():
    # Connect to the database
    try:
        mydb = mysql.connector.connect(
            host="localhost",
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
                dat DATE,\
                newspaper varchar(255),\
                page int,\
                imageName varchar(255))"

    mycursor.execute(myquery)

def sql_insert(dat, newspaper, page, imageName):
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
    myquery = "INSERT INTO tender_details (dat, newspaper, page, imageName) VALUES (%s, %s, %s, %s)"
    mycursor.execute(myquery, (dat, newspaper, page, imageName))
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")


def sql_query_date():
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

# myquery = "select * from tender_details"
# mycursor.execute(myquery)
