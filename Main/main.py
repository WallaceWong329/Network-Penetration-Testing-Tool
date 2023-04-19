from bottle import Bottle, run, template, get, post, debug, route, request, redirect, response, error, static_file
import gunicorn
import subprocess
import json
import nmap
import get_database
import get_whitelist
import get_script_data
import get_open_port
import get_family
import get_vendor
import get_whitelist_summary
import get_services_version_data
import db_connection
import csv
import io

data = {}
app = Bottle()

conn = db_connection.nmap_create_connection()
cur = conn.cursor()

sessions_keys = "b94661627c30984de941d9c1146b4303"

@app.route('/', method=['GET', 'POST'])
def web_login_page():
    
    if request.method == 'GET':
        session_token = request.get_cookie("session_token")
        if (session_token == sessions_keys):
            return redirect("/home")
        return template('webpage/login', login_status = "")

    elif request.method == 'POST':
        if 'login' in request.POST: 
            username = request.forms.get('username')  # username: admin
            password = request.forms.get('password')  # password: P@ssw0rdAdmin
            
            # Check if username and password are correct
            if username == "admin" and password == "P@ssw0rdAdmin":    
                # Set the session token as a cookie
                response.set_cookie("session_token", sessions_keys, max_age=3600)
                return redirect("/home")
            else:
                return template('webpage/login', login_status = "Incorrect username or password!")
        else:
           return template('webpage/login', login_status = "Incorrect username or password!")

@app.route('/home', method='GET')
def web_home_page():
    # check if user is authenticated
    session_token = request.get_cookie("session_token")
    if not session_token or session_token != sessions_keys:
        return redirect("/")
    else:
        return template('webpage/index')


@app.route('/scanner', method=['GET', 'POST'])
def web_scan_page():
    # check if user is authenticated
    session_token = request.get_cookie("session_token")
    if not session_token or session_token != sessions_keys:
        return redirect("/")
    else:
        if request.method == 'GET':
            return template('webpage/scanner')
        elif request.method == 'POST':        
            cur.execute("DELETE FROM nmap_services_version")
            conn.commit()
            cur.execute("DELETE FROM nmap_scripts")
            conn.commit()        
            cur.execute("DELETE FROM nmap_port")
            conn.commit()
            cur.execute("DELETE FROM nmap_scan")
            conn.commit()
            cur.execute("DELETE FROM sqlite_sequence WHERE name IN ('nmap_scan', 'nmap_port', 'nmap_scripts', 'nmap_services_version')")
            conn.commit()
            ipaddress = request.forms.get('ipaddress')
            cmd = "sudo python nmap_os_discovery.py " + ipaddress
            subprocess.Popen(cmd, shell=True)
            return redirect('scanner_result')
        

@app.route('/get_progress', method='GET')
def get_progress():
    # check if user is authenticated
    session_token = request.get_cookie("session_token")
    if not session_token or session_token != sessions_keys:
        return redirect("/")
    else:
        data = get_database.get_data()
        return json.dumps(data)

@app.route('/scanner_result', method=['GET', 'POST'])
def web_scan_result_page():
    # check if user is authenticated
    session_token = request.get_cookie("session_token")
    if not session_token or session_token != sessions_keys:
        return redirect("/")
    else:
        if request.method == 'GET':
            return template('webpage/scanner_result')
        if request.method == 'POST':
            cur.execute("DELETE FROM nmap_services_version")
            conn.commit()
            cur.execute("DELETE FROM sqlite_sequence WHERE name IN ('nmap_services_version')")
            conn.commit()
            ip = request.forms.get('ip') 
            scan_id = request.forms.get('scan_id')
            port = request.forms.get('port')
            cmd = "sudo python nmap_services_version.py " + str(ip) + " " + str(scan_id) + " " + str(port)
            subprocess.Popen(cmd, shell=True)
            redirect('services_version_result')
        

