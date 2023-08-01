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
