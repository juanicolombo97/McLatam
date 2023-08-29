import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("clave.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def agregar_datos(titulo, fecha_limite, publicado, organismo_onu, tipo_anuncio, referencia, pais):
    data = {"expediente_id": referencia, "fecha_limite": fecha_limite, "titulo": titulo, "publicado": publicado,
            "organismo_onu": organismo_onu, "tipo_anuncio": tipo_anuncio, "pais": pais,
            "pagina": "https://www.ungm.org/Public/Notice", "estado_expediente": "NoRevisado",
            "Nombre_pagina": "Naciones Unidas Global", "Fecha_revisado": "", "Encargado": "", "Reporte": ""}
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
        if pagina == 'https://www.ungm.org/Public/Notice':
            valores_campo.append(expediente_id)
    return valores_campo
