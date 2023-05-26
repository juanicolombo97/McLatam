import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import FieldFilter

cred = credentials.Certificate("clave.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def agregar_datos(titulo, fecha_limite, publicado, organismo_onu, tipo_anuncio, referencia, pais):
    data = {"Expediente_id": referencia, "Fecha_limite": fecha_limite, "Titulo": titulo, "Publicado": publicado,
            "Organismo_onu": organismo_onu, "Tipo_anuncio": tipo_anuncio, "Pais": pais,
            "Pagina": "https://www.ungm.org/Public/Notice", "Estado_expediente": "NoRevisado"}
    db.collection("crm").add(data)
