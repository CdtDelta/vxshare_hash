# This script is for pulling new hash files from vxshare.com
#
# Version 1.0
# By Tom Yarrish
#
# Modules required: requests, configobj
#
# Todo:
# - Add code to strip out first six lines of each file and replace with MD5 (for import in X-Ways Forensic)

from configobj import ConfigObj
import requests
import os

config_file = "/home/tom/tom@yarrish.com/Python/Projects/vx_share.cfg"

if os.path.exists(config_file):
    print "File exists"
    config = ConfigObj(config_file)
    vxshare_no = int(config['last_vxshare_num'])
else:
    print "File doesn't exist"
    config = ConfigObj()
    config.filename = config_file
    config['last_vxshare_num'] = 0
    vxshare_no = int(config['last_vxshare_num'])
    config.write()

vxshare_base_url = "http://virusshare.com/hashes/"
vxshare_file_name = "VirusShare_{:05d}.md5".format(vxshare_no)

vxshare_hash_url = vxshare_base_url + vxshare_file_name
file_is_valid = True

try:
    while file_is_valid == True:
        vxshare_file_name = "VirusShare_{:05d}.md5".format(vxshare_no)
        vxshare_hash_url = vxshare_base_url + vxshare_file_name
        vxshare_requests = requests.get(vxshare_hash_url)
        if vxshare_requests.status_code == 200:
            with open(vxshare_file_name, "w") as hash_file:
                print "Downloading {}...\n".format(vxshare_file_name)
                hash_file.write(vxshare_requests.content)
        else:
            file_is_valid = False
            config['last_vxshare_num'] = vxshare_no
            config.write()
        vxshare_no += 1
except Exception,e:
    print str(e)

print "All files parsed..." 