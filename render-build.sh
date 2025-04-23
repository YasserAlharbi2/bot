#!/usr/bin/env bash
# تثبيت Chromium
apt-get update
apt-get install -y chromium

# تستكمل بعدها تثبيت باقي المتطلبات
pip install -r requirements.txt
