import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from functools import wraps
from Tables import Contact
from Tables import Base


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
        

        
    '''
Questo decoratore gestisce la creazione, il commit e la chiusura di sessioni di database SQLAlchemy all'interno dei metodi di classe.

Parametri:

- `func`: La funzione da decorare, che deve essere un metodo di classe.

Comportamento:

1. Quando viene chiamata una funzione decorata con `session_management`, viene eseguita la seguente procedura:

   a. Stampa un messaggio indicando che la gestione della sessione è stata chiamata.
   
   b. Crea una nuova sessione utilizzando `self.session_maker()`, dove `self` è l'istanza della classe contenente il metodo decorato.
   
   c. Prova ad eseguire la funzione originale (`func`) passando la sessione come argomento `session`.
   
   d. Se si verifica un'eccezione durante l'esecuzione della funzione, la sessione viene riportata allo stato precedente con `rollback()`, chiusa con `close()` e l'eccezione viene propagata.
   
   e. Indipendentemente dall'eccezione, la sessione viene sempre committata con `commit()`.
   
   f. Dopo il commit, vengono eseguite le seguenti azioni:
   
      - `expunge_all()`: Rimuove tutti gli oggetti dalla sessione.
      
      - `session.close()`: Chiude la sessione.
      
2. Durante ciascuna fase, vengono stampati messaggi di debug per indicare lo stato corrente delle operazioni.

Note:

- L'uso di `@wraps(func)` assicura che la funzione decorata conservi il suo nome, la sua documentazione e altri attributi.

- `InvalidRequestError` è un'eccezione che può essere sollevata durante le operazioni di commit, expunge o chiusura della sessione. La gestione di questa eccezione è inclusa per garantire che il decoratore funzioni correttamente anche in situazioni anomale.
'''

    def session_management(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                print("session management called...")
                session = self.session_maker()
                print("session created...")
                try:
                    kwargs["session"] = session
                    result = func(self, *args, **kwargs)
                    return result
                except:
                    session.rollback()
                    session.close()
                    raise
                finally:
                    if session:
                        try:
                            print("committing session...")
                            session.commit()
                            print("committed!")
                            pass
                        except InvalidRequestError:
                            print("already committed!")
                            pass
                        
                        
                        try:
                            session.expunge_all()
                            print("expunged all!")
                        except InvalidRequestError:
                            print("nothing to expunge!")
                            pass
                        
                        
                        if session.is_active:
                            try:
                                print("closing session...")
                                session.close()
                                print("closed!")
                                pass
                            except InvalidRequestError:
                                print("already closed!")
                                pass

            return wrapper
    
    
    
    @session_management
    def get_contacts(self, session=None):
        """
        Retrieve all contacts from the database.

        Args:
            session: The database session to use (optional).

        Returns:
            A list of Contact objects representing all contacts in the database.
        """
        return session.query(Contact).all()
    
    @session_management
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
    
    @session_management
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
        contact = Contact(name=name, surname=surname, phone=phone, email=email)
        session.add(contact)
        return contact
    
    @session_management
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
    
    @session_management
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
    
    
        
    
    
    
    
    






