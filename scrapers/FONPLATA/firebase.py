import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("clave.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def agregar_datos(prestamo, modalidad, objeto, descripcion, presupuesto, fecha_publicacion, fecha_presentacion, pais):
    data = {"expediente_id": prestamo, "modalidad": modalidad, "objeto": objeto, "descripcion": descripcion,
            "presupuesto": presupuesto, "fecha_publicacion": fecha_publicacion, "pais": pais,
            "fecha_presentacion": fecha_presentacion,
            "pagina": "https://www.fonplata.org/es/adquisiciones-en-proyectos",
            "estado_expediente": "NoRevisado", "Nombre_pagina": "Fonplata", "Fecha_revisado": "", "Encargado": "",
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
        if pagina == 'https://www.fonplata.org/es/adquisiciones-en-proyectos':
            valores_campo.append(expediente_id)
    return valores_campo
