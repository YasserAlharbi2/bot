#!/bin/bash

apt-get update && apt-get install -y chromium
which chromium
which chromium-browser
which google-chrome

pip install -r requirements.txt
