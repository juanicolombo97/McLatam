import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("clave.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def agregar_datos(expediente_id, descripcion, pais, titulo, tipo_noticia, idioma, fecha):
    data = {"expediente_id": expediente_id, "descripcion": descripcion, "pais": pais,
            "titulo": titulo, "tipo_noticia": tipo_noticia, "idioma": idioma, "fecha": fecha,
            "pagina": "https://projects.worldbank.org/en/projects-operations/procurement?lang=en&qterm=&showrecent=true&srce=notices",
            "estado_expediente": "NoRevisado"}
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
        expediente_id = documento.get("expediente_id")
        pagina = documento.get("pagina")
        if pagina == 'https://projects.worldbank.org/en/projects-operations/procurement?lang=en&qterm=&showrecent=true&srce=notices':
            valores_campo.append(expediente_id)
    return valores_campo
