#!/usr/bin/env python3
import sqlite3
import db_connection

conn = db_connection.nmap_create_connection()
cur = conn.cursor()


def drop_data():
    cur.execute("DELETE FROM device_whitelist")
    conn.commit()
    cur.execute("DELETE FROM sqlite_sequence WHERE name IN ('device_whitelist')")
    conn.commit()
    
if __name__ == '__main__':
    drop_data()
