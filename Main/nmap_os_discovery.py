#!/usr/bin/env python3
import sqlite3
import nmap
import sys
import db_connection
import subprocess
import get_whitelist
import socket

conn = db_connection.nmap_create_connection()
cur = conn.cursor()

host = sys.argv[1]
current_progress = 0

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

this_host_ipv4 = get_ip_address()

def ping_scan(host):
    list_of_up_hosts = []

    nm = nmap.PortScanner()
    nm.scan(hosts = host, arguments = '-n -sn')    
    nmap_output = nm._scan_result

    for ip, host in nmap_output["scan"].items():
        if ip == this_host_ipv4:
            pass
        else:
            list_of_up_hosts.append(ip)

    max_host = len(list_of_up_hosts)
    print(list_of_up_hosts)
    for host in list_of_up_hosts:
        global current_progress
        current_progress = int((list_of_up_hosts.index(host) + 1) / max_host * 100)
        os_scan(host)

def os_scan(host):
    nm = nmap.PortScanner()
    nm.scan(hosts = host, arguments = '-T4 -Pn -sS -O -R')
    nmap_output = nm._scan_result

    whitelists = get_whitelist.get_data()
    data = []
    for whitelist in whitelists:
        data.append(whitelist[0])


    for ip, host in nmap_output["scan"].items():
        #host info
        try:
            ipv4_addr = host['addresses']['ipv4']
        except:
            ipv4_addr = "None"
        try:
            mac_addr = host['addresses']['mac']
        except:
            mac_addr = "None"
        try:
            if host['hostnames'][0]['name']:
                host_name = host['hostnames'][0]['name']
            else:
                host_name = "None"
        except:
            host_name = "None"
        try:
            if host['vendor']:
                for mac_addr, vendor in host['vendor'].items():
                    vendor = vendor
            else:
                vendor = "None"
        except:
            vendor = "None"

        try:
            uptime = host['uptime']['lastboot']
        except:
            uptime = "None"
        #OS info
        try:
            os_name = host['osmatch'][0]['name']
        except:
            os_name = "None"
        try:
            os_vendor = host['osmatch'][0]['osclass'][0]['vendor']
        except:
            os_vendor = "None"            
        try:
            os_family = host['osmatch'][0]['osclass'][0]['osfamily']
        except:
            os_family = "None"  
        try:
            os_gen = host['osmatch'][0]['osclass'][0]['osgen']
        except:
            os_gen = "None"
        try:
            os_accuracy = host['osmatch'][0]['accuracy']
        except:
            os_accuracy = "None"

        open_port = []
        try:
            for key, value in host['tcp'].items():
                if value['state'] == "open":
                    open_port.append(key)
        except:
            open_port = []

        global current_progress
        #print([ipv4_addr, mac_addr, host_name, vendor, uptime, os_name, os_vendor, os_family, os_gen, os_accuracy, open_port, current_progress])
        
        if mac_addr in data:
            cur.execute("INSERT INTO nmap_scan(host_ipv4,host_mac_addr,host_name,host_vendor,host_uptime,os_name,os_vendor,os_family,os_gen,os_accuracy,current_progress,whitelist) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", \
                        (ipv4_addr, mac_addr, host_name, vendor, uptime, os_name, os_vendor, os_family, os_gen, os_accuracy, current_progress, "TRUE"))
            conn.commit()
        else:
            cur.execute("INSERT INTO nmap_scan(host_ipv4,host_mac_addr,host_name,host_vendor,host_uptime,os_name,os_vendor,os_family,os_gen,os_accuracy,current_progress,whitelist) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", \
                        (ipv4_addr, mac_addr, host_name, vendor, uptime, os_name, os_vendor, os_family, os_gen, os_accuracy, current_progress, "FALSE"))
            conn.commit()

        last_id = cur.lastrowid

        for port in open_port: 
            cur.execute("INSERT INTO nmap_port(scan_id, open_port) VALUES(?, ?)",(last_id, port))
            conn.commit()

        

if __name__ == "__main__":
    ping_scan(host)