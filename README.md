# Certbot.Docker+GoDaddy.DNS Wildcard Domain name #

##using manual-auth-hook script##

Recently certbot supports manual-auth-hook method that can call a script to update DNS' TXT record for dns authenticator. Detail of these method is explained [here](https://eff-certbot.readthedocs.io/en/stable/using.html#pre-and-post-validation-hooks)

Normaly the authenticator and cleanup script can easily use ```curl``` command to send the REST request to GoDaddy for DNS update/delete. However, for the default certbot docker image, the curl command is not available that make more difficult for the authenticator script to run.

This github project contains python scripts for authenticator and cleanup that can work with original certbot docker so that you will not need to rebuild or adding more component to the default image to make it work.

Comments and questions, please send to <huydd79@gmail.com>

# Usage
- Generating GoDaddy's api key/secret from https://developer.godaddy.com/keys
- Creating folder for certbot container running
  
```
mkdir -p /var/lib/letsencrypt
mkdir -p /etc/letsencrypt
```

- Copying godaddy.ini, authenticator.py and cleanup.py for ```/var/lib/letsencrypt```
- Updating godaddy.ini file with your domain, key and secret info
- Making sure your docker/podman machine can connect to GoDaddy's API url: https://api.godaddy.com/v1/domains
- Running below docker/podman command to execute certbot with test env and getting certificate with dns auto-authentication
```
podman run \
    --name certbot \
    -it --rm \
    -v "/etc/letsencrypt:/etc/letsencrypt" \
    -v "/var/lib/letsencrypt:/var/lib/letsencrypt" \
    certbot/certbot certonly \
    -v --agree-tos --agree-tos \
    --preferred-challenges dns \
    --manual \
    --manual-auth-hook /var/lib/letsencrypt/authenticator.py \
    --manual-cleanup-hook /var/lib/letsencrypt/cleanup.py \
    --server https://acme-v02.api.letsencrypt.org/directory \
    --email name@your.domain.com \
    --test-cert \
    -d *.your.domain.com
```
Remove ``` --test-cert``` to execute certbot and getting production certificates

#END#
