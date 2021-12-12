import os
import sqlite3

# path to database (TODO: This is only for windows)
dbfile = os.getenv('APPDATA') + '\\scminer.db'
dbversion = "1.0"

class DB:
    connection = None

    def __init__(self):
        if type(self).connection is None:
            self.createConnection()

    def createConnection(self):
        type(self).connection = sqlite3.connect(dbfile)
        cursor = type(self).connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        try:
            if not self.getVersion() == dbversion:
                self.upgradeDatabase()
        except:
            self.createDatabase()

    def createDatabase(self):
        cursor = type(self).connection.cursor()
        cursor.execute("DROP TABLE refineries")
        cursor.execute("CREATE TABLE refineries (id INTEGER PRIMARY KEY, name TEXT)")
        cursor.execute("INSERT INTO refineries VALUES (NULL, 'ARC L1')")
        cursor.execute("INSERT INTO refineries VALUES (NULL, 'CRU L1')")
        cursor.execute("INSERT INTO refineries VALUES (NULL, 'HUR L1')")
        cursor.execute("INSERT INTO refineries VALUES (NULL, 'HUR L2')")
        cursor.execute("INSERT INTO refineries VALUES (NULL, 'MIC L1')")

        cursor.execute("DROP TABLE IF EXISTS orders")
        cursor.execute("CREATE TABLE orders (" +
            "id INTEGER PRIMARY KEY, refinery_id INTEGER, jobstart INTEGER, " +
            "dur_h INTEGER, dur_m INTEGER, " +
            "FOREIGN KEY(refinery_id) REFERENCES refineries(id) ON UPDATE CASCADE)")

        cursor.execute("DROP TABLE IF EXISTS order_details")
        cursor.execute("CREATE TABLE order_details (" +
            "order_id INTEGER, mineral INTEGER, cscu INTEGER, " +
            "FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE)")

        cursor.execute("DROP TABLE IF EXISTS meta")
        cursor.execute("CREATE TABLE meta (key TEXT, value TEXT)")
        cursor.execute("INSERT INTO meta VALUES ('dbversion', '1.0')")
        cursor.connection.commit()

