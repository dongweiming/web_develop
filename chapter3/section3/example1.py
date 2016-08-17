# coding=utf-8
import MySQLdb
from consts import HOSTNAME, DATABASE, USERNAME, PASSWORD

try:
    con = MySQLdb.connect(HOSTNAME, USERNAME, PASSWORD, DATABASE)
    cur = con.cursor()
    cur.execute("SELECT VERSION()")
    ver = cur.fetchone()
    print "Database version : %s " % ver
except MySQLdb.Error as e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    exit(1)
finally:
    if con:
        con.close()
