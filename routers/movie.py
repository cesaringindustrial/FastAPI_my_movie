from fastapi import APIRouter
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router= APIRouter()


movies= [
    {
        "id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
    }, 
    {
        "id": 2,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 9.8,
		"category": "Acción"
    }
]



### get movies
@movie_router.get('/movies', tags=['movies'],response_model=List[Movie],status_code=200,dependencies=[Depends(JWTBearer())])
def get_movies() -> List[movies]:
    db= Session()
    result= MovieService(db).get_movies()
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

### get movie
@movie_router.get('/movies/{id}',tags=['movies'],response_model=Movie,status_code=404)
def get_movie(id: int= Path(ge=1,le=2000))->Movie:
    db= Session()
    result= MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message':'No encontrado'})
    return JSONResponse(status_code=200,content=jsonable_encoder(result)) 

### movies by category
@movie_router.get('/movies/', tags=['movies'],response_model=List[Movie])
def get_movies_by_category(category:str =Query(min_length=5,max_length=15)) ->List[movies]:
    db= Session()
    result= MovieService(db).get_movies_by_category(category)
    return JSONResponse(status_code=200,content=jsonable_encoder(result)) 

### create movie   
@movie_router.post('/movies', tags=['movies'],response_model= dict,status_code=201)
def create_movie(movie:Movie) ->dict:
    db= Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201,content={"message": "Se ha registrado la pelicula"})

### update movie
@movie_router.put('/movies/{id}', tags=['movies'],response_model= dict,status_code=200)
def update_movie(id: int, movie:Movie ) ->dict:
    db= Session()
    result= MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    MovieService(db).update_movie(id,movie)
    return JSONResponse(status_code=200,content={"message": "Se ha modificado la pelicula"})

### delete movie       
@movie_router.delete('/movies/{id}', tags=['movies'],response_model= dict,status_code=200)
def delete_movie(id: int) ->dict:
    db= Session()
    result: MovieModel = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message':'No encontrado'})
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code=200,content={"message": "Se ha elimanido la pelicula"})
     