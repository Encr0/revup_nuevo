from core.database import get_connection
from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel, Field, ConfigDict
from typing_extensions import Annotated
from annotated_types import MinLen, MaxLen

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

class EmpleadosModel:

    @staticmethod
    def get_all() -> List[EmpleadoInDB]:
        cnx = None
        cursor = None
        try:
            cnx = get_connection()
            if not cnx:
                return []
            cursor = cnx.cursor(dictionary=True)
            cursor.execute("SELECT id, nombres, apellidos, rut, fecha_nacimiento, direccion FROM empleados")
            empleados = cursor.fetchall()
            return [EmpleadoInDB(**emp) for emp in empleados]
        except Exception as e:
            print(f"Error obteniendo empleados: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()

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
