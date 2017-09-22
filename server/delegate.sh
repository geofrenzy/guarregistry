#!/bin/bash
pdnsdatabase="/data/powerdns.sqlite3"
if [ -f "$pdnsdatabase" ] 
then
  echo $pdnsdatabase "already exists: not copied"
else
  cp -v /tmp/powerdns.sqlite3 $pdnsdatabase
  echo "copied database template to /data"
fi
chmod 774 $pdnsdatabase
chgrp pdns $pdnsdatabase
chmod 774 /data
chgrp pdns /data
ls -al /data
ls -al $pdnsdatabase
diff -s /tmp/powerdns.sqlite3 $pdnsdatabase
/usr/sbin/pdns_server 


