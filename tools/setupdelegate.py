import base64
import copy
import csv
import json
import pprint
import sys

import ipaddress
import requests
import pdnsutils
import signdelegate

headers = {
    'X-API-Key': 'PlE@seChAnG3MeT0Some+hingEl$e'
}
url = 'http://127.0.0.1:8081/api/v1/servers/localhost'
dnsprefix = "uas.directory."
SOAvalues = " 1 86400 7200 3600000 60"

s = requests.Session()
assert isinstance(s, object)
r = s.get(url + '/zones', headers=headers).json()
pprint.pprint(r)

ISOcode = input('Numeric ISO code: ')
zonename = str(ISOcode).zfill(3) + "." + dnsprefix
newzone = pdnsutils.NewZone(zonename)
SOARRset = pdnsutils.RRset(zonename,"SOA")
nameserver1 = "ns1." + zonename
nameserver2 = "ns2." + zonename
authemailin = input('Contact email for domain: ')
authemail = authemailin.replace('@', '.') + "."
SOAvalues = nameserver1 + " " + authemail + SOAvalues
SOArecord = pdnsutils.create_record(SOAvalues)
SOARRset.add_record(SOArecord)
newzone.add_rrset(SOARRset.get())

nameserverIP1string = input('First Nameserver ip address: ')
assert isinstance(nameserverIP1string, object)
if nameserverIP1string:
    try:
        nameserverIP1 = ipaddress.ip_address(nameserverIP1string)
        newzone.add_nameserver(nameserver1,nameserverIP1string)
    except ValueError:
        print("Not a valid IP address")
        raise
nameserver1_record = pdnsutils.create_record(nameserverIP1string, nameserver1, "A")
assert isinstance(nameserver1_record, object)
nameserverIP2string = input('Second Nameserver ip address (hit enter if none):')
assert isinstance(nameserverIP2string, object)
if nameserverIP2string:
    try:
        nameserverIP2 = ipaddress.ip_address(nameserverIP2string)
        newzone.add_nameserver(nameserver1,nameserverIP1string)
    except ValueError:
        print("Not a valid IP address")
        raise

print("automatically generated nameserver name(s):")
print("first nameserver = " + nameserver1)
if nameserverIP2string:
    print("second nameserver = " + nameserver2)

pprint.pprint(newzone.get())
update_result = s.post(url=url + "/zones", data=newzone.get_json(), headers=headers)
print("post done")
assert isinstance(update_result.status_code, object)
print(update_result.status_code)
print(update_result.text)

if update_result:
    pprint.pprint(update_result.text)

signdelegate.sign_zone(zonename)

