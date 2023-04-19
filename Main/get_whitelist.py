#!/usr/bin/env python3
import sqlite3
import nmap
import sys
import db_connection

conn = db_connection.nmap_create_connection()
cur = conn.cursor()


def get_data():
    cur.execute("SELECT mac_addr, remark FROM device_whitelist")
    data = cur.fetchall()    
    return data

if __name__ == '__main__':
    get_data()
