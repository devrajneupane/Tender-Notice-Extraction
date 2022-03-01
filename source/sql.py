import os
import sys
import mysql.connector
from pathlib import Path
from dotenv import dotenv_values
from log import Logger

sys.stdout = Logger()

path = Path(__file__).parent

dir_lst = os.listdir(path)
if ".env" not in dir_lst:
    print(f"==>\n.env file not found in: \n{path}\n<==")
    exit()
env_path = path.joinpath(".env")

# load values form .env file
try:
    tesseract_exec = dotenv_values(env_path)["TESSERACT_EXECUTABLE"]
except KeyError:
    print("TESSERACT_EXECUTABLE not found in .env file")
    exit()

try:
    USER_NAME = dotenv_values(env_path)["SQL_USER_NAME"]
except KeyError:
    print("SQL_USER_NAME not found in .env file")
    exit()

try:
    USER_PASS = dotenv_values(env_path)["SQL_USER_PASS"]
except KeyError:
    print("SQL_USER_PASS not found in .env file")
    exit()

try:
    HOST = dotenv_values(env_path)["SQL_HOST"]
except KeyError:
    print("SQL_HOST not found in .env file")
    exit()


def sql_initialize(query, is_insert):
    """
    A database named tender must be exists with a table named tenderweb_tender with following fields
    id, image_id, date_published, newspaper_source, page_number, image_name
    Run following SQL query if the databse and table doesn't exist already
    CREATE DATABASE IF NOT EXISTS tender;
    USE tender;
    CREATE TABLE IF NOT EXISTS tenderweb_tender(
            id int AUTO_INCREMENT PRIMARY KEY,
            image_id int,
            date_published DATE,
            newspaper_source varchar(255),
            page_number int,
            image_name varchar(255));

    """
    sys.stdout = Logger()

    try:
        with mysql.connector.connect(host=HOST, user=USER_NAME, password=USER_PASS, database="tender") as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                if not is_insert:
                    return cursor.fetchall()

                else:
                    connection.commit()
                    return True

    except mysql.connector.Error as e:
        print(f"Following Error occured\n{e}")
        return False


def is_duplicate(image_name):
    check_duplicate = f"SELECT * FROM tenderweb_tender WHERE image_name = '{image_name}'"
    data = sql_initialize(check_duplicate, False)
    return True if data else False


def sql_insert(img_id, date, newspaper, page, image_name):
    """
     This function inserts the data into the database:
     1) image_id: id of the image
     2) date_published: date of the tender
     3) newspaper_source: name of the newspaper
     4) page_number: page number of the newspaper where the tender was found
     5) image_name: name of the image
     """
    sys.stdout = Logger()

    insert_query = f"INSERT INTO tenderweb_tender (image_id, date_published, newspaper_source, page_number, image_name)\
                 VALUES ({img_id}, '{date}', '{newspaper}', {page}, '{image_name}')"
    if not is_duplicate(image_name):
        if sql_initialize(insert_query, True):
            print(f"\t\t\t==>{image_name.split('/')[3]} inserted into database")


def sql_query_info():
    """
    This function returns the date of the last tender added to the database and a boolean value as a flag
    """

    date_query = "SELECT date_published FROM tenderweb_tender ORDER BY id DESC LIMIT 1"
    try:
        latest_date = sql_initialize(date_query, False)[0]
    except IndexError:
        latest_date = sql_initialize(date_query, False)

    source_query = f"SELECT DISTINCT newspaper_source FROM tender.tenderweb_tender WHERE date_published = '{latest_date[0]}'"
    data = [data for data in sql_initialize(source_query, False) for data in data]
    return latest_date, 'kantipur' in data or 'kathmandupost' in data
