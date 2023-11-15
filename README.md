# Letsencrypt Certbot Docker and GoDaddy DNS using manual-auth-hook script
Recently certbot supports manual-auth-hook method that can call a script to update DNS' TXT record for dns authenticator. Detail of these method is explained https://eff-certbot.readthedocs.io/en/stable/using.html#pre-and-post-validation-hooks
Normaly the authenticator and cleanup script can easily use ```curl``` command to send the REST request to GoDaddy for DNS update/delete. However, for certbot docker, the curl command is not available 
Manual auth hook python script using with certbot docker working with GoDaddy DNS provider


mkdir -p /huydd/certbot/test/data/vat/lib/letsencrypt
mkdir -p /huydd/certbot/test/data/log
mkdir -p /huydd/certbot/test/data/etc/letsencrypt
