"""Sensor for roblox account status."""
from datetime import timedelta
import logging
import requests

from time import mktime

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_API_KEY
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import track_time_interval
from homeassistant.util.dt import utc_from_timestamp

import json
import asyncio
from aiohttp import ClientError, ClientResponseError
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

CONF_ACCOUNTS = "accounts"
CONF_HASSIP = "hassip"

ICON = "mdi:robot-outline"

roblox_cookie = ""

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_API_KEY): cv.string,
        vol.Required(CONF_ACCOUNTS, default=[]): vol.All(cv.ensure_list, [cv.string]),
        vol.Required(CONF_HASSIP): cv.string,
    }
)


BASE_INTERVAL = timedelta(minutes=2)
SCAN_INTERVAL = timedelta(minutes=2)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the roblox platform."""

    roblox_cookie = config.get(CONF_API_KEY)
    ip_address = config.get(CONF_HASSIP)
    # Initialize robloxmods app list before creating sensors
    # to benefit from internal caching of the list.

    entities = [
        robloxSensor(hass,account, ip_address,roblox_cookie) for account in config.get(CONF_ACCOUNTS)
    ]
    if not entities:
        return
        
    async_add_entities(entities, True)


class robloxSensor(Entity):
    """A class for the roblox account."""

    def __init__(self, hass, account,ip_address, robloxod):
        """Initialize the sensor."""
        self._robloxod = robloxod
        self._account = account
        self._profile = None
        self._game = None
        self._game_id = None
        self._extra_game_info = None
        self._state = None
        self._name = None
        self._avatar = None
        self._last_online = None
        self._level = None
        self._owned_games = None
        self._gameurl = None
        self._game_image_header = None
        self._game_image_main = None
        self._placeId = None
        self._universeId = None
        self._ip_address = ip_address
        self.hass = hass
        
    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def entity_id(self):
        """Return the entity ID."""
        return f"sensor.roblox_{self._account}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def should_poll(self):
        """Turn off polling, will do ourselves."""
        return True

    async def async_update(self):
        """Update device state."""
        
        
        try:        
            session = async_get_clientsession(self.hass)
        
            resp = await session.get("https://users.roblox.com/v1/users/" + self._account)
            data = await resp.json()
            self._name = data["displayName"]
           
            
            #self._avatar = data["AvatarUri"]
            
            # Get Headshot
            headers = {
                'accept': 'application/json',
            }

            params = {
                'userIds': self._account,
                'size': '48x48',
                'format': 'Png',
                'isCircular': 'false',
            }
            
            resp = await session.get('https://thumbnails.roblox.com/v1/users/avatar-headshot', params=params, headers=headers)
            data = await resp.json()
            self._avatar = data.get('data')[0].get('imageUrl')
            
            # Get Presence
            cookies_dict = {".ROBLOSECURITY": self._robloxod}
            headers = {
                "accept": "application/json",
                "Content-Type": "application/json",
            }

            json_data = {
                "userIds": [
                    self._account,
                ],
            }
            
            resp = await session.post(
                "https://presence.roblox.com/v1/presence/users",
                headers=headers,
                json=json_data,
                cookies=cookies_dict,
            )
            data = await resp.json()
            
            userPresence = data.get("userPresences")[0]
            self._game_id = userPresence.get("gameId")
            
            self._last_online = userPresence.get("lastOnline")
            self._placeId = userPresence.get("placeId")
            self._game = userPresence.get("lastLocation")
            self._universeId = userPresence.get("universeId")
            
            isOnline = int(userPresence.get("userPresenceType")) > 0
            if isOnline:
                self._state = "online"    
            else:
                self._state = "offline"
                self._game = "offline"
            
            if self._universeId is not None:
                resp = await session.get('https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds=' + str(self._universeId) + '&countPerUniverse=1&defaults=true&size=768x432&format=Png&isCircular=false')
                data = await resp.json()
                
                self._game_image_header = data['data'][0]['thumbnails'][0]['imageUrl']
                self._game_image_main = data['data'][0]['thumbnails'][0]['imageUrl']
                # self._gameurl = 'https://www.roblox.com/games/' + str(placeId)
        except:
            self._game = None
            self._game_id = None
            self._state = None
            self._name = None
            self._avatar = None
            self._last_online = None
            self._level = None
            self._game_image_header = None
            self._game_image_main = None
            self._gameurl = None
            self._placeId = None
            self._universeId = None

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attr = {}
        if self._game is not None:
            attr["game"] = self._game
        if self._game_id is not None:
            attr["game_id"] = self._game_id
            attr["place_id"] = self._placeId
            attr["universe_id"] = self._universeId
            # game_url = f"{roblox_API_URL}{self._game_id}/"
            attr["game_image_header"] = self._game_image_header
            attr["game_image_main"] = self._game_image_main
        else:
            attr["game_image_header"] = "https://" + self._ip_address + "/local/1x1.png"
            attr["game_image_main"] = "https://" + self._ip_address + "/local/1x1.png"
            
        if self._last_online is not None:
            attr["last_online"] = self._last_online

        return attr

    @property
    def entity_picture(self):
        """Avatar of the account."""
        return self._avatar

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return ICON
