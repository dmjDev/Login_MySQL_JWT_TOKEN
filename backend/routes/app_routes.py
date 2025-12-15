from fastapi import APIRouter

app_routes = APIRouter()

## Añadir ruta favicon
from fastapi.responses import FileResponse
@app_routes.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")
##

@app_routes.get("/")
def root():
    return "Hi i'm FastAPI"