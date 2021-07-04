# Roblox-Homeassistant
Roblox Sensor For Homeassistant
Basically an editted version of the built-in steam-online integration

Setup:
In configuration.yaml add under sensors:

```
- platform: roblox_online
    api_key: '_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    accounts:
      - 'UserId1'
      - 'UserId2'
      - 'UserId3'
 ```
Where the api_key is a cookie from a logged in roblox account. This is a little tricky to get:
 Chrome
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
