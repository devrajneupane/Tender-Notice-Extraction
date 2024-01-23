import os
import sys
import mysql.connector
from pathlib import Path
from log import Logger
from utils import config

sys.stdout = Logger()


def sql_initialize(query, is_insert=False):
    """
    A database named tender must be exists with a table named tender_web_tender with following fields
    id, image_id, date_published, newspaper_source, page_number, image_path
    Run following SQL query if the databse and table doesn't exist already
    CREATE DATABASE IF NOT EXISTS tender;
    USE tender;
    CREATE TABLE IF NOT EXISTS tender_web_tender(
            id int AUTO_INCREMENT PRIMARY KEY,
            image_id int,
            date_published DATE,
            newspaper_source varchar(255),
            page_number int,
            image_path varchar(255));

    """
    sys.stdout = Logger()

    try:
        with mysql.connector.connect(host=config["SQL_HOST"], user=config["SQL_USER_NAME"], password=config["SQL_USER_PASS"], database="tender") as connection:
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


def is_duplicate(image_path):
    check_duplicate = f"SELECT * FROM tender_web_tender WHERE image_path = '{image_path}'"
    data = sql_initialize(check_duplicate)
    return True if data else False


def sql_insert(img_id, date, newspaper, page, image_path):
    """
     This function inserts the data into the database:
     1) image_id: id of the image
     2) date_published: date of the tender
     3) newspaper_source: name of the newspaper
     4) page_number: page number of the newspaper where the tender was found
     5) image_path: name of the image
     """
    sys.stdout = Logger()

    insert_query = f"INSERT INTO tender_web_tender (image_id, date_published, newspaper_source, page_number, image_path)\
                 VALUES ({img_id}, '{date}', '{newspaper}', {page}, '{image_path}')"
    if not is_duplicate(image_path):
        if sql_initialize(insert_query, True):
            print(f"\t\t\t==>{image_path.split('/')[3]} inserted into database")


def sql_query_info():
    """
    This function returns the date of the last tender added to the database and a boolean value as a flag
    """

    date_query = "SELECT date_published FROM tender_web_tender ORDER BY id DESC LIMIT 1"
    try:
        latest_date = sql_initialize(date_query)[0]
    except IndexError:
        latest_date = sql_initialize(date_query)

    # Failsafe for empty database
    if latest_date:
        source_query = f"SELECT DISTINCT newspaper_source FROM tender.tender_web_tender WHERE date_published = '{latest_date[0]}'"
        data = [data for data in sql_initialize(source_query) for data in data]
        return latest_date, 'kantipur' in data or 'kathmandupost' in data
    
    else:
        return None, False
