from email.mime.text import MIMEText
from yattag import Doc
import os.path
import base64
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import FieldFilter

cred = credentials.Certificate("/Users/mickyconca/Desktop/McLatam/clave.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def obtener_expedientes_seleccionados():
    docs = (
        db.collection("crm")
        .where(filter=FieldFilter("Estado_expediente", "==", 'Enviar')).stream()
    )

    json_array = []

    for doc in docs:
        doc_dict = doc.to_dict()  # Convierte el documento a un diccionario
        json_array.append(doc_dict)  # Agrega el diccionario al array

    return json_array


# expedientes = obtener_expedientes_seleccionados()
expedientes = obtener_expedientes_seleccionados()


def lambda_handler(event, context):
    service = gmail_authenticate()

    # Creamos el reporte
    html_report = create_report(expedientes)

    # Creamos el mensaje
    message = create_message('jcolombo@qanlexlfund.com', 'concamicky@gmail.com', 'Reporte de Expedientes Revisados',
                             html_report, 'Reporte')

    # Enviamos el mensaje
    send_message(service, 'me', message)
    print("Email enviado")


def gmail_authenticate():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)


def create_message(sender, to, subject, message_text, nombre):
    message = MIMEText(message_text, 'html')

    # Le agregamos los headers
    message['to'] = to
    message['from'] = nombre + "<" + sender + ">"
    message['subject'] = subject

    # Devolvemos dragt
    raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
    return {
        'raw': raw_message.decode("utf-8")
    }


def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId='me', body=message).execute()
        return message
    except Exception as e:
        print('An error occurred: %s' % e)
        return None


def create_report(expedientes):
    """
    Crea un reporte HTML basado en una lista de expedientes.
    Cada expediente debe ser un diccionario con llaves como en initialFormValues.
    """

    doc, tag, text = Doc().tagtext()

    # Estilos para separar y resaltar el Expediente_ID
    styles = """
        .expediente {
            border: 1px solid #ddd;
            margin: 20px 0;
            padding: 15px;
            border-radius: 5px;
            background-color: #f7f7f7;
        }
        .expediente-id {
            text-align: center;
            font-weight: bold;
            font-size: 24px;
            margin-bottom: 20px;
            padding: 10px;
            background-color: #e0e0e0;
            border-radius: 5px;
        }
        .btn {
            display: inline-block;
            padding: 5px 10px;
            background-color: #FFC107;
            width: 20%;
            color: #FFFFFF;
            font-weight: bold;
            text-align: center;
            border-radius: 4px;
            text-decoration: none;
            margin: 10px auto;
            display: block;
        }
        .btn:hover {
            background-color: #E0A800;
        }
    """

    with tag('html'):
        with tag('head'):
            with tag('style'):
                doc.text(styles)
        with tag('body'):

            for expediente in expedientes:
                with tag('div', klass='expediente'):
                    # Destacamos el dato de Expediente_ID
                    if 'Titulo' in expediente:
                        with tag('div', klass='expediente-id'):
                            text(expediente['Titulo'])

                    # Procesamos todos los otros datos del expediente
                    for key, value in expediente.items():
                        if value is not None and key not in ['Fecha_revisado', 'FechaRevisado', 'Reporte',
                                                             'Estado_expediente',
                                                             'Expediente_id',
                                                             'Titulo']:  # Asegurarse de que el valor no sea None
                            # Formateamos el nombre del campo si es 'FechaPublicacion'
                            display_key = 'Fecha Publicación' if key == 'FechaPublicacion' else key
                            with tag('p'):
                                with tag('strong'):
                                    text(display_key.capitalize() + ': ')
                                text(value)

    return doc.getvalue()


lambda_handler(1, 2)
