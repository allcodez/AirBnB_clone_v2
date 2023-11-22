#!/usr/bin/python3
"""Defines unit tests for the User class in models/user.py."""
import os
import pep8
import models
import MySQLdb
import unittest
from datetime import datetime
from models.base_model import Base, BaseModel
from models.user import User
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

class TestUser(unittest.TestCase):
    """Unit tests for evaluating the User class functionality."""

    @classmethod
    def setUpClass(cls):
        """Setting up the environment for User testing.

        Temporarily renaming any existing file.json.
        Resetting the FileStorage objects dictionary.
        Creating instances of FileStorage, DBStorage, and User for testing.
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.filestorage = FileStorage()
        cls.user = User(email="poppy@holberton.com", password="betty98")

        if type(models.storage) == DBStorage:
            cls.dbstorage = DBStorage()
            Base.metadata.create_all(cls.dbstorage._DBStorage__engine)
            Session = sessionmaker(bind=cls.dbstorage._DBStorage__engine)
            cls.dbstorage._DBStorage__session = Session()

    @classmethod
    def tearDownClass(cls):
        """Tearing down the User testing environment.

        Restoring the original file.json.
        Deleting the FileStorage, DBStorage, and User test instances.
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.user
        del cls.filestorage
        if type(models.storage) == DBStorage:
            cls.dbstorage._DBStorage__session.close()
            del cls.dbstorage

    def test_pep8(self):
        """Checking adherence to pep8 styling."""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["models/user.py"])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_docstrings(self):
        """Ensuring the presence of docstrings."""
        self.assertIsNotNone(User.__doc__)

    def test_attributes(self):
        """Verifying the existence of attributes."""
        us = User(email="a", password="a")
        self.assertEqual(str, type(us.id))
        self.assertEqual(datetime, type(us.created_at))
        self.assertEqual(datetime, type(us.updated_at))
        self.assertTrue(hasattr(us, "__tablename__"))
        self.assertTrue(hasattr(us, "email"))
        self.assertTrue(hasattr(us, "password"))
        self.assertTrue(hasattr(us, "first_name"))
        self.assertTrue(hasattr(us, "last_name"))
        self.assertTrue(hasattr(us, "places"))
        self.assertTrue(hasattr(us, "reviews"))

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_email_not_nullable(self):
        """Ensuring that the email attribute is non-nullable."""
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(User(password="a"))
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(User(email="a"))
            self.dbstorage._DBStorage__session.commit()

    def test_is_subclass(self):
        """Verifying that User is a subclass of BaseModel."""
        self.assertTrue(issubclass(User, BaseModel))

    def test_init(self):
        """Testing the initialization process."""
        self.assertIsInstance(self.user, User)

    def test_two_models_are_unique(self):
        """Ensuring that different User instances are unique."""
        us = User(email="a", password="a")
        self.assertNotEqual(self.user.id, us.id)
        self.assertLess(self.user.created_at, us.created_at)
        self.assertLess(self.user.updated_at, us.updated_at)

    def test_init_args_kwargs(self):
        """Testing initialization with args and kwargs."""
        dt = datetime.utcnow()
        st = User("1", id="5", created_at=dt.isoformat())
        self.assertEqual(st.id, "5")
        self.assertEqual(st.created_at, dt)

    def test_str(self):
        """Testing the __str__ representation."""
        s = self.user.__str__()
        self.assertIn("[User] ({})".format(self.user.id), s)
        self.assertIn("'id': '{}'".format(self.user.id), s)
        self.assertIn("'created_at': {}".format(
            repr(self.user.created_at)), s)
        self.assertIn("'updated_at': {}".format(
            repr(self.user.updated_at)), s)
        self.assertIn("'email': '{}'".format(self.user.email), s)
        self.assertIn("'password': '{}'".format(self.user.password), s)

    @unittest.skipIf(type(models.storage) == DBStorage,
                     "Testing DBStorage")
    def test_save_filestorage(self):
        """Testing the save method with FileStorage."""
        old = self.user.updated_at
        self.user.save()
        self.assertLess(old, self.user.updated_at)
        with open("file.json", "r") as f:
            self.assertIn("User." + self.user.id, f.read())

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_save_dbstorage(self):
        """Testing the save method with DBStorage."""
        old = self.user.updated_at
        self.user.save()
        self.assertLess(old, self.user.updated_at)
        db = MySQLdb.connect(user="hbnb_test",
                             passwd="hbnb_test_pwd",
                             db="hbnb_test_db")
        cursor = db.cursor()
        cursor.execute("SELECT * \
                          FROM `users` \
                         WHERE BINARY email = '{}'".
                       format(self.user.email))
        query = cursor.fetchall()
        self.assertEqual(1, len(query))
        self.assertEqual(self.user.id, query[0][0])
        cursor.close()

    def test_to_dict(self):
        """Testing the to_dict method."""
        user_dict = self.user.to_dict()
        self.assertEqual(dict, type(user_dict))
        self.assertEqual(self.user.id, user_dict["id"])
        self.assertEqual("User", user_dict["__class__"])
        self.assertEqual(self.user.created_at.isoformat(),
                         user_dict["created_at"])
        self.assertEqual(self.user.updated_at.isoformat(),
                         user_dict["updated_at"])
        self.assertEqual(self.user.email, user_dict["email"])
        self.assertEqual(self.user.password, user_dict["password"])


if __name__ == "__main__":
    unittest.main()
