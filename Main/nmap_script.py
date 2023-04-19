#!/usr/bin/env python3
import nmap
import re
import sys
import subprocess
import db_connection

conn = db_connection.nmap_create_connection()
cur = conn.cursor()

host = sys.argv[1]
scanId = sys.argv[2]
protocol_id = sys.argv[3]
scripts = sys.argv[4]

def script(host, scanId, protocol_id, scripts):
    nm = nmap.PortScanner()
    #+ ' --script-args userdb=/home/kali/FYP/Main/usernames.lst,passdb=/home/kali/FYP/Main/passwords.lst'
    nm.scan(hosts = host, arguments =  '-p '+ protocol_id + ' --script ' + scripts + ' --script-args userdb=/home/kali/FYP/Main/usernames.lst,passdb=/home/kali/FYP/Main/passwords.lst')
    nmap_output = nm._scan_result
    for ip_address, data in nmap_output['scan'].items():
        for port, port_data in data['tcp'].items():
            if 'script' in port_data:
                for script in port_data['script']:
                    script_output = port_data['script'][script].replace("\n", "<br>").replace("<br>  ", "", 1)
                    script_output = re.sub(r'^<br>\s*', '', script_output)
                    cur.execute("INSERT INTO nmap_scripts(scan_id, host_ipv4, port, script_name, script_output, info_found) VALUES(?, ?, ?, ?, ?, ?)",(scanId, host, protocol_id, scripts, script_output, "TRUE"))
                    conn.commit()
            else:
                cur.execute("INSERT INTO nmap_scripts(scan_id, host_ipv4, port, script_name, script_output, info_found) VALUES(?, ?, ?, ?, ?, ?)",(scanId, host, protocol_id, scripts, "Nothing...", "FALSE"))
                conn.commit()
script(host, scanId, protocol_id, scripts)