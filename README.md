# Commute Delay Alerting

This scripts monitors your commute and sends alerts when there is a delay found on your route. Alert is send once at 
start of delay and a final alert is send when delay is cleared. The Telegram API is used to send the alerts. Waze API is 
used to calculate delays on the specified routes. This project is mainly used for learning purposes. 


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
  
## Usage

When you use this tool for the first time run db.py to create a database with sample configuration. Then run 
check_routes.py to fill the database with route data every 5 minutes. Finally run app.py to view the data and edit the 
configuration from your browser. You need to restart check_routes.py everytime you make changes to the configuration.

## NOTE

Waze returns multiple routes when alternative routes are available. Distance from config needs to match one of
these routes. This will be the main route to monitor for delays. If no routes match, check the log file for all routes 
Waze API returns, choose your main route and copy correct distance to config.
