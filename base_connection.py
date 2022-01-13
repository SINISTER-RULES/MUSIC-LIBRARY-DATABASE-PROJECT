import mysql.connector

def connect_database():

    connection = mysql.connector.connect( host="localhost",
                                    user="root",
                                    password="pass123",
                                    database="music_library")
    return connection