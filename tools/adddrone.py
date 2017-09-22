import requests
import pprint
import json
import csv
import copy
import base64
import sys
from LatLon23 import LatLon
import pdnsutils

headers = {
    'X-API-Key': 'PlE@seChAnG3MeT0Some+hingEl$e'
}
url = 'http://127.0.0.1:8081/api/v1/servers/localhost'
dnsprefix = "uas.directory."

#domain = str(sys.argv[1]) + "." + dnsprefix

s = requests.Session()
assert isinstance(s, object)
r = s.get(url + '/zones', headers=headers).json()
for each in r:
    if "uas.directory" in each["name"]:
        zonedict = each


myzone = pdnsutils.Zone()
contentdict = {}
contentdict["droneid"] = input('Drone ID:')
contentdict["droneowner"] = input('Drone Owner:')
contentdict["dronetype"] = input('airframe type:')
contentdict["dronepurpose"] = input('drone purpose:')
dronename = contentdict["droneid"] + "." + zonedict["name"]
#OK lets build the URI .place record
dronefence = "10 1 \"https://" + contentdict["droneid"] + "." + contentdict["droneowner"].replace(' ','-') + ".place\""
fence_record = pdnsutils.create_record(dronefence)
fence_rrset = pdnsutils.RRset("_http._tcp." + dronename,"URI")
fence_rrset.add_record(fence_record)
myzone.add_rrset(fence_rrset.get())
#OK lets add the rdap refereall
dronerdap = "10 1 \"https://rdap." + zonedict["name"] + "\""
rdap_record = pdnsutils.create_record(dronerdap)
rdap_rrset = pdnsutils.RRset("_rdap._tcp." + dronename,"URI")
rdap_rrset.add_record(rdap_record)
myzone.add_rrset(rdap_rrset.get())
#OK lets do the Json structure in the text record
contentstring = json.dumps(contentdict)
text_record = pdnsutils.create_record('"' + base64.b64encode(contentstring.encode()).decode() + '"')
text_rrset = pdnsutils.RRset(dronename,"TXT")
text_rrset.add_record(text_record)
myzone.add_rrset(text_rrset.get())
pprint.pprint(myzone.get())
update_result = s.patch(url=url + '/zones/' + zonedict["name"], data=myzone.get_json(), headers=headers)
print(update_result.status_code)
print(update_result.text)

