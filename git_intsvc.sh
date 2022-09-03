#!/bin/bash
cd /var/www/ZDIntegrationService
sudo git pull
sudo chown -R www-data:www-data /var/www/ZDIntegrationService/
sudo systemctl stop intservice
sudo systemctl start intservice
sudo systemctl restart nginx
