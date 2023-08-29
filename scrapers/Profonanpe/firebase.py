import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("clave.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def agregar_datos():
    data = {"expediente_id": "",
            "pagina": "https://convocatoriasprofonanpe.vform.pe/", "estado_expediente": "NoRevisado",
            "Nombre_pagina": "Profonanpe", "Fecha_revisado": "", "Encargado": "", "Reporte": ""}
    db.collection("crm").add(data)
