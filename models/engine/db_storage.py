#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import urllib.parse

from models.base_model import BaseModel, Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place, place_amenity
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """The database storage class
    Manages storage of hbnb models"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialise the table"""
        user = os.getenv('HBNB_MYSQL_USER')
        password = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')

        db_uri = "mysql+mysqldb://{}:{}@{}:3306/{}".format(
            user, password, host, db)

        self.__engine = create_engine(
                db_uri, pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))

    def all(self, cls=None):
        """Returns a dictionary containing the
        objects of the models in storage"""
        objects = dict()
        all_classes = [User, State, City, Amenity, Place, Review]

        if cls is None:
            for _class in all_classes:
                class_obj = self.__session.query(_class)
                for obj in class_obj.all():
                    obj_key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    objects[obj_key] = obj
        else:
            query = self.__session.query(cls)
            for obj in query:
                obj_key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                objects[obj_key] = obj

        return objects

    def new(self, obj):
        """Adds the object to the current db session"""
        if obj is not None:
            self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """To reload the db"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
                bind=self.__engine,
                expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Closes the storage engine."""
        self.__session.close()
