from email.mime.text import MIMEText
from yattag import Doc
import os.path
import base64
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Ejemplo de uso:
expedientes = [
    {
        'consultoria': 'Consultoría ABC',
        'lugar': 'Ciudad A',
        'tipo': 'Tipo 1',
        'codigoProceso': '12345',
        'codigoCompleto': 'ABC-12345',
        'proyecto': 'Proyecto X',
        'deadline': '01/01/2024',
        'plazo': '30 días',
        'presupuesto': '$1000',
        'objetivos': 'Objetivo principal...',
        'objetivoEspecifico': 'Objetivo específico...',
        'alcance': 'Alcance del proyecto...',
        'experiencia': '10 años',
        'encargado': 'Juan Pérez',
        'Expediente_ID': 'EXP-12345',
    },
    {
        'consultoria': 'Consultoría DEF',
        'lugar': 'Ciudad B',
        'tipo': 'Tipo 2',
        'codigoProceso': '67890',
        'codigoCompleto': 'DEF-67890',
        'proyecto': 'Proyecto Y',
        'deadline': '01/02/2024',
        'plazo': '45 días',
        'presupuesto': '$1500',
        'objetivos': 'Otro objetivo principal...',
        'objetivoEspecifico': 'Otro objetivo específico...',
        'alcance': 'Otro alcance...',
        'experiencia': '5 años',
        'encargado': 'María Rodríguez',
        'Expediente_ID': 'EXP-67890',
    },
]

SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def lambda_handler(event, context):
    service = gmail_authenticate()

    # Creamos el reporte
    html_report = create_report(expedientes)

    # Creamos el mensaje
    message = create_message('jcolombo@qanlexlfund.com', 'juanicolombo8@gmail.com', 'Reporte de Expedientes Revisados',
                             html_report, 'Reporte')

    # Enviamos el mensaje
    send_message(service, 'me', message)


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
                    if 'Expediente_ID' in expediente:
                        with tag('div', klass='expediente-id'):
                            text(expediente['Expediente_ID'])

                    # Procesamos todos los otros datos del expediente
                    for key, value in expediente.items():
                        if value is not None:  # Asegurarse de que el valor no sea None
                            if key != 'Expediente_ID':  # Evitamos mostrarlo nuevamente
                                with tag('p'):
                                    with tag('strong'):
                                        text(key.capitalize() + ': ')
                                    text(value)
                    # Botón que dirige a la URL del expediente
                    expediente_url = f"https://tuweb.com/expediente/{expediente['Expediente_ID']}"
                    with tag('a', href=expediente_url, klass='btn'):
                        text('Ver Expediente')

    return doc.getvalue()


lambda_handler(1, 2)
