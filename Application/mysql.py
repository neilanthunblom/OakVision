#!/usr/bin/python
print "Content-type:text/html\n\n"
import mysql.connector

try:
 conn = mysql.connector.connect (
  host = "",
  user = "",
  passwd = "",
  db = "oakvision_v1_mysql")

except mysql.Error as e:
 print("Error %d: %s" % (e.args[0], e.args[1]))
 sys.exit (1)

print "connected to the database"