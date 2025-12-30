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
RUN apt install -y \
    git \
    openssh-server \
    python3 \
    python3-pip \
    chromium-browser \
    chromium-chromedriver \
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
#RUN python3 -m venv myenv
RUN /usr/bin/pip3 install --upgrade pip
RUN /usr/bin/pip3 install -r requirements.txt

# --------------------------------------------------
# Start SSH
# --------------------------------------------------
COPY start.sh /start.sh
RUN chmod +x /start.sh

#CMD ["/start.sh"]

CMD ["python3", "arcaplanet.py"]

