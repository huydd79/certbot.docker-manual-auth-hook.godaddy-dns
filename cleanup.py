#!/usr/bin/env python

# Created by huydd79@gmail.com
# Using API to delete GoDaddy DNS txt record for certbot clean up
# Input:
#       - API key/secret from ini file
#       - Base domain from ini file
#       - Subdomain file existed as cleanup request
# Output:
#       - Write down subdomain file on success
#       - Show message on failure

import requests
import os
import configparser


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
payload = ""
headers = {'Authorization': 'sso-key ' + key + ':' + secret, 'Content-Type': 'application/json'}

fname = "/var/lib/letsencrypt/" + sub_domain
if (os.path.isfile(fname)):
    print ("Cleaning up TXT arecord for " + sub_domain + "...")
    response = requests.request("DELETE", api_url, headers=headers, data=payload)
    if (response.status_code==200):
        print ("200:OK")
    else:
        print (str(response.status_code) + ":" +response.text)
    os.remove(fname)
else:
    print ("Sub domain " + sub_domain + " is not existed. Nothing to clean.")