@app.get('/services_version_result', method=['GET', 'POST'])
def web_progress_page():
    # check if user is authenticated
    session_token = request.get_cookie("session_token")
    if not session_token or session_token != sessions_keys:
        return redirect("/")
    else:
        if request.method == 'GET':
            return template('webpage/services_version_result')
        if request.method == 'POST':
            cur.execute("DELETE FROM nmap_scripts")
            conn.commit()
            cur.execute("DELETE FROM sqlite_sequence WHERE name IN ('nmap_scripts')")
            conn.commit()
            scan_id = request.forms.get('scan_id')
            script = request.forms.get('script')
            ip_address = request.forms.get('ip_address')
            port = request.forms.get('port')        
            cmd = "sudo python nmap_script.py " + str(ip_address) + " " + str(scan_id) + " " + str(port) + " " + str(script)
            subprocess.Popen(cmd, shell=True)
            return redirect('script_result')

@app.get('/script_result', method=['GET', 'POST'])
def web_progress_page():
    # check if user is authenticated
    session_token = request.get_cookie("session_token")
    if not session_token or session_token != sessions_keys:
        return redirect("/")
    else:
        if request.method == 'GET':
            return template('webpage/script_result')

#@app.get('/report', method=['GET', 'POST'])
#def web_report_page():
#    if request.method == 'GET':
#        return template('webpage/report')

@app.get('/get_vendor')
def get_whitelist_data():
    # check if user is authenticated
    session_token = request.get_cookie("session_token")
    if not session_token or session_token != sessions_keys:
        return redirect("/")
    else:
        vendors = get_vendor.get_data()
        data = []
        for vendor, count in vendors:
            data.append({'vendor': vendor, 'count': count})
        return {'data': data}

@app.get('/get_family')
def get_whitelist_data():
    # check if user is authenticated
    session_token = request.get_cookie("session_token")
    if not session_token or session_token != sessions_keys:
        return redirect("/")
    else:
        familys = get_family.get_data()
        data = []
        for family, count in familys:
            data.append({'family': family, 'count': count})
        return {'data': data}

@app.get('/get_services_version')
def get_services_version():
    # check if user is authenticated
    session_token = request.get_cookie("session_token")
    if not session_token or session_token != sessions_keys:
        return redirect("/")
    else:
        services_versions = get_services_version_data.get_data()
        data = []
        for scan_id, ip, protocol_id, service_name, product, version, extrainfo, available_scripts, current_progress in services_versions:
            data.append({'scan_id': scan_id, 'ip': ip, 'protocol_id': protocol_id, 'service_name': service_name, 'product': product, 'version': version, 'extrainfo': extrainfo, 'available_scripts': available_scripts, 'current_progress': current_progress})
        return {'data': data}

@app.get('/get_script_data')
def get_whitelist_data():
    # check if user is authenticated
    session_token = request.get_cookie("session_token")
    if not session_token or session_token != sessions_keys:
        return redirect("/")
    else:
        script_datas = get_script_data.get_data()
        data = []
        for scan_id, host_ipv4, port, script_name, script_output, info_found in script_datas:
            data.append({'scan_id': scan_id, 'host_ipv4': host_ipv4, 'port': port, 'script_name': script_name, 'script_output': script_output, 'info_found': info_found})
        return {'data': data}

@app.get('/get_whitelist_summary')
def get_whitelist_data():
    # check if user is authenticated
    session_token = request.get_cookie("session_token")
    if not session_token or session_token != sessions_keys:
        return redirect("/")
    else:
        whitelist_summarys = get_whitelist_summary.get_data()
        data = []
        for whitelist, count in whitelist_summarys:
            data.append({'whitelist': whitelist, 'count': count})
        return {'data': data}

@app.get('/get_open_port')
def get_whitelist_data():
    # check if user is authenticated
    session_token = request.get_cookie("session_token")
    if not session_token or session_token != sessions_keys:
        return redirect("/")
    else:
        open_ports = get_open_port.get_data()
        data = []
        for open_port, count in open_ports:
            data.append({'open_port': open_port, 'count': count})
        return {'data': data}

