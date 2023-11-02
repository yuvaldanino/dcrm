# file that makes the new database 

import mysql.connector

#shows  version of mysql connector 
#print(mysql.connector.__version__)

dataBase = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "yuval1234"
)

#new cursor object 
cursorObject = dataBase.cursor()

#create database 
cursorObject.execute("CREATE DATABASE elderco")

print("All done!")