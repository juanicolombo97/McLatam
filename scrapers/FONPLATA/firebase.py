import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("clave.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def agregar_datos(prestamo, modalidad, objeto, descripcion, presupuesto, fecha_publicacion, fecha_presentacion, pais):
    data = {"expediente_id": prestamo, "modalidad": modalidad, "objeto": objeto, "descripcion": descripcion,
            "presupuesto": presupuesto, "fecha_publicacion": fecha_publicacion, "pais": pais,
            "fecha_presentacion": fecha_presentacion, "pagina": "https://www.fonplata.org/es/adquisiciones-en-proyectos",
            "estado_expediente": "NoRevisado"}
    db.collection("crm").add(data)
