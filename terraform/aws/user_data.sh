#!/bin/bash
set -e

# Update system
apt-get update
apt-get upgrade -y

# Set hostname
hostnamectl set-hostname ${hostname}
echo "127.0.1.1 ${hostname}" >> /etc/hosts

# Install basic packages
apt-get install -y \
    curl \
    wget \
    unzip \
    git \
    htop \
    nginx \
    certbot \
    python3-certbot-nginx

# Configure nginx
systemctl enable nginx
systemctl start nginx

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
usermod -aG docker ubuntu

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Clean up
rm -f get-docker.sh

echo "User data script completed successfully" | tee /var/log/user-data.log