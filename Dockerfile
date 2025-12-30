FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Rome

# --------------------------------------------------
# Base system update
# --------------------------------------------------
RUN apt update && apt dist-upgrade -y

# --------------------------------------------------
# Install required packages
# --------------------------------------------------
RUN apt update && apt install -y \
    git \
    openssh-server \
    python3 \
    python3-pip \
    wget \
    gnupg \
    unzip \
    libnss3 \
    libgconf-2-4 \
    libxss1 \
    libappindicator3-1 \
    libasound2 \
    fonts-liberation \
    xdg-utils \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# --------------------------------------------------
# Install Google Chrome
# --------------------------------------------------
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub \
    | gpg --dearmor -o /usr/share/keyrings/google-linux-keyring.gpg

RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-keyring.gpg] \
    http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google-chrome.list

RUN apt update && apt install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# --------------------------------------------------
# Install chromedriver (Chrome for Testing - correct way)
# --------------------------------------------------
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') && \
    MAJOR_VERSION=$(echo $CHROME_VERSION | cut -d. -f1) && \
    wget -q "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip" && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver && \
    rm -rf chromedriver-linux64 chromedriver-linux64.zip

# --------------------------------------------------
# SSH setup
# --------------------------------------------------
RUN mkdir /var/run/sshd
RUN echo 'root:root' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

EXPOSE 22

# --------------------------------------------------
# Clone your repo
# --------------------------------------------------
WORKDIR /opt
RUN git clone https://github.com/brun100gr/getNextArcaplanetPrice.git

# --------------------------------------------------
# Python virtual environment
# --------------------------------------------------
WORKDIR /opt/getNextArcaplanetPrice
RUN /usr/bin/pip3 install --upgrade pip
RUN /usr/bin/pip3 install -r requirements.txt

# --------------------------------------------------
# Start SSH
# --------------------------------------------------
COPY start.sh /start.sh
RUN chmod +x /start.sh

#CMD ["/start.sh"]

CMD ["python3", "getPrice.py"]

