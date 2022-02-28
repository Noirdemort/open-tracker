'''
device.py

Managing Device and related ops

@author: Noirdemort
'''
from .DataLayer import storage
import uuid

class Device:

    collection = storage.device
    coding_keys = ["identifier", "user_id", "name", "ip_address"]
    batch_counter = 0
    
    def __init__(self):
        pass
    
    @classmethod
    def instance_from(cls, data):
        '''
            Creates a class instance from given data otherwise returns None
        '''
        
        try:
            device = cls()
            device.identifier = data["identifier"]
            device.name = data["name"]
            device.ip_address = data["ip_address"]
            
            device.set_export_object()

            return device

        except Exception as e:
            return e
    
    
    def set_export_object(self):
        '''
            Sets object for Food DB usage.
        '''
        self.export = {
            "identifier": self.identifier,
            "name": self.name,
            "ip_address": self.ip_address
        }
        
        self.id = self.export["identifier"]
    
    
    @staticmethod
    def save():
        if batch_counter == 10:
            storage.save()
            batch_counter = 0
            return
        batch_counter += 1
        return
    
    # CRUDable
    
    @staticmethod
    def read(id, all=False):
        '''
            Performs R of CRUD
        '''
        if not all:
            return Device.collection.get(id, None)
        
        devices = [] # filter device["user"]
        for device in Device.collection:
            if device["user_id"] == id:
                devices.append(device)
        
        return devices
        
    
    @staticmethod
    def create(data):
        '''
            C of CRUD. Takes in data object (dictionary) and tries to convert to class instance and store it.
            On failing return False.
        '''
        device = Device.instance_from(data)
        if isinstance(device, Device):
            device.collection[device.id] = device.export
            Device.save()
        return device
    
    
    @staticmethod
    def delete(id):
        '''
            Deletes a record from collection. D of CRUD.
        '''
        if not Device.collection.get(id, None):
            return 0
        del Device.collection[id]
        Device.save()
        return 1
        

    @staticmethod
    def update(id, data):
        '''
            Finds a record and updates with said data. U of CRUD.
        '''
        device = Device.read(id)
        if not device:
            return 0
        
        # Loop may seems like redundancy but actually protects against extra arguments in a request
        # More clearly, it avoids adding extra fields from a tailored request.
        for i in Device.coding_keys[2:]:
            if data.get(i, None):
                device[i] = data.get(i)
        
        Device.collection[id] = device
        Device.save()
        return 1




