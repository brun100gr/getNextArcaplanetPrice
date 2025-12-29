# getNextArcaplanetPrice
Script to get price of cat food

## Environment setup
```
sudo apt update
sudo apt install -y \
  google-chrome-stable \
  chromium-chromedriver \
  libnss3 \
  libgconf-2-4 \
  libxss1 \
  libappindicator3-1 \
  libasound2 \
  fonts-liberation \
  xdg-utils \
  python3-venv

git clone https://github.com/brun100gr/getNextArcaplanetPrice.git

python3 -m venv myenv
source myenv/bin/activate
pip3 install -r requirements.txt

google-chrome --version
chromedriver --version


python3 - <<EOF
from selenium import webdriver
from bs4 import BeautifulSoup
print("OK")
EOF

```

