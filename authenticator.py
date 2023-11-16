#!/usr/bin/env python

# Created by huydd79@gmail.com
# Using API to update GoDaddy DNS txt record for certbot validation
# Input:
#       - API key/secret from ini file
#       - Base domain from ini file
#       - Certbot domain and validation from environment variables
# Output:
#       - Write down subdomain file on success
#       - Show message on failure

import requests
import json
import os
import configparser
import time

config = configparser.ConfigParser()
config.read("/var/lib/letsencrypt/godaddy.ini")

key = config.get("setting","key")
secret = config.get("setting","secret")
domain = config.get("setting","domain")
certbot_domain = os.getenv('CERTBOT_DOMAIN')
validation = os.getenv('CERTBOT_VALIDATION')

# Domains are not matched
if (certbot_domain.find(domain) < 0):
    exit
# Certbot domain and primary domain are similar
if (certbot_domain.find(domain) == 0):
    sub_domain = "_acme-challenge"
# Certbot domain is sub domain
else:
    sub_domain = "_acme-challenge." + certbot_domain[:certbot_domain.find("." + domain)]

api_url = "https://api.godaddy.com/v1/domains/" + domain + "/records/TXT/" + sub_domain
payload = json.dumps([{"data": validation}])
headers = {'Authorization': 'sso-key ' + key + ':' + secret, 'Content-Type': 'application/json'}

print ("Sending request for DNS update: " + sub_domain + "." + domain + " <=> " + validation + "...")
response = requests.request("PUT", api_url, headers=headers, data=payload)
if (response.status_code==200):
    print ("200:OK")
    #Write down file for cleanup script
    f = open("/var/lib/letsencrypt/" + sub_domain, "w")
    f.write("\n" + sub_domain + " : " + domain + " : " + certbot_domain + " : " + validation + " : " + str(response.status_code) + " : " + response.text + "\n")
    f.close   
else:
    print (str(response.status_code) + ":" +response.text)

# Sleep to make sure the change has time to propagate over to DNS
time.sleep(30)
