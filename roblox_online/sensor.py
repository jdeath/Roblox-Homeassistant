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

_LOGGER = logging.getLogger(__name__)

CONF_ACCOUNTS = "accounts"

ICON = "mdi:robot-outline"

roblox_cookie = ""

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_API_KEY): cv.string,
        vol.Required(CONF_ACCOUNTS, default=[]): vol.All(cv.ensure_list, [cv.string]),
    }
)


BASE_INTERVAL = timedelta(minutes=1)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the roblox platform."""

    roblox_cookie = config.get(CONF_API_KEY)
    # Initialize robloxmods app list before creating sensors
    # to benefit from internal caching of the list.
    
    entities = [robloxSensor(account, roblox_cookie) for account in config.get(CONF_ACCOUNTS)]
    if not entities:
        return
    add_entities(entities, True)

    # Only one sensor update once every 60 seconds to avoid
    # flooding roblox and getting disconnected.
    entity_next = 0

    @callback
    def do_update(time):
        nonlocal entity_next
        entities[entity_next].async_schedule_update_ha_state(True)
        entity_next = (entity_next + 1) % len(entities)

    track_time_interval(hass, do_update, BASE_INTERVAL)


class robloxSensor(Entity):
    """A class for the roblox account."""

    def __init__(self, account, robloxod):
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
        return False
        
    def update(self):
        """Update device state."""
        try:
            r = requests.get('https://www.roblox.com/profile?userId=' + self._account)
            data = r.json();
                     
            self._name = data['Username']
            self._avatar = data['AvatarUri']
               
            cookies_dict = {".ROBLOSECURITY": self._robloxod}
            
            r = requests.get('http://api.roblox.com/users/' + self._account + '/onlinestatus',cookies=cookies_dict)
            data = r.json();
           
            self._game = data['LastLocation']
            self._game_id = data['GameId']
            if data['IsOnline']:
                self._state = 'online'
            else:
                self._state = 'offline'
            
            
            self._last_online = data['LastOnline']
            placeId = data['PlaceId']
            self._placeId = placeId
            if placeId is not None:
                r = requests.get('https://thumbnails.roblox.com/v1/assets?assetIds=' + str(placeId) +'&size=396x216&format=Png&isCircular=false')
                data = r.json()              
                self._game_image_header = data['data'][0]['imageUrl']
                self._game_image_main = data['data'][0]['imageUrl']
                #self._gameurl = 'https://www.roblox.com/games/' + str(placeId)
        
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
    
    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        attr = {}
        if self._game is not None:
            attr["game"] = self._game
        if self._game_id is not None:
            attr["game_id"] = self._game_id
            attr["place_id"] = self._placeId
            #game_url = f"{roblox_API_URL}{self._game_id}/"
            attr["game_image_header"] = self._game_image_header
            attr["game_image_main"] = self._game_image_main
        
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
