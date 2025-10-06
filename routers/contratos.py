from core.database import get_connection
from typing import Optional

def crear_contrato_por_empleado(
    empleado_id: int,
    empresa_id: int,
    tipo: str,
    fecha_inicio: str,
    sueldo_base: int,
    afp_id: int,
    salud_id: int,
    afc_id: int
) -> bool:
    cnx = None
    cursor = None
    try:
        cnx = get_connection()
        if not cnx:
            return False
        cursor = cnx.cursor()
        cursor.execute(
            """
            INSERT INTO contratos (
                empleado_id, empresa_id, tipo, fecha_inicio, sueldo_base, afp_id, salud_id, afc_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, 
            (empleado_id, empresa_id, tipo, fecha_inicio, sueldo_base, afp_id, salud_id, afc_id)
        )
        cnx.commit()
        return True
    except Exception as e:
        if cnx:
            cnx.rollback()
        print(f"Error al crear contrato: {e}")  # Para debugging
        return False
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()
