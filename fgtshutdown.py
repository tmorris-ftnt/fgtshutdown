import requests, sys, json
requests.packages.urllib3.disable_warnings()

try:
    fgtip = sys.argv[1]
    fgtapikey = sys.argv[2]
except:
    print("Usage: fgtshutdown.exe <fgthost> <apitoken>")
    sys.exit()


session = requests.session()
headers = {"Authorization": "Bearer " + fgtapikey}


url = 'https://' + fgtip + '/api/v2/cmdb/system/global/?format=hostname'
try:
    res = session.get(url, headers=headers, verify=False, timeout=4)
except requests.exceptions.RequestException:
    print("Could not connect to FortiGate at https://" + fgtip)
    sys.exit()

if res.status_code != 200:
    print("Could not get FortiGate Info. API key could be invalid or not have permission.")

firewallinfo = json.loads(res.text)

print("FortiGate Info:")
print("Hostname: " + firewallinfo['results']['hostname'])
print("Serial No: " + firewallinfo['serial'])
print("")

while True:
    confirm = input("Confirm Shutdown (Yes/No):")
    if confirm == "Yes" or confirm == "YES" or confirm == "yes":
        url = 'https://' + fgtip + '/api/v2/monitor/system/os/shutdown'
        data = {"event_log_message": "Shutdown by fgtshutdown script"}
        res = session.post(url, data=data, headers=headers, verify=False)
        if res.status_code == 200:
            print("FortiGate is shutting down ...")
        else:
            print("Failed to shutdown FortiGate (check API user has permission ...")
        sys.exit()
    elif confirm == "No" or confirm == "no" or confirm == "NO":
        print("Quitting")
        sys.exit()

