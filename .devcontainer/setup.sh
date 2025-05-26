#!/bin/bash
set -e

echo "Installing custom tools and packages..."

# Update and install system packages
sudo apt-get update
sudo apt-get install -y \
    curl \
    git 
    
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
# Clean up
rm awscliv2.zip
rm -rf aws



echo "Setup complete."
