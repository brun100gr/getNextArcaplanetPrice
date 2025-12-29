# getNextArcaplanetPrice
Script to get price of cat food

## Environment setup
```
git clone https://github.com/brun100gr/getNextArcaplanetPrice.git

sudo apt update
sudo apt dist-upgrade -y
sudo apt install -y \
  chromium-browser \
  chromium-chromedriver \
  libnss3 \
  libgconf-2-4 \
  libxss1 \
  libappindicator3-1 \
  libasound2 \
  fonts-liberation \
  xdg-utils \
  python3-venv

cd getNextArcaplanetPrice
python3 -m venv myenv
source myenv/bin/activate
pip3 install -r requirements.txt

sudo timedatectl set-timezone Europe/Rome
```

## Environment check
```
chromedriver --version

python3 - <<EOF
from selenium import webdriver
from bs4 import BeautifulSoup
print("OK")
EOF

date
```
