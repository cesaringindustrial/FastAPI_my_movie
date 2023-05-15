from pydantic import BaseModel

### login and password
class User(BaseModel):
    email: str
    password: str 

