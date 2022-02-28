'''
user.py

Managing User and related ops

@author: Noirdemort
'''
from .DataLayer import storage
from .device import Device
import uuid

class User:

    index_field = "_id"
    collection = storage.user
    coding_keys = ["_id", "public_key"]
    batch_counter = 0
    
    def __init__(self):
        pass
    
    @classmethod
    def instance_from(cls, data):
        '''
            Creates a class instance from given data otherwise returns None
        '''
        
        try:
            user = cls()
            user.public_key = data["public_key"]
            
            user.set_export_object()

            return user

        except Exception as e:
            return e
    
    
    def set_export_object(self):
        '''
            Sets object for Food DB usage.
        '''
        self.export = {
            "_id": str(uuid.uuid4()),
            "public_key": self.public_key
        }
        
        self.id = self.export["_id"]
    
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
    def read(id):
        '''
            Performs R of CRUD
        '''
        return User.collection.get(id, None) if id else None
    
    @staticmethod
    def create(data):
        '''
            C of CRUD. Takes in data object (dictionary) and tries to convert to class instance and store it.
            On failing return False.
        '''
        user = User.instance_from(data)
        if isinstance(user, User):
            user.collection[user.id] = user.export
            User.save()
        return user
    
    
    @staticmethod
    def delete(id):
        '''
            Deletes a record from collection. D of CRUD.
        '''
        if not User.collection.get(id, None):
            return 0
        del User.collection[id]
        devices = Device.read(id, all=True)
        for device in devices:
            Device.delete(device["identifier"])
        User.save()
        return 1
        

    @staticmethod
    def update(id, data):
        '''
            Finds a record and updates with said data. U of CRUD.
        '''
        user = User.read(id)
        if not user:
            return 0
        
        User.collection[id]["public_key"] = data
        User.save()
        return 1




