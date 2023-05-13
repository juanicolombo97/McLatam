import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("clave.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def agregar_datos(oficina, titulo, fecha, estado, referencia):
    data = {"Expediente_id": referencia, "Oficina": oficina,"Titulo": titulo, "Fecha": fecha, "Estado": estado,
            "Estado_expediente": "NoRevisado"}
    db.collection("crm").add(data)


def obtener_ids():
    # Obtén una referencia a la instancia de Firestore
    db = firestore.client()

    # Ejecuta la consulta para obtener todos los documentos de la colección
    documentos = db.collection("crm").get()

    # Crea una lista para almacenar los valores del campo
    valores_campo = []

    # Itera sobre los documentos y extrae el valor del campo deseado
    for documento in documentos:
        valor = documento.get("Expediente_id")
        valores_campo.append(valor)
    return valores_campo
