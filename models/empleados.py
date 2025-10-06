from core.database import get_connection
from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
from typing_extensions import Annotated
from annotated_types import MinLen, MaxLen

# Campos utilizados en la tabla empleados
CAMPOS = ["id", "nombres", "apellidos", "rut", "fecha_nacimiento", "direccion"]

class EmpleadoBase(BaseModel):
    nombres: Annotated[str, MinLen(1)] = Field(..., description="Nombres del empleado")
    apellidos: Annotated[str, MinLen(1)] = Field(..., description="Apellidos del empleado")
    rut: Annotated[str, MinLen(1), MaxLen(12)] = Field(..., description="RUT del empleado")
    fecha_nacimiento: date = Field(..., description="Fecha de nacimiento")
    direccion: Annotated[str, MinLen(1)] = Field(..., description="Dirección del empleado")
    model_config = ConfigDict(from_attributes=True)

class EmpleadoCreate(EmpleadoBase):
    pass

class EmpleadoInDB(EmpleadoBase):
    id: int = Field(..., description="ID del empleado")

def normalizar_empleado(emp):
    # Si viene como tupla, conviértelo a dict
    if not isinstance(emp, dict):
        emp = dict(zip(CAMPOS, emp))
    # Verifica y normaliza los tipos
    if 'id' in emp and isinstance(emp['id'], Decimal):
        emp['id'] = int(emp['id'])
    for campo in ['nombres', 'apellidos', 'rut', 'direccion']:
        if campo in emp and emp[campo] is not None:
            if isinstance(emp[campo], Decimal) or isinstance(emp[campo], bytes):
                emp[campo] = str(emp[campo])
    # Fecha nacimiento en formato datetime a date
    if 'fecha_nacimiento' in emp and emp['fecha_nacimiento'] is not None:
        if isinstance(emp['fecha_nacimiento'], datetime):
            emp['fecha_nacimiento'] = emp['fecha_nacimiento'].date()
    # Valor por defecto si hay valores faltantes
    for field in CAMPOS:
        if field not in emp or emp[field] is None:
            if field == "id":
                emp[field] = 0
            elif field == "fecha_nacimiento":
                emp[field] = date(2000,1,1)
            else:
                emp[field] = ""
    return emp

class EmpleadosModel:
    @staticmethod
    def get_all() -> List[EmpleadoInDB]:
        cnx = get_connection()
        if not cnx:
            return []
        cursor = cnx.cursor(dictionary=True)  # Si tu adaptador no soporta esto, elimina "dictionary=True"
        try:
            cursor.execute(
                "SELECT id, nombres, apellidos, rut, fecha_nacimiento, direccion FROM empleados"
            )
            empleados = cursor.fetchall()
        finally:
            cursor.close()
            cnx.close()
        result = []
        for emp in empleados:
            emp = normalizar_empleado(emp)
            try:
                result.append(EmpleadoInDB(**emp))
            except Exception as e:
                print(f"Error instanciando EmpleadoInDB con {emp}: {e}")
        return result

    @staticmethod
    def create(
        nombres, apellidos, rut, fecha_nacimiento, direccion,
        empresa_id, tipo_contrato, fecha_inicio, fecha_termino,
        sueldo_base, afp_id, salud_id, afc_id
    ) -> Optional[int]:
        cnx = None
        cursor = None
        try:
            cnx = get_connection()
            if not cnx:
                return None
            cursor = cnx.cursor()
            # Si llega fecha como string, convertir a date
            if isinstance(fecha_nacimiento, str):
                fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
            if isinstance(fecha_inicio, str):
                fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            if isinstance(fecha_termino, str) and fecha_termino:
                fecha_termino = datetime.strptime(fecha_termino, "%Y-%m-%d").date()
            elif fecha_termino in [None, ""]:
                fecha_termino = None
            # Insertar empleado
            sql_empleado = """
            INSERT INTO empleados (nombres, apellidos, rut, fecha_nacimiento, direccion)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql_empleado, (nombres, apellidos, rut, fecha_nacimiento, direccion))
            empleado_id = cursor.lastrowid

            # Insertar contrato
            sql_contrato = """
            INSERT INTO contratos (
                empleado_id, empresa_id, tipo, fecha_inicio, fecha_termino, sueldo_base, afp_id, salud_id, afc_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_contrato, (
                empleado_id, empresa_id, tipo_contrato, fecha_inicio,
                fecha_termino, sueldo_base, afp_id, salud_id, afc_id
            ))

            cnx.commit()
            return empleado_id

        except Exception as e:
            if cnx:
                cnx.rollback()
            print(f"Error creando empleado: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()
