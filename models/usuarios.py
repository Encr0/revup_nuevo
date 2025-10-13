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

def crear_usuario(email: str, password: str):
    cnx = get_connection()
    if not cnx:
        print("DB Connection error")
        return False
    cursor = cnx.cursor()
    # Verifica si el usuario ya existe 
    cursor.execute(
        "SELECT id FROM usuarios WHERE email=%s", (email,)
    )
    if cursor.fetchone():
        cursor.close()
        cnx.close()
        return False  # Usuario ya existe
    # Inserta el nuevo usuario
    cursor.execute(
        "INSERT INTO usuarios (email, password, disabled) VALUES (%s, %s, 0)",
        (email, password)
    )
    cnx.commit()
    cursor.close()
    cnx.close()
    return True
