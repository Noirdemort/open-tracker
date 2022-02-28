'''
DataLayer.py

All MongoDB related Drivers and Config
    - will be its own package in future

@author: Noirdemort
'''

import json

class PersistenceLayer:

    FILENAME = "tracker.json"
    USER_KEY = "users"
    DEVICE_KEY = "devices"
    
    user = {}
    device = {}
    data = {}

    def __init__(self):
        f = open(PersistenceLayer.FILENAME, "r+")
        z = f.read()
        if z:
            self.data = json.loads(z)
            self.user = self.data.get(PersistenceLayer.USER_KEY, {})
            self.device = self.data.get(PersistenceLayer.DEVICE_KEY, {})
        f.close()
        
    def save(self):
        self.data[PersistenceLayer.USER_KEY] = self.user
        self.data[PersistenceLayer.DEVICE_KEY] = self.device
        with open(PersistenceLayer.FILENAME, "w+") as f:
            json.dump(self.data, f)
    
    
    def __del__(self):
        self.save()

storage = PersistenceLayer()
