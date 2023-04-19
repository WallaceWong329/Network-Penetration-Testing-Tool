#!/usr/bin/env python3
import sqlite3
import db_connection

conn = db_connection.nmap_create_connection()
cur = conn.cursor()

def get_data():
    cur.execute("SELECT scan_id, ip, protocol_id, service_name, product, version, extrainfo, available_scripts, current_progress FROM nmap_services_version")
    data = cur.fetchall()
    return data

if __name__ == '__main__':
    get_data()