from yattag import Doc

def create_report(expedientes):
    """
    Crea un reporte HTML basado en una lista de expedientes.
    Cada expediente debe ser un diccionario con llaves como en initialFormValues.
    """
    
    doc, tag, text = Doc().tagtext()
    
    with tag('html'):
        with tag('body'):
            with tag('h1'):
                text('Reporte de Expedientes')
                
            for expediente in expedientes:
                with tag('div', klass='expediente'):
                    for key, value in expediente.items():
                        with tag('p'):
                            with tag('strong'):
                                text(key + ': ')
                            text(value)

    return doc.getvalue()


# Ejemplo de uso:
expedientes = [
    {
        'consultoria': 'Ejemplo1',
        'lugar': 'Lugar1',
        # ... (rellena con otros campos)
        'encargado': 'Encargado1',
    },
    {
        'consultoria': 'Ejemplo2',
        'lugar': 'Lugar2',
        # ... (rellena con otros campos)
        'encargado': 'Encargado2',
    },
    # ... (añade más expedientes si lo deseas)
]

html_report = create_report(expedientes)
print(html_report)
