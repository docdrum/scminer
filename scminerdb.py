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

        cursor.execute("DROP TABLE IF EXISTS minerals")
        cursor.execute("CREATE TABLE minerals (id INTEGER PRIMARY KEY, name TEXT, value REAL)")
        cursor.execute("INSERT INTO minerals VALUES (1, 'Quantainium', 88.0)")
        cursor.execute("INSERT INTO minerals VALUES (2, 'Bexalite', 40.66)")
        cursor.execute("INSERT INTO minerals VALUES (3, 'Taranite',  32.58)")
        cursor.execute("INSERT INTO minerals VALUES (4, 'Borase', 32.58)")
        cursor.execute("INSERT INTO minerals VALUES (5, 'Laranite', 31.02)")
        cursor.execute("INSERT INTO minerals VALUES (6, 'Agricium', 27.50)")
        cursor.execute("INSERT INTO minerals VALUES (7, 'Hephaestanite', 14.76)")
        cursor.execute("INSERT INTO minerals VALUES (8, 'Titanium', 8.94)")
        cursor.execute("INSERT INTO minerals VALUES (9, 'Diamond', 7.36)")
        cursor.execute("INSERT INTO minerals VALUES (10, 'Gold', 6.4)")
        cursor.execute("INSERT INTO minerals VALUES (11, 'Copper', 5.74)")
        cursor.execute("INSERT INTO minerals VALUES (12, 'Beryl', 4.42)")
        cursor.execute("INSERT INTO minerals VALUES (13, 'Tungsten', 4.1)")
        cursor.execute("INSERT INTO minerals VALUES (14, 'Corundum', 2.7)")
        cursor.execute("INSERT INTO minerals VALUES (15, 'Quartz', 1.56)")
        cursor.execute("INSERT INTO minerals VALUES (16, 'Aluminium', 1.34)")

        cursor.execute("DROP TABLE IF EXISTS refineries")
        cursor.execute("CREATE TABLE refineries (id INTEGER PRIMARY KEY, name TEXT)")
        cursor.execute("INSERT INTO refineries VALUES (1, 'ARC L1')")
        cursor.execute("INSERT INTO refineries VALUES (2, 'CRU L1')")
        cursor.execute("INSERT INTO refineries VALUES (3, 'HUR L1')")
        cursor.execute("INSERT INTO refineries VALUES (4, 'HUR L2')")
        cursor.execute("INSERT INTO refineries VALUES (5, 'MIC L1')")

        cursor.execute("DROP TABLE IF EXISTS orders")
        cursor.execute("CREATE TABLE orders (" +
            "id INTEGER PRIMARY KEY, refinery_id INTEGER, jobstart INTEGER, " +
            "dur_h INTEGER, dur_m INTEGER, " +
            "FOREIGN KEY(refinery_id) REFERENCES refineries(id) ON UPDATE CASCADE ON DELETE CASCADE)")

        cursor.execute("INSERT INTO orders VALUES(1, 2, 0, 0, 0)")
        cursor.execute("INSERT INTO orders VALUES(2, 2, 0, 0, 0)")
        cursor.execute("INSERT INTO orders VALUES(3, 2, 0, 0, 0)")

        cursor.execute("DROP TABLE IF EXISTS order_details")
        cursor.execute("CREATE TABLE order_details (" +
            "order_id INTEGER, mineral INTEGER, cscu INTEGER, " +
            "FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE)")

        cursor.execute("INSERT INTO order_details VALUES(1, 9, 45)")
        cursor.execute("INSERT INTO order_details VALUES(1, 4, 119)")
        cursor.execute("INSERT INTO order_details VALUES(1, 2, 1344)")

        cursor.execute("INSERT INTO order_details VALUES(2, 4, 52)")
        cursor.execute("INSERT INTO order_details VALUES(2, 1, 1989)")

        cursor.execute("INSERT INTO order_details VALUES(3, 8, 1428)")

        cursor.execute("DROP TABLE IF EXISTS meta")
        cursor.execute("CREATE TABLE meta (key TEXT, value TEXT)")
        cursor.execute("INSERT INTO meta VALUES ('dbversion', '1.0')")

        cursor.execute("DROP VIEW IF EXISTS partial_order_value")
        cursor.execute('''
            CREATE VIEW partial_order_value AS
                SELECT orders.id AS order_id, refineries.name AS refinery, minerals.name AS mineral,
                    order_details.cscu AS cSCU, cSCU * minerals.value AS value
                FROM orders
                    JOIN order_details ON orders.id = order_details.order_id
                    JOIN minerals ON order_details.mineral = minerals.id
                    JOIN refineries ON orders.refinery_id = refineries.id''')

        cursor.execute('''
            CREATE VIEW order_value AS
                SELECT order_id, refinery, sum(cSCU), sum(value)
                FROM partial_order_value
                GROUP BY order_id''')
        cursor.connection.commit()

