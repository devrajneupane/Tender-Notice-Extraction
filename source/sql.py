import mysql.connector


def sql_initialize():
    # Connect to the database
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="dbms123",
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
            user="root",
            passwd="dbms123",
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

# myquery = "select * from tender_details"
# mycursor.execute(myquery)
