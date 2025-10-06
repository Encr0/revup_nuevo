from core.database import get_connection

def buscar_usuario(email: str, password: str):
    cnx = get_connection()
    if not cnx:
        print("DB Connection error")
        return None
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM usuarios WHERE email=%s AND password=%s AND disabled=0", (email, password)
    )
    usuario = cursor.fetchone()
    print("Resultado usuario:", usuario)  # <-- DEBUG aquí
    cursor.close()
    cnx.close()
    return usuario

