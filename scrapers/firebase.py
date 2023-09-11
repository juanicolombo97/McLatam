import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import FieldFilter

cred = credentials.Certificate("/Users/mickyconca/Desktop/McLatam/scrapers/clave.json")
firebase_admin.initialize_app(cred)

# Obtén una referencia a la instancia de Firestore
db = firestore.client()


def obtener_expediente(expediente_id):
    docs = (
        db.collection("crm")
        .where(filter=FieldFilter("Expediente_id", "==", expediente_id)).stream()
    )

    for doc in docs:
        print(f"{doc.id} => {doc.to_dict()}")
        return 1
    return 0


def delete_all_documents():
    # Obtengo los documentos
    docs = db.collection("crm").stream()
    # Elimina cada documento uno por uno
    for documento in docs:
        documento.reference.delete()
        print("eliminado")

# delete_all_documents()

# BANCO MUNDIAL
def agregar_datos_banco_mundial(expediente_id, descripcion, pais, titulo, tipo_noticia, idioma, fecha):
    data = {"Expediente_id": expediente_id, "descripcion": descripcion, "pais": pais,
            "Titulo": titulo, "tipo_noticia": tipo_noticia, "idioma": idioma, "fecha": fecha,
            "Documento": "https://projects.worldbank.org/en/projects-operations/procurement?lang=en&qterm=&showrecent=true&srce=notices",
            "Estado_expediente": "NoRevisado", "Pagina": "Banco Mundial", "Fecha_revisado": "", "Encargado": "",
            "Reporte": ""}
    db.collection("crm").add(data)


def obtener_ids_banco_mundial():
    # Ejecuta la consulta para obtener todos los documentos de la colección
    documentos = db.collection("crm").get()

    # Crea una lista para almacenar los valores del campo
    valores_campo = []

    # Itera sobre los documentos y extrae el valor del campo deseado
    for documento in documentos:
        expediente_id = documento.get("Expediente_id")
        pagina = documento.get("pagina")
        if pagina == 'https://projects.worldbank.org/en/projects-operations/procurement?lang=en&qterm=&showrecent=true&srce=notices':
            valores_campo.append(expediente_id)
    return valores_campo


# COMUNIDAD ANDINA
def agregar_datos_comunidad_andina(nombre, fecha_limite, hora, contacto, documento):
    data = {"Expediente_id": nombre, "fecha_limite": fecha_limite, "hora": hora, "contacto": contacto,
            "Documento": documento,
            "Estado_expediente": "NoRevisado", "Pagina": "Comunidad Andina", "Fecha_revisado": "",
            "Encargado": "", "Reporte": ""}
    db.collection("crm").add(data)


def obtener_ids_comunidad_andina():
    # Ejecuta la consulta para obtener todos los documentos de la colección
    documentos = db.collection("crm").get()

    # Crea una lista para almacenar los valores del campo
    valores_campo = []

    # Itera sobre los documentos y extrae el valor del campo deseado
    for documento in documentos:
        expediente_id = documento.get("Expediente_id")
        pagina = documento.get("pagina")
        if pagina == 'https://www.comunidadandina.org/convocatorias/':
            valores_campo.append(expediente_id)
    return valores_campo


# FONPLATA
def agregar_datos_fonplata(prestamo, modalidad, objeto, descripcion, presupuesto, fecha_publicacion, fecha_presentacion,
                           pais):
    data = {"Expediente_id": prestamo, "modalidad": modalidad, "objeto": objeto, "descripcion": descripcion,
            "presupuesto": presupuesto, "fecha_publicacion": fecha_publicacion, "pais": pais,
            "fecha_presentacion": fecha_presentacion,
            "Estado_expediente": "NoRevisado", "Pagina": "Fonplata", "Fecha_revisado": "", "Encargado": "",
            "Reporte": "", "Documento": "https://www.fonplata.org/es/adquisiciones-en-proyectos"}
    db.collection("crm").add(data)


def obtener_ids_fonplata():
    # Ejecuta la consulta para obtener todos los documentos de la colección
    documentos = db.collection("crm").get()

    # Crea una lista para almacenar los valores del campo
    valores_campo = []

    # Itera sobre los documentos y extrae el valor del campo deseado
    for documento in documentos:
        expediente_id = documento.get("Expediente_id")
        pagina = documento.get("pagina")
        if pagina == 'https://www.fonplata.org/es/adquisiciones-en-proyectos':
            valores_campo.append(expediente_id)
    return valores_campo


# NUG
def agregar_datos_NUG(titulo, fecha_limite, publicado, organismo_onu, tipo_anuncio, referencia, pais):
    data = {"Expediente_id": referencia, "fecha_limite": fecha_limite, "Titulo": titulo, "publicado": publicado,
            "organismo_onu": organismo_onu, "tipo_anuncio": tipo_anuncio, "pais": pais,
            "Documento": "https://www.ungm.org/Public/Notice", "Estado_expediente": "NoRevisado",
            "Pagina": "Naciones Unidas Global", "Fecha_revisado": "", "Encargado": "", "Reporte": ""}
    db.collection("crm").add(data)


def obtener_ids_NUG():
    # Ejecuta la consulta para obtener todos los documentos de la colección
    documentos = db.collection("crm").get()

    # Crea una lista para almacenar los valores del campo
    valores_campo = []

    # Itera sobre los documentos y extrae el valor del campo deseado
    for documento in documentos:
        expediente_id = documento.get("Expediente_id")
        pagina = documento.get("pagina")
        if pagina == 'https://www.ungm.org/Public/Notice':
            valores_campo.append(expediente_id)
    return valores_campo


# OEA
def agregar_datos_OEA(oficina, titulo, fecha, estado, referencia):
    data = {"Expediente_id": referencia, "oficina": oficina, "Titulo": titulo, "fecha": fecha, "estado": estado,
            "Documento": "https://oei.int/contrataciones", "Estado_expediente": "NoRevisado", "Pagina": "OEA",
            "Fecha_revisado": "", "Encargado": "", "Reporte": ""}
    db.collection("crm").add(data)


def obtener_ids_OEA():
    # Ejecuta la consulta para obtener todos los documentos de la colección
    documentos = db.collection("crm").get()

    # Crea una lista para almacenar los valores del campo
    valores_campo = []

    # Itera sobre los documentos y extrae el valor del campo deseado
    for documento in documentos:
        expediente_id = documento.get("Expediente_id")
        pagina = documento.get("pagina")
        if pagina == 'https://oei.int/contrataciones':
            valores_campo.append(expediente_id)
    return valores_campo


# PROCUREMENT
def agregar_datos_PROCUREMENT(numero_referencia, titulo, oficina, pais, proceso, fecha_hasta, fecha_publicacion):
    data = {"Expediente_id": numero_referencia, "Titulo": titulo, "oficina": oficina, "pais": pais, "proceso": proceso,
            "fecha_hasta": fecha_hasta, "fecha_publicacion": fecha_publicacion,
            "Documento": "https://procurement-notices.undp.org/search.cfm", "Estado_expediente": "NoRevisado",
            "Pagina": "Procurement Notices", "Fecha_revisado": "", "Encargado": "",
            "Reporte": ""}
    db.collection("crm").add(data)


def obtener_ids_PROCUREMENT():
    # Ejecuta la consulta para obtener todos los documentos de la colección
    documentos = db.collection("crm").get()

    # Crea una lista para almacenar los valores del campo
    valores_campo = []

    # Itera sobre los documentos y extrae el valor del campo deseado
    for documento in documentos:
        expediente_id = documento.get("Expediente_id")
        pagina = documento.get("pagina")
        if pagina == 'https://procurement-notices.undp.org/search.cfm':
            valores_campo.append(expediente_id)
    return valores_campo


# PROFONANPE
def agregar_datos_profonanpe():
    data = {"Expediente_id": "",
            "Documento": "https://convocatoriasprofonanpe.vform.pe/", "Estado_expediente": "NoRevisado",
            "Pagina": "Profonanpe", "Fecha_revisado": "", "Encargado": "", "Reporte": ""}
    db.collection("crm").add(data)


# BID
def agregar_datos_BID(id_fila, titulo, fecha, fecha_aprobacion, fecha_publicacion, url_id, costo, monto,
                      sector_proyecto, pais, link_datos, tipo_proyecto, estado_proyecto, sub_sector, fund):
    data = {"Expediente_id": id_fila, "fecha_limite": fecha, "fecha_aprobacion": fecha_aprobacion,
            "fecha_publicacion": fecha_publicacion, "Titulo": titulo,
            "url_id": url_id, "costo": costo, "monto": monto, "sector_proyecto": sector_proyecto, "pais": pais,
            "link_datos": link_datos, "tipo_proyecto": tipo_proyecto, "estado_proyecto": estado_proyecto,
            "sub_sector": sub_sector, "fund": fund, "Documento": "https://www.worldbank.org/en/home",
            "Estado_expediente": "NoRevisado", "Pagina": "BID", "Fecha_revisado": "", "Encargado": "",
            "Reporte": ""}
    db.collection("crm").add(data)
