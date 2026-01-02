# getNextArcaplanetPrice
This script automatically sends the price of Next cat food cans from the ArcaPlanet online store to a Telegram bot.

## Environment setup
Download GitHub repository
```
git clone https://github.com/brun100gr/getNextArcaplanetPrice.git

```

## Docker
Create container
```
docker build -t arcaplanet-bot .
```
Start container
```
docker run --rm --env-file .env arcaplanet-bot
```

## .env file
.env contains
```
APPS_SCRIPT_URL=https://script.google.com/macros/s/.../exec
TELEGRAM_TOKEN=123456789:AAAbbbCCCdddEEEfff
TELEGRAM_CHAT_ID=1234567890
```

## Get chat ID
```
https://api.telegram.org/bot<TOKEN>/getUpdates
```
