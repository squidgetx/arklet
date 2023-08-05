#!/bin/bash

DOMAIN_FLAGS="-d ark.frick.org"
EMAIL=saz310@nyu.edu

certbot certonly --non-interactive --nginx --agree-tos --email $EMAIL $DOMAIN_FLAGS

