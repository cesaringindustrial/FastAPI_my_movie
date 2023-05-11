from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from jwt_manager import create_token
from pydantic import BaseModel

autentication_router=  APIRouter()


### login and password
class User(BaseModel):
    email: str
    password: str 

### autentication login and password
@autentication_router.post('/login', tags=['auth'],status_code=200)
def login(user: User):
    if user.email == "admin@gmail.com" and user.password== "admin":
        token: str =create_token(user.dict())
    return JSONResponse(status_code=200, content=token)