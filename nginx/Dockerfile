FROM nginx:1.25
RUN apt-get update && apt-get install -y certbot python3-certbot-nginx
RUN rm /etc/nginx/conf.d/default.conf

# Set up non-SSL nginx conf first, because the SSL scripts
# need to be run on a container that the ark.frick.org domain is pointed at
COPY nginx.conf /etc/nginx/conf.d
COPY nginx.ssl.conf /nginx.ssl.conf

# Set up SSL
COPY ssl_setup.sh /ssl_setup.sh
RUN chmod +x /ssl_setup.sh
