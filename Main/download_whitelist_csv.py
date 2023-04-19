#!/usr/bin/env python3
import sqlite3
import nmap
import sys
import db_connection
import csv
import os

conn = db_connection.nmap_create_connection()
cur = conn.cursor()

if not os.path.exists('download'):
    os.makedirs('download')

def get_data():
    cur.execute("SELECT mac_addr, remark FROM device_whitelist")
    data = cur.fetchall()    
    return data

def to_csv():
    data = get_data()
    with open('download/all_whitelist.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['mac_address', 'remark'])
        for row in data:
            writer.writerow(row)

if __name__ == '__main__':
    to_csv()
