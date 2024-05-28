# list-users.py
# created May 28, 2024
# creates a csv with members of a group and some membership details

import os
from arcgis import GIS
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()
OUTPUT_FILE = 'list.csv'
MHUSER = os.getenv('MHUSER')
MHPASS = os.getenv('MHPASS')
GROUPNAME = os.getenv('MHGROUP')

mh = GIS(username=MHUSER,password=MHPASS)
data = []
header = ['user','fullname','lastlogin','email']
# get group users and user info
for g in mh.groups.search(GROUPNAME):
    members = g.get_members()
    for m in members['users']:
        user = mh.users.get(m)
        lastlogin = datetime.fromtimestamp(user.lastLogin/1000.0).strftime("%Y-%m-%d")
        r = [m,user.fullName,lastlogin,user.email]
        data.append(','.join(r)+'\n')

# write to file
with open(OUTPUT_FILE,'w') as f:
    f.write(','.join(header))
    f.write('\n')
    f.writelines(data)


