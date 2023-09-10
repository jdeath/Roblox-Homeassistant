# Roblox-Homeassistant
Roblox Sensor For Homeassistant

Basically an editted version of the built-in steam-online integration, but works for roblox

**Breaking change:**
You must put 1x1.png in config/www/
You must add your homeassistant domain name in the config

Because it largely clones the steam-online integration, you can use the custom steam card lovelace card with it:
https://github.com/Kibibit/kb-steam-card

Setup:
Add this repo to HACS or copy "roblox" folder into /config/custom_components/ and restart homeassistant

In configuration.yaml, add an entry under sensors:

```
- platform: roblox
  api_key: '_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
  hassip: "homeassistant.example.com"
  accounts:
      - 'UserId1'
      - 'UserId2'
      - 'UserIdN'
 ```

hassip: should be replaced with your homeassistant domain name. This is so the webserver can provide an empty image when no game is being played. You must also put the 1x1.png if your config/www/ directory. I use a white 1x1.png, but you could find a transparent png or anything else you want.

UserIds are the roblox userids you want to track. On roblox.com, search for a user. Click on their profile web page, and the URL should be:
https://www.roblox.com/users/XXXXXXX/profile

XXXXXXX is their UserID. You can track as many as you want. 

The sensor will check each ID every 2 minutes. You can change line 41 and 42 of sensor.py to check quicker if you want (below is changed for .25 minutes):
```
BASE_INTERVAL = timedelta(minutes=.25)
SCAN_INTERVAL = timedelta(minutes=.25)
```
Note, an older version of the integration stepped the sensors at this rate. This new version updates every sensor at this rate.

api_key is tricky to get. It is a cookie from a logged in roblox account. Best to use a dummy account in case these credentials are stolen. Not sure how often you need to get a new cookie.

Chrome and the latest Edge
```
1. Click the arrow icon on the right-hand side of the toolbar. 
2. Go to More Tools. 
3. Click the Developer Tools button. 
4. Click the Application tab and Cookies button on the menu to the left. 
5. Click the dropdown until you find www.roblox.com. 
6. Your cookie is the value assigned to the key named .ROBLOSECURITY. Copy it into api_key:
```
Firefox
```
1. Click the hamburger icon on the right-hand side of the toolbar. 
2. Go to Web Developer. 
3. Click Storage Inspector and the Cookies button on the menu to the left. 
4. Click the dropdown until you find www.roblox.com. 
5. Your cookie is the value assigned to the key named .ROBLOSECURITY. Copy it api_key:
```
Safari
```
1. Go to Preferences, Advanced and select Show Develop menu in menu bar. 
2. Click the Develop tab. 
3. Click Show Web Inspector. 
4. Click the Storage tab and then click Cookies. 
5. Click the dropdown until you find www.roblox.com. 
6. Your cookie is the value assigned to the key named .ROBLOSECURITY. Copy it api_key:
```

Finanaly, create entries in lovelace:
```
type: entities
entities:
  - type: attribute
    entity: sensor.roblox_XXXXX
    attribute: game  
```    
or
```
type: custom:kb-steam-card
entities:
  - sensor.roblox_XXXX
  - sensor.roblox_YYYY
  - sensor.roblox_ZZZZ
```  
