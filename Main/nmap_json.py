#!/usr/bin/env python3
import nmap
import json
from datetime import date

host = "172.18.38.35"

nm = nmap.PortScanner()
nm.scan(hosts = host, arguments = '-sV')
nmap_output = nm._scan_result
today = date.today()
filename = today.strftime("%b-%d-%Y")

# Serializing json
json_object = json.dumps(nmap_output, indent=4)
 
# Writing to sample.json
with open(filename + ".json", "w") as outfile:
    outfile.write(json_object)