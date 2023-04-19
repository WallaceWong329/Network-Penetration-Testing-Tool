#!/usr/bin/env python3
import nmap
import sys
import subprocess
import db_connection

conn = db_connection.nmap_create_connection()
cur = conn.cursor()

host = sys.argv[1]
scanId = sys.argv[2]
ports = sys.argv[3]
progress = int(0)


port_num = ""

#Nmap NSE Script list

#MYSQL
script_mysql = ["mysql-brute",          #Performs password guessing against MySQL.
                "mysql-empty-password"] #Checks for MySQL servers with an empty password for root or anonymous.

#SMB
script_smb = ["smb-brute",              #Attempts to guess username/password combinations over SMB, storing discovered combinations for use in other scripts
                "smb-enum-domains",     #Attempts to enumerate domains on a system, along with their policies
                "smb-enum-groups",      #Obtains a list of groups from the remote Windows system, as well as a list of the group's users
                "smb-enum-services",    #Retrieves the list of services running on a remote Windows system
                "smb-enum-shares",      #Attempts to list shares using the srvsvc.NetShareEnumAll MSRPC function and retrieve more information about them using srvsvc.NetShareGetInfo
                "smb-enum-users",       #Attempts to enumerate the users on a remote Windows system, with as much information as possible, through two different techniques (both over MSRPC, which uses port 445 or 139; see smb.lua) 
                "smb-system-info"]      #Pulls back information about the remote system from the registry

#SSH
script_ssh = ["ssh-brute"]  #Performs brute-force password guessing against ssh servers

#HTTP
script_http = ["http-apache-server-status",   #Attempts to retrieve the server-status page for Apache webservers that have mod_status enabled.
                "http-cookie-flags",          #Examines cookies set by HTTP services
                "http-php-version",           #Attempts to retrieve the PHP version from a web server
                "http-wordpress-brute",       #Performs brute force password auditing against Wordpress CMS/blog installations
                "http-wordpress-enum",        #Enumerates themes and plugins of Wordpress installations.
                "http-wordpress-users"]       #Enumerates usernames in Wordpress blog/CMS installations by exploiting an information disclosure vulnerability existing in versions 2.6, 3.1, 3.1.1, 3.1.3 and 3.2-beta2 and possibly others  
                                            


def services_verions(host, scanId, ports):
    nm = nmap.PortScanner()
    nm.scan(hosts = host, arguments = '-sV -p ' + ports)    
    nmap_output = nm._scan_result
    for ip_address, data in nmap_output['scan'].items():
        for port, port_data in data['tcp'].items():
            global port_num
            port_num = port
            scripts = ""
            if port_data['name'] == "ssh":
                scripts = script_ssh
            if port_data['name'] == "smb":
                scripts = script_smb
            if port_data['name'] == "mysql":
                scripts = script_mysql            
            if port_data['name'] == "http":
                scripts = script_http
            cur.execute("INSERT INTO nmap_services_version(scan_id, ip, protocol_id, service_name, product, version, extrainfo, available_scripts) VALUES(?, ?, ?, ?, ? ,? ,? , ?)",(scanId, host, port, port_data['name'], port_data['product'], port_data['version'], port_data['extrainfo'], str(scripts)))
            conn.commit()
            
values = ports.split(',')
total_progress = len(values)

for index, val in enumerate(values):
    try:
        services_verions(host, scanId, val)
    except:
        pass
    current_progress = int((index + 1 ) / total_progress * 100)
    cur.execute("UPDATE nmap_services_version SET current_progress = " + str(current_progress) + " WHERE protocol_id = " + str(port_num))
    conn.commit()