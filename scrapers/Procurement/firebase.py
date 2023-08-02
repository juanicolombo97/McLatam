import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("clave.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def agregar_datos(numero_referencia, titulo, oficina, pais, proceso, fecha_hasta, fecha_publicacion):
    data = {"expediente_id": numero_referencia, "titulo": titulo, "oficina": oficina, "pais": pais, "proceso": proceso,
            "fecha_hasta": fecha_hasta, "fecha_publicacion": fecha_publicacion,
            "pagina": "https://procurement-notices.undp.org/search.cfm", "estado_expediente": "NoRevisado"}
    db.collection("crm").add(data)
