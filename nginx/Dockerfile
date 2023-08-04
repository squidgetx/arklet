FROM nginx:1.25

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

# Install required packages for Certbot
RUN apt-get update && apt-get install -y certbot python3-certbot-nginx && rm -rf /var/lib/apt/lists/*

# Copy the script to obtain and renew Let's Encrypt certificates
COPY certbot_renew.sh /usr/local/bin/certbot_renew.sh
RUN chmod +x /usr/local/bin/certbot_renew.sh

# Add cron job to renew certificates automatically (runs every day at 2:30 am)
RUN echo "30 2 * * * root /usr/local/bin/certbot_renew.sh" > /etc/cron.d/certbot_renew


# Start Nginx and the cron service
CMD ["sh", "-c", "cron && nginx -g 'daemon off;'"]
