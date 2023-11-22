#!/usr/bin/python3
"""Defines the FileStorage class."""

import json
from models.base_model import BaseModel
from models.place import Place
from models.amenity import Amenity
from models.user import User
from models.city import City
from models.state import State
from models.review import Review

class FileStorage:
    """Represents a storage engine with abstracted functionality.

    Instance Attributes:
        __file_path (str): The file name used to store objects.
        __objects (dict): A dictionary containing instantiated objects.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Retrieve a dictionary of instantiated objects stored in __objects.

        If a specific cls is provided, returns objects of that type.
        Otherwise, returns the entire __objects dictionary.
        """
        if cls is not None:
            if type(cls) == str:
                cls = eval(cls)
            cls_dict = {}
            for key, value in self.__objects.items():
                if type(value) == cls:
                    cls_dict[key] = value
            return cls_dict
        return self.__objects

    def new(self, obj):
        """Add obj to __objects with the key <obj_class_name>.id."""
        self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj

    def save(self):
        """Serialize __objects and write to the JSON file __file_path."""
        object_dict = {key: obj.to_dict() for key, obj in self.__objects.items()}
        with open(self.__file_path, "w", encoding="utf-8") as file:
            json.dump(object_dict, file)

    def reload(self):
        """Deserialize the JSON file __file_path to populate __objects, if it exists."""
        try:
            with open(self.__file_path, "r", encoding="utf-8") as file:
                for obj_data in json.load(file).values():
                    class_name = obj_data["__class__"]
                    del obj_data["__class__"]
                    self.new(eval(class_name)(**obj_data))
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Remove a specified object from __objects, if present."""
        try:
            del self.__objects["{}.{}".format(type(obj).__name__, obj.id)]
        except (AttributeError, KeyError):
            pass

    def close(self):
        """Invoke the reload method."""
        self.reload()
