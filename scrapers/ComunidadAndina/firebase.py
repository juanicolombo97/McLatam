import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("clave.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def agregar_datos(nombre, fecha_limite, hora, contacto, documento):
    data = {"expediente_id": nombre, "fecha_limite": fecha_limite, "hora": hora, "contacto": contacto,
            "documento": documento, "pagina": "https://www.comunidadandina.org/convocatorias/",
            "estado_expediente": "NoRevisado", "Nombre_pagina": "Comunidad Andina", "Fecha_revisado": "",
            "Encargado": "", "Reporte": ""}
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
        if pagina == 'https://www.comunidadandina.org/convocatorias/':
            valores_campo.append(expediente_id)
    return valores_campo
