from pydantic import BaseModel

class ContactCreateRequest(BaseModel):
    name: str
    surname: str
    phone: str
    email: str