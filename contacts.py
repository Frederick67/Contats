import fastapi
from fastapi import FastAPI, HTTPException
from DatabaseManager import DatabaseManager
from Tables import Contact
from Models import ContactCreateRequest

app = FastAPI()
db = DatabaseManager()


@app.get("/contacts")
async def get_contacts():
    """
    Retrieve all contacts from the database.
    
    Returns:
        List: A list of contacts.
    """
    return db.get_contacts()

@app.get("/contacts/{contact_id}")
async def get_contact(contact_id: int):
    """
    Retrieve a contact by its ID.

    Args:
        contact_id (int): The ID of the contact to retrieve.

    Returns:
        dict: The contact information.

    Raises:
        HTTPException: If the contact is not found.
    """
    contact = db.get_contact(contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@app.post("/contacts")
async def create_contact(o: ContactCreateRequest):
    """
    Create a new contact.

    Args:
        name (str): The name of the contact.
        surname (str): The surname of the contact.
        phone (str): The phone number of the contact.
        email (str): The email address of the contact.

    Returns:
        dict: The contact information.
    """
    return db.create_contact(o.name, o.surname, o.phone, o.email)

@app.put("/contacts/{contact_id}")
async def update_contact(contact_id: int, name: str, surname: str, phone: str, email: str):
    """
    Update an existing contact.

    Args:
        contact_id (int): The ID of the contact to update.
        name (str): The name of the contact.
        surname (str): The surname of the contact.
        phone (str): The phone number of the contact.
        email (str): The email address of the contact.

    Returns:
        dict: The contact information.

    Raises:
        HTTPException: If the contact is not found.
    """
    contact = db.get_contact(contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    contact.name = name
    contact.surname = surname
    contact.phone = phone
    contact.email = email
    return db.update_contact(contact)

@app.delete("/contacts/{contact_id}")
async def delete_contact(contact_id: int):
    """
    Delete a contact by its ID.

    Args:
        contact_id (int): The ID of the contact to delete.

    Returns:
        dict: The contact information.

    Raises:
        HTTPException: If the contact is not found.
    """
    contact = db.get_contact(contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db.delete_contact(contact)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0" , port=8000)

    

