import json
import pprint


class Zone:
    def __init__(self):
        self.rrsetsArray = []
        self.zonedict = {}
        self.zonedict["rrsets"] = self.rrsetsArray

    def add_rrset(self, newset):
        self.zonedict["rrsets"].append(newset)

    def get(self):
        return self.zonedict

    def get_json(self):
        return json.dumps(self.zonedict)


class NewZone(Zone):
    def __init__(self, name):
        Zone.__init__(self)
        self.nameserversArray = []
        self.mastersArray = []
        self.zonedict["nameservers"] = self.nameserversArray
        self.zonedict["kind"] = "Native"
        self.zonedict["name"] = name
        self.zonedict["masters"] = self.mastersArray

    def add_nameserver(self, newnameserver, address):
        self.zonedict["nameservers"].append(newnameserver)
        self.myrrset = RRset(newnameserver, "A")
        self.myrecord = create_record(address)
        self.myrrset.add_record(self.myrecord)
        self.add_rrset(self.myrrset.get())


class RRset:
    def __init__(self, name, dnstype, ttl=3600, changetype="REPLACE"):
        self.rrsetdict = {}
        self.recordArray = []
        self.commentArray = []
        self.rrsetdict["name"] = name
        self.rrsetdict["type"] = dnstype
        self.rrsetdict["ttl"] = ttl
        self.rrsetdict["changetype"] = changetype
        self.rrsetdict["records"] = self.recordArray
        self.rrsetdict["comments"] = self.commentArray

    def get(self):
        r = dict(self.rrsetdict)
        if self.rrsetdict["changetype"] == "DELETE":
            del r["ttl"]
        return r

    def get_json(self):
        return json.dumps(self.get())

    def add_record(self, newrecord):
        self.rrsetdict["records"].append(newrecord)

    def add_comment(self, newcomment):
        self.rrsetdict["comments"].append(newcomment)


def create_record(content, disabled=False, setptr=False):
 #   record_dict = {"content": content, "disabled": disabled, "set-ptr": setptr}
    record_dict = {"content": content, "disabled": disabled}
    return record_dict


def create_comment(content, account=""):
    comment_dict = {"content": content, "account": account}
    return comment_dict
