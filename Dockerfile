FROM debian:12

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
    chromium \
    chromium-driver \
    libnss3 \
    libgtk-3-0 \
    libxkbcommon0 \
    libgbm1 \
    libxdamage1 \
    libxrandr2 \
    libxcomposite1 \
    fonts-liberation \
    ca-certificates \
    python3-pip \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# --------------------------------------------------
# Clone your repo
# --------------------------------------------------
WORKDIR /opt
RUN git clone -b arm https://github.com/brun100gr/getNextArcaplanetPrice.git

# --------------------------------------------------
# Copy local folder to container (for development purposes)
# --------------------------------------------------
#WORKDIR /opt/getNextArcaplanetPrice
#COPY . .

# --------------------------------------------------
# Python virtual environment
# --------------------------------------------------
WORKDIR /opt/getNextArcaplanetPrice
RUN pip3 install --break-system-packages --upgrade pip
RUN pip3 install --break-system-packages -r requirements.txt

# --------------------------------------------------
# Default command
# --------------------------------------------------
CMD ["python3", "getPrice.py"]

