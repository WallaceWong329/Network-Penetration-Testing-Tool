#!/usr/bin/env python3
import sqlite3
import db_connection

conn = db_connection.nmap_create_connection()
cur = conn.cursor()

def get_data():
    cur.execute("SELECT scan_id, host_ipv4, port, script_name, script_output, info_found FROM nmap_scripts")
    data = cur.fetchall()
    return data

if __name__ == '__main__':
    print(get_data())