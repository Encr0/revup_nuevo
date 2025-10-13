
from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from models.usuarios import crear_usuario, buscar_usuario

router = APIRouter()

@router.post("/register")
async def register_user(email: str = Form(...), password: str = Form(...)):
    resultado = crear_usuario(email=email, password=password)
    if resultado:
        return JSONResponse(status_code=201, content={"msg": "Registro exitoso"})
    else:
        return JSONResponse(status_code=409, content={"error": "Usuario ya existe"})

@router.post("/login")
async def login_user(email: str = Form(...), password: str = Form(...)):
    usuario = buscar_usuario(email=email, password=password)
    if usuario:
        return JSONResponse(status_code=200, content={"msg": "Login exitoso"})
    else:
        return JSONResponse(status_code=401, content={"error": "Credenciales inválidas"})
