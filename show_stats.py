# script to check iops from ScaleIO
# next up plot iops using matplot animation option

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

# import requests for our RESTfull calls
import requests
import base64
import json

gateway = 'sio01.t-i.demo'
sdc = '10.160.35.157'
volume = {'name':'testvol'}

# build uri of gateway to login to
uri = 'https://%s/api/login' % gateway

# request session_id. We know it's json result
response = requests.get(uri,auth=('admin','password'),verify=False)
session_id = response.json()

# now create new header(dict), we need to create basic authentication header
# Authorization has no name but we need to add : and b64encode the session_id
auth = ":" + session_id
auth = base64.b64encode(auth)
auth = "Basic " + auth
headers = {'Authorization' : auth,
           'Content-Type' : 'application/json'
    }

# now we need to lookup the id of the volume using following url
# headers can be dictionary, data should be json format.
uri = 'https://%s/api/types/Volume/instances/action/queryIdByKey' % gateway
response = requests.post(uri,data=json.dumps(volume),headers=headers,verify=False)

# statistics for a volume can be found at:
# volume stats: /api/instances/Volume::f262f2b900000000/relationships/Statistics
uri = 'https://%s/api/instances/Volume::%s/relationships/Statistics' % (gateway,response.json())
response = requests.get(uri,headers=headers,verify=False)

# create dictionary with stats from volume
# we're only interested in read/write IOPS.
stats = response.json()
writeIOPS = stats['userDataWriteBwc']['numOccured']
readIOPS = stats['userDataReadBwc']['numOccured']
totalIOPS = writeIOPS + readIOPS

print "%d:%d:%d" % (totalIOPS,readIOPS,writeIOPS)