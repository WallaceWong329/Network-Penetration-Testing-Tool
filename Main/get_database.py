#!/usr/bin/env python3
import sqlite3
import nmap
import sys
import db_connection

def group_concat(values, separator=', '):
    return separator.join(str(v) for v in values if v is not None)

conn = db_connection.nmap_create_connection()
conn.create_aggregate('group_concat', 2, group_concat)

cur = conn.cursor()


def get_data():
    cur.execute("SELECT nmap_scan.id, nmap_scan.host_ipv4, group_concat(nmap_port.open_port), host_mac_addr, host_name, host_vendor, host_uptime,"
            "os_name, os_vendor, os_family ,os_gen ,os_accuracy, whitelist, current_progress AS open_ports,current_progress "
            "FROM nmap_scan LEFT JOIN nmap_port ON nmap_scan.id = nmap_port.scan_id "
            "GROUP BY nmap_scan.host_ipv4 ORDER BY current_progress, open_ports")
    data = cur.fetchall()
    return data

if __name__ == '__main__':
    get_data()
