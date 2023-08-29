import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("/Users/mickyconca/Desktop/McLatam/scrapers/clave.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


# BANCO MUNDIAL
def agregar_datos_banco_mundial(expediente_id, descripcion, pais, titulo, tipo_noticia, idioma, fecha):
    data = {"expediente_id": expediente_id, "descripcion": descripcion, "pais": pais,
            "titulo": titulo, "tipo_noticia": tipo_noticia, "idioma": idioma, "fecha": fecha,
            "pagina": "https://projects.worldbank.org/en/projects-operations/procurement?lang=en&qterm=&showrecent=true&srce=notices",
            "estado_expediente": "NoRevisado", "Nombre_pagina": "Banco Mundial", "Fecha_revisado": "", "Encargado": "",
            "Reporte": ""}
    db.collection("crm").add(data)


def obtener_ids_banco_mundial():
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
        if pagina == 'https://projects.worldbank.org/en/projects-operations/procurement?lang=en&qterm=&showrecent=true&srce=notices':
            valores_campo.append(expediente_id)
    return valores_campo


# COMUNIDAD ANDINA
def agregar_datos_comunidad_andina(nombre, fecha_limite, hora, contacto, documento):
    data = {"expediente_id": nombre, "fecha_limite": fecha_limite, "hora": hora, "contacto": contacto,
            "documento": documento, "pagina": "https://www.comunidadandina.org/convocatorias/",
            "estado_expediente": "NoRevisado", "Nombre_pagina": "Comunidad Andina", "Fecha_revisado": "",
            "Encargado": "", "Reporte": ""}
    db.collection("crm").add(data)


def obtener_ids_comunidad_andina():
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


# FONPLATA
def agregar_datos_fonplata(prestamo, modalidad, objeto, descripcion, presupuesto, fecha_publicacion, fecha_presentacion,
                           pais):
    data = {"expediente_id": prestamo, "modalidad": modalidad, "objeto": objeto, "descripcion": descripcion,
            "presupuesto": presupuesto, "fecha_publicacion": fecha_publicacion, "pais": pais,
            "fecha_presentacion": fecha_presentacion,
            "pagina": "https://www.fonplata.org/es/adquisiciones-en-proyectos",
            "estado_expediente": "NoRevisado", "Nombre_pagina": "Fonplata", "Fecha_revisado": "", "Encargado": "",
            "Reporte": ""}
    db.collection("crm").add(data)


def obtener_ids_fonplata():
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


# NUG
def agregar_datos_NUG(titulo, fecha_limite, publicado, organismo_onu, tipo_anuncio, referencia, pais):
    data = {"expediente_id": referencia, "fecha_limite": fecha_limite, "titulo": titulo, "publicado": publicado,
            "organismo_onu": organismo_onu, "tipo_anuncio": tipo_anuncio, "pais": pais,
            "pagina": "https://www.ungm.org/Public/Notice", "estado_expediente": "NoRevisado",
            "Nombre_pagina": "Naciones Unidas Global", "Fecha_revisado": "", "Encargado": "", "Reporte": ""}
    db.collection("crm").add(data)


def obtener_ids_NUG():
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


# OEA
def agregar_datos_OEA(oficina, titulo, fecha, estado, referencia):
    data = {"expediente_id": referencia, "oficina": oficina, "titulo": titulo, "fecha": fecha, "estado": estado,
            "pagina": "https://oei.int/contrataciones", "estado_expediente": "NoRevisado", "Nombre_pagina": "OEA",
            "Fecha_revisado": "", "Encargado": "", "Reporte": ""}
    db.collection("crm").add(data)


def obtener_ids_OEA():
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
        if pagina == 'https://oei.int/contrataciones':
            valores_campo.append(expediente_id)
    return valores_campo


# PROCUREMENT
def agregar_datos_PROCUREMENT(numero_referencia, titulo, oficina, pais, proceso, fecha_hasta, fecha_publicacion):
    data = {"expediente_id": numero_referencia, "titulo": titulo, "oficina": oficina, "pais": pais, "proceso": proceso,
            "fecha_hasta": fecha_hasta, "fecha_publicacion": fecha_publicacion,
            "pagina": "https://procurement-notices.undp.org/search.cfm", "estado_expediente": "NoRevisado",
            "Nombre_pagina": "Procurement Notices", "Fecha_revisado": "", "Encargado": "",
            "Reporte": ""}
    db.collection("crm").add(data)


def obtener_ids_PROCUREMENT():
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


# PROFONANPE
def agregar_datos_profonanpe():
    data = {"expediente_id": "",
            "pagina": "https://convocatoriasprofonanpe.vform.pe/", "estado_expediente": "NoRevisado",
            "Nombre_pagina": "Profonanpe", "Fecha_revisado": "", "Encargado": "", "Reporte": ""}
    db.collection("crm").add(data)
