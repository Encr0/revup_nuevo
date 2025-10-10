from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.empleados import EmpleadosModel
from models.usuarios import buscar_usuario

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def login(request: Request, msg: str = ""):
    if msg is None:
        msg = ""
    return templates.TemplateResponse("login.html", {"request": request, "titulo": "Login | Revup Group", "msg": msg})


@router.post("/home")
async def login_post(request: Request, email: str = Form(...), password: str = Form(...)):
    print(f"POST: {email=}, {password=}")
    usuario = buscar_usuario(email=email, password=password)
    print("Usuario encontrado en login_post:", usuario)
    if usuario: 
        return RedirectResponse(url="/home", status_code=303)
    else: 
        return RedirectResponse(url="/?msg=Datos%20incorrectos", status_code=303)



@router.get("/home", response_class=HTMLResponse)
def lista(request: Request) -> HTMLResponse:
    try:
        empleados = EmpleadosModel.get_all()
    except Exception as e:
        empleados = []
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "empleados": empleados,
            "titulo": "Lista de empleados | Revup Group"
        }
    )
@router.get("/lista", response_class=HTMLResponse)
def lista(request: Request) -> HTMLResponse:
    try:
        empleados = EmpleadosModel.get_all()
    except Exception as e:
        empleados = []
    return templates.TemplateResponse(
        "lista.html",
        {
            "request": request,
            "empleados": empleados,
            "titulo": "Lista de empleados | Revup Group"
        }
    )
