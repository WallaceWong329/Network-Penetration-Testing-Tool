#!/usr/bin/env python3
import sqlite3
import db_connection

conn = db_connection.nmap_create_connection()
cur = conn.cursor()

def get_data():
    cur.execute("SELECT os_vendor, COUNT(*) as count FROM nmap_scan GROUP BY os_vendor")
    data = cur.fetchall()
    return data

if __name__ == '__main__':
    get_data()