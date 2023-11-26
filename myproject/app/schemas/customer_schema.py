from pydantic import BaseModel


class Customer_Model_SignUp(BaseModel):
    name: str
    email: str
    password: str

class Customer_Model_SignIn(BaseModel):
    email: str
    password: str