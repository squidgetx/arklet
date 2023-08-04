#!/bin/bash

DOMAINS="ark.frick.org minter.ark.frick.org"
NGINX_RELOAD_CMD="nginx -s reload"
EMAIL=saz310@nyu.edu

certbot certonly --non-interactive --nginx --agree-tos --email $EMAIL --domains $DOMAINS

# Check if certbot command was successful (exit code 0) and reload Nginx
if [ $? -eq 0 ]; then
    $NGINX_RELOAD_CMD
fi
