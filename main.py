
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router
app = FastAPI()
app.title = "Mi app con FastAPI"
app.version = "0.0.1"
### add middleware to manage Error
app.add_middleware(ErrorHandler)
### add movie´s routrer 
app.include_router(movie_router)
### add autentication´s routrer 
app.include_router(user_router)
Base.metadata.create_all(bind=engine)


### message in html
@app.get('/', tags= ['home'])
def message():
    return HTMLResponse('<h1 hola mundo </h1>')