@app.get('/get_whitelist')
def get_whitelist_data():
    # check if user is authenticated
    session_token = request.get_cookie("session_token")
    if not session_token or session_token != sessions_keys:
        return redirect("/")
    else:
        whitelists = get_whitelist.get_data()
        data = []
        for whitelist in whitelists:
            data.append({'mac_addr': whitelist[0], 'remark': whitelist[1]})
        return {'data': data}

@app.get('/whitelist', method=['GET', 'POST'])
def web_whitelist_page():
    # check if user is authenticated
    session_token = request.get_cookie("session_token")
    if not session_token or session_token != sessions_keys:
        return redirect("/")
    else:
        whitelists = get_whitelist.get_data()
        if request.method == 'GET':
            return template('webpage/whitelist')
        elif request.method == 'POST':
            if 'remove_mac_address' in request.POST:
                rm_mac_addr = request.forms.get('rm_mac_address')
                cmd = "sudo python remove_whitelist_db.py " + rm_mac_addr
                subprocess.Popen(cmd, shell=True)
                return template('webpage/whitelist')
            if 'remove_all_whitelist' in request.POST:
                cmd = "sudo python drop_whitelist.py"
                subprocess.Popen(cmd, shell=True)
                return template('webpage/whitelist')
            if 'btn_add1_mac_addr' in request.POST:
                mac_addr = request.forms.get('macaddress')
                remark = request.forms.get('remark')
                cmd = "sudo python add_whitelist_to_db.py " + mac_addr + " " + remark
                subprocess.Popen(cmd, shell=True)
                return template('webpage/whitelist')
            if 'btn_upload_mac_addr' in request.POST:
                file_obj = request.files.get('csv-file')
                file_content = file_obj.file.read()
                file_content = file_content.decode("utf-8")
                if file_content == "":
                    print('No file uploaded')
                    return template('webpage/whitelist')
                else:
                    file_like_obj = io.StringIO(file_content)
                    csv_reader = csv.reader(file_like_obj)
                    next(csv_reader)  # Skip the header row
                    for row in csv_reader:
                        mac_addr = row[0]
                        remark = row[1]
                        cmd = "sudo python add_whitelist_to_db.py " + mac_addr + " " + remark
                        subprocess.Popen(cmd, shell=True)    
                    return template('webpage/whitelist')
            return template('webpage/whitelist')
    

@app.get('/summary', method='GET')
def web_help_page():
    # check if user is authenticated
    session_token = request.get_cookie("session_token")
    if not session_token or session_token != sessions_keys:
        return redirect("/")
    else:
        if request.method == 'GET':
            return template('webpage/summary')

@app.get('/help', method='GET')
def web_help_page():
    # check if user is authenticated
    session_token = request.get_cookie("session_token")
    if not session_token or session_token != sessions_keys:
        return redirect("/")
    else:
        if request.method == 'GET':
            return template('webpage/help')

@app.get('/download_template', method=['GET', 'POST'])
def download_file():
    # check if user is authenticated
    session_token = request.get_cookie("session_token")
    if not session_token or session_token != sessions_keys:
        return redirect("/")
    else:
        if request.method == 'POST':
            if 'download_template' in request.POST:
                return static_file(filename='template.csv', root="./", download=True)
            else:
                return redirect('whitelist')
        elif request.method == 'GET':
            return redirect('whitelist')

@app.get('/download_whitelist', method=['GET', 'POST'])
def download_file():
    # check if user is authenticated
    session_token = request.get_cookie("session_token")
    if not session_token or session_token != sessions_keys:
        return redirect("/")
    else:
        if request.method == 'POST':
            if 'download_all_whitelist' in request.POST:
                cmd = "sudo python download_whitelist_csv.py"
                subprocess.run(cmd, shell=True)
                return static_file(filename='all_whitelist.csv', root="./download", download=True)
            else:
                return redirect('whitelist')
        elif request.method == 'GET':
            return redirect('whitelist')

@app.error(404)
def web_error404_page(error):
    return template('webpage/error')

if __name__ == '__main__':
    run(app, host='0.0.0.0', port=443, server='gunicorn', reloader=True, keyfile='SSL/localhost.key', certfile='SSL/localhost.crt')