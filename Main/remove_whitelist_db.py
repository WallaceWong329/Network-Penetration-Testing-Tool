#!/usr/bin/env python3
import sys
import db_connection

conn = db_connection.nmap_create_connection()
cur = conn.cursor()

mac_addr = sys.argv[1]

def remove_mac_addr(mac_addr):
    cur.execute("DELETE FROM device_whitelist WHERE mac_addr = '" + mac_addr + "'")
    conn.commit()

remove_mac_addr(mac_addr)