import sqlite3
import db_connection
def nmap_create_connection():
    conn = None
    try:
        conn = sqlite3.connect('./database/nmap.db')
        cur = conn.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS device_whitelist (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        mac_addr VARCHAR(17) NOT NULL,
                        remark VARCHAR(255)
                    )
                    """)

        cur.execute("""CREATE TABLE IF NOT EXISTS nmap_scripts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        scan_id INTEGER NOT NULL,
                        host_ipv4 VARCHAR(15) NOT NULL,
                        port VARCHAR(255) NOT NULL,
                        script_name VARCHAR(255),
                        script_output VARCHAR(255),
                        info_found VARCHAR(255),
                        FOREIGN KEY (scan_id) REFERENCES nmap_scan(id)
                    )
                    """)

        cur.execute("""CREATE TABLE IF NOT EXISTS nmap_scan (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        host_ipv4 VARCHAR(15) NOT NULL,
                        host_mac_addr VARCHAR(17),
                        host_name VARCHAR(50),
                        host_vendor VARCHAR(50),
                        host_uptime INTEGER,
                        os_name VARCHAR(255),
                        os_vendor VARCHAR(50),
                        os_family VARCHAR(50),
                        os_gen VARCHAR(50),
                        os_accuracy INTEGER,                
                        current_progress INTEGER,
                        whitelist VARCHAR(255)
                    )
                    """)
                    
        cur.execute("""CREATE TABLE IF NOT EXISTS nmap_port (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        scan_id INTEGER NOT NULL,
                        open_port VARCHAR(255) NOT NULL,
                        FOREIGN KEY (scan_id) REFERENCES nmap_scan(id)
                    )
                    """)
                    
        cur.execute("""CREATE TABLE IF NOT EXISTS nmap_services_version (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        scan_id INTEGER NOT NULL,
                        ip VARCHAR(15),
                        protocol_id VARCHAR(50),
                        service_name VARCHAR(50),
                        product VARCHAR(50),
                        version VARCHAR(50),
                        extrainfo VARCHAR(50),
                        available_scripts VARCHAR(255),
                        current_progress INTEGER,
                        FOREIGN KEY (scan_id) REFERENCES nmap_scan(id)
                    )
                    """)
    except sqlite3.Error as error:
        print(error)
    return conn
