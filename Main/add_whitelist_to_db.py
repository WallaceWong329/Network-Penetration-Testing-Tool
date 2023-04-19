#!/usr/bin/env python3
import sys
import db_connection

conn = db_connection.nmap_create_connection()
cur = conn.cursor()

mac_addr = sys.argv[1]

try:
    remark = sys.argv[2]
except:
    remark = ""

def get_data():
    cur.execute("SELECT mac_addr FROM device_whitelist")
    data = cur.fetchall()    
    return data

all_mac_addr = get_data()

def add_mac_addr(mac_addr, remark):
    if any(mac_addr in tpl for tpl in all_mac_addr):
        pass
    else:
        cur.execute("INSERT INTO device_whitelist(mac_addr, remark) VALUES(?, ?)",(mac_addr, remark))
        conn.commit()

add_mac_addr(mac_addr, remark)