import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from functools import wraps
from Tables import Contact
from Tables import Base
from SessionManager import session_management
import re

EMAIL_REGEX = "^[\w\.]+@([\w-]+\.)+[\w-]{2,4}$"
PHONE_REGEX = "^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$"


class DatabaseManager:
            
    def __init__(self, database_uri="sqlite:///contacts.db"):
            """
            Initializes a DatabaseManager object.

            Args:
                database_uri (str): The URI of the database. Defaults to "sqlite:///contacts.db".
            """
            self.engine = create_engine(database_uri, echo=True)
            self.metadata = MetaData()
            self.session_maker = sessionmaker(bind=self.engine)
            self.create_tables()
        
    def create_tables(self):
        Base.metadata.create_all(self.engine)
    
    
    
    @session_management()
    def get_contacts(self, session=None):
        """
        Retrieve all contacts from the database.

        Args:
            session: The database session to use (optional).

        Returns:
            A list of Contact objects representing all contacts in the database.
        """
        return session.query(Contact).all()
    
    @session_management()
    def get_contact(self, id, session=None):
        """
        Retrieve a contact from the database by its ID.

        Args:
            id (int): The ID of the contact to retrieve.
            session (Session, optional): The database session. Defaults to None.

        Returns:
            Contact: The retrieved contact object, or None if not found.
        """
        return session.query(Contact).filter(Contact.id == id).first()
    
    @session_management(auto_commit=True)
    def create_contact(self, name, surname, phone, email, session=None):
        """
        Create a new contact and add it to the database.

        Args:
            name (str): The name of the contact.
            surname (str): The surname of the contact.
            phone (str): The phone number of the contact.
            email (str): The email address of the contact.
            session (Session, optional): The database session. Defaults to None.

        Returns:
            Contact: The created contact object.
        """

        if (not re.match(EMAIL_REGEX, email)):
            raise ValueError("email doesn't match the EMAIL_REGEX")
        
        if (not re.match(PHONE_REGEX, phone)):
            raise ValueError("phone doesn't match the PHONE_REGEX")
        


        contact = Contact(name=name, surname=surname, phone=phone, email=email)
        session.add(contact)
        return contact
    
    @session_management(auto_commit=True)
    def update_contact(self, contact, session=None):
        """
        Update a contact in the database.

        Args:
            contact: The contact object to be updated.
            session: The database session (optional).

        Returns:
            The updated contact object.
        """
        session.add(contact)
        return contact
    
    @session_management(auto_commit=True)
    def delete_contact(self, contact, session=None):
        """
        Deletes a contact from the database.

        Args:
            contact: The contact object to be deleted.
            session: The database session (optional).

        Returns:
            The deleted contact object.
        """
        session.delete(contact)
        return contact
    
    
        
    
    
    
    
    






