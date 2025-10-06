from fastapi import APIRouter, HTTPException, Body
from models.empleados import EmpleadosModel

empleados = EmpleadosModel.get_all()


router = APIRouter(prefix="/empleados", tags=["Empleados"])

@router.get("/")
def list_empleados():
    empleados = EmpleadosModel.get_all()
    return empleados

@router.post("/")
def create_empleado( nombres: str, apellidos: str, rut: str, fecha_nacimiento: str, direccion: str,
    empresa_id: int, tipo_contrato: str, fecha_inicio: str, fecha_termino:str,
    sueldo_base: int, afp_id: int, salud_id: int, afc_id: int):
        
    #Crear empleado:
    success = EmpleadosModel.create( nombres, apellidos, rut, fecha_nacimiento, direccion,
    empresa_id, tipo_contrato, fecha_inicio, fecha_termino,
    sueldo_base, afp_id, salud_id, afc_id
    )
    if not success:
        raise HTTPException(status_code=500, detail="Empleado could not be created")
    return {"message": "Empleado created successfully"}

@router.post("/nuevo")
def create_empleado_form(
    nombres: str = Body(...), apellidos: str = Body(...), rut: str = Body(...), fecha_nacimiento: str = Body(...), direccion: str = Body(...),
    empresa_id: int = Body(...), tipo_contrato: str = Body(...), fecha_inicio: str = Body(...), fecha_termino:str = Body(...),
    sueldo_base: int = Body(...), afp_id: int = Body(...), salud_id: int = Body(...), afc_id: int = Body(...)
):
    success = EmpleadosModel.create( nombres, apellidos, rut, fecha_nacimiento, direccion,
    empresa_id, tipo_contrato, fecha_inicio, fecha_termino,
    sueldo_base, afp_id, salud_id, afc_id
    )

    if not success:
        raise HTTPException(status_code=500, detail="Empleado could not be created")
    return {"message": "Empleado created successfully"}
