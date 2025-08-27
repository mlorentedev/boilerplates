#!/bin/bash
set -e

# Update system
apt-get update
apt-get upgrade -y

# Install basic packages
apt-get install -y \
    curl \
    wget \
    unzip \
    git \
    htop \
    nginx \
    ufw

# Configure firewall
ufw allow ssh
ufw allow http
ufw allow https
ufw --force enable

# Configure nginx
systemctl enable nginx
systemctl start nginx

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Clean up
rm -f get-docker.sh

echo "Droplet initialization completed" | tee /var/log/cloud-init-output.log