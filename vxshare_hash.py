# This script is for pulling new hash files from vxshare.com
#
# Version 1.1
# By Tom Yarrish
#
# Modules required: requests, configobj
#
# 3/21/15 - Added import sys which apparently disappeared when I was working on the code


from configobj import ConfigObj
import requests
import os
import sys

def reconfig_hash_file(hash_file):
    with open(hash_file, "r") as hash_file_to_process:
        new_hash_file = hash_file_to_process.readlines()
        bkup_hash_file = new_hash_file[6:]    
    with open(hash_file, "w") as new_hash_file:
        bkup_hash_file.insert(0, "MD5\n")
        new_hash_file.writelines(bkup_hash_file)

config_file = sys.argv[1]

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
                reconfig_hash_file(vxshare_file_name)
        else:
            file_is_valid = False
            config['last_vxshare_num'] = vxshare_no
            config.write()
        vxshare_no += 1
except Exception,e:
    print str(e)

print "All files parsed..." 