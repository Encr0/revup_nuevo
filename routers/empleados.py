from fastapi import APIRouter, HTTPException
from models.empleados import EmpleadosModel
from pydantic import BaseModel
from datetime import date
from typing import Optional

router = APIRouter(prefix="/empleados", tags=["Empleados"])

class EmpleadoRequest(BaseModel):
    nombres: str
    apellidos: str
    rut: str
    fecha_nacimiento: date
    direccion: str
    empresa_id: int
    tipo_contrato: str
    fecha_inicio: date
    fecha_termino: Optional[date] = None
    sueldo_base: int
    afp_id: int
    salud_id: int
    afc_id: int

@router.get("/")
def list_empleados():
    empleados = EmpleadosModel.get_all()
    return empleados

@router.post("/")
def create_empleado(data: EmpleadoRequest):
    empleado_id = EmpleadosModel.create(
        data.nombres, data.apellidos, data.rut, data.fecha_nacimiento, data.direccion,
        data.empresa_id, data.tipo_contrato, data.fecha_inicio, data.fecha_termino,
        data.sueldo_base, data.afp_id, data.salud_id, data.afc_id
    )
    if not empleado_id:
        raise HTTPException(status_code=500, detail="Empleado could not be created")
    return {"message": "Empleado created successfully", "empleado_id": empleado_id}
