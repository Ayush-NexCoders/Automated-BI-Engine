#!/bin/bash
# Script to install Docker and Docker Compose on an Ubuntu VPS, and start n8n.

echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

echo "Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

echo "Adding user to docker group..."
sudo usermod -aG docker $USER

echo "Installing Docker Compose plugin..."
sudo apt-get install docker-compose-plugin -y

echo "Starting n8n via Docker Compose..."
# Assuming docker-compose.yml is in the same directory as this script
docker compose up -d

echo "n8n has been started!"
echo "Please verify by accessing http://<your-vps-ip>:5678"
