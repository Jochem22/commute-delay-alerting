# Commute Delay Alerting

This scripts monitors your commute set in config.yaml and sends alerts when there is a delay found on your
route. Alert is send once at start of delay and a final alert is send when delay is cleared. The Telegram API is used to 
send the alerts. Waze API is used to calculate delays on the specified route. I use this script to leave early when first 
delay alert is received or leave when all alerts are cleared to avoid traffic jams on my route. This keeps me from 
checking Waze or Google Maps for traffic jams manually.

![image](https://user-images.githubusercontent.com/25078202/222752347-b17420af-39b6-4843-9468-a9c8cc6f7d8f.png)


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/)

```bash
pip install -r requirements.txt
```

## Requirements

- .env file with telegram API token and chat_id 
  - copy env_example to .env
  - [generate-telegram-token-for-bot-api](https://medium.com/geekculture/generate-telegram-token-for-bot-api-d26faf9bf064)
- coordinates (lat,lon) of origin and destination
  - Open https://www.google.com/maps
  - Right-click on place or area on map
  - Left-click coordinates from pop-up window
- distance of routes
  - Open https://www.waze.com/live-map/
  - Add starting point and destination using the coordinates from Google Maps
    - starting point  'lat=xx.xxxxxxxxxxxxxx lng=x.xxxxxxxxxxxxxx'
    - destination 'lat=xx.xxxxxxxxxxxxxx lng=x.xxxxxxxxxxxxxx'
  - Copy distance of route you want to monitor
- config.yaml
  - copy and rename config_example.yaml to config.yaml
  
## Usage

Add your routes in config.yaml and run main.py to start monitoring for delays for your commute.

## NOTE

Waze returns multiple routes when alternative routes are available. Distance from config file needs to match one of
these routes. This will be the main route to monitor for delays. If no routes match, check the log file for all routes 
Waze API returns, choose your main route and copy correct distance to config.
