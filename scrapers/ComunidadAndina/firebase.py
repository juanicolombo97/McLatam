import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("clave.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def agregar_datos(nombre, fecha_limite, hora, contacto, documento):
    data = {"expediente_id": nombre, "fecha_limite": fecha_limite, "hora": hora, "contacto": contacto,
            "documento": documento, "pagina": "https://www.comunidadandina.org/convocatorias/",
            "estado_expediente": "NoRevisado"}
    db.collection("crm").add(data)
