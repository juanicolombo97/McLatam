import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("clave.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def agregar_datos(titulo, fecha_limite, publicado, organismo_onu, tipo_anuncio, referencia, pais):
    data = {"expediente_id": referencia, "fecha_limite": fecha_limite, "titulo": titulo, "publicado": publicado,
            "organismo_onu": organismo_onu, "tipo_anuncio": tipo_anuncio, "pais": pais,
            "pagina": "https://www.ungm.org/Public/Notice", "estado_expediente": "NoRevisado"}
    db.collection("crm").add(data)