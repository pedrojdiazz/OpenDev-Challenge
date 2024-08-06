from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi_pagination import add_pagination
from src.routes import leads_routes
from src.exceptions import DatabaseException, NotFoundException, InvalidRequestException
from src.database import engine, Base
from fastapi.staticfiles import StaticFiles

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(leads_routes.router)
add_pagination(app)



@app.get("/", response_class=HTMLResponse)
def read_index():
    with open("static/index.html") as f:
        return HTMLResponse(content=f.read())
    

@app.exception_handler(DatabaseException)
def database_exception_handler(request: Request, exc: DatabaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},)


@app.exception_handler(NotFoundException)
def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )


@app.exception_handler(InvalidRequestException)
def invalid_request_exception_handler(request: Request, exc : InvalidRequestException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )