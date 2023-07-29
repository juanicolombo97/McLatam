import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("clave.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def agregar_datos(id_fila, titulo, fecha, fecha_aprobacion, fecha_publicacion, url_id, costo, monto,
                  sector_proyecto, pais, link_datos, tipo_proyecto, estado_proyecto, sub_sector, fund):
    data = {"expediente_id": id_fila, "fecha_limite": fecha, "fecha_aprobacion": fecha_aprobacion,
            "fecha_publicacion": fecha_publicacion, "titulo": titulo,
            "url_id": url_id, "costo": costo, "monto": monto, "sector_proyecto": sector_proyecto, "pais": pais,
            "link_datos": link_datos, "tipo_proyecto": tipo_proyecto, "estado_proyecto": estado_proyecto,
            "sub_sector": sub_sector, "fund": fund, "pagina": "https://www.worldbank.org/en/home",
            "estado_expediente": "NoRevisado"}
    db.collection("crm").add(data)
