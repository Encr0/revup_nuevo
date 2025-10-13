from fastapi import FastAPI
from routers import empleados, public
from fastapi.templating import Jinja2Templates
from routers.hr import router as hr_router


app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Rutas privadas (API para empleados)
app.include_router(empleados.router, prefix="/api/v1")
app.include_router(hr_router, prefix="/hr")

# Rutas públicas (web clásica)
app.include_router(public.router)

# Si quieres correr local con Uvicorn (desarrollo), recuerda:
# uvicorn main:app --reload
