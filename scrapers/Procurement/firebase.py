import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("clave.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def agregar_datos(numero_referencia, titulo, oficina, pais, proceso, fecha_hasta, fecha_publicacion):
    data = {"expediente_id": numero_referencia, "titulo": titulo, "oficina": oficina, "pais": pais, "proceso": proceso,
            "fecha_hasta": fecha_hasta, "fecha_publicacion": fecha_publicacion,
            "pagina": "https://procurement-notices.undp.org/search.cfm", "estado_expediente": "NoRevisado",
            "Nombre_pagina": "Procurement Notices", "Fecha_revisado": "", "Encargado": "",
            "Reporte": ""}
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
        if pagina == 'https://procurement-notices.undp.org/search.cfm':
            valores_campo.append(expediente_id)
    return valores_campo
