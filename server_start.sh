#!/bin/bash
cd /var/www/ZDIntegrationService
source /var/www/ZDIntegrationService/venv/bin/activate
pip install -r requirements.txt
/var/www/ZDIntegrationService/venv/bin/uvicorn main:app --host 0.0.0.0 --port 3000 >> /var/www/ZDIntegrationService/logs/errors.txt
