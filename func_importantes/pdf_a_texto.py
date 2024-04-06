# Imports
import pytesseract
import os
from PIL import Image
from pdf2image import convert_from_path
import os
import spacy
import sys

# Funcion que recibe un path a un pdf y devuelve el texto del mismo
def pdf_a_texto(filename):

    # Verificar la extensión del archivo
    ext = os.path.splitext(filename)[1]
    text = ""
    
    # Si es una imagen
    if ext in ['.jpg', '.jpeg', '.png', '.bmp']:
        # Abrir la imagen
        img = Image.open(filename)
        # Convertir la imagen a texto con pytesseract
        text = pytesseract.image_to_string(img, lang='eng')
        
    # Si es un PDF
    elif ext == '.pdf':
        # Convertir el PDF a una lista de imágenes
        pages = convert_from_path(filename)
        for page in pages:
            # Convertir cada página del PDF a texto con pytesseract
            text += pytesseract.image_to_string(page, lang='eng')
            
    # Retornar el texto obtenido
    return text
 
# Funcion que recibe texto y trata de devolver los datos del CV, y devuelve una lista de habilidades
def datos_cv(texto):
    nlp = spacy.load('es_core_news_sm')
    print('Comenzando el procesamiento del texto...')

    # Procesamiento del texto con spaCy
    doc = nlp(texto)

    # Buscar el nombre del solicitante
    nombre = None
    for ent in doc.ents:
        if ent.label_ == 'PER':
            nombre = ent.text
            break

    # Buscar la lista de habilidades
    habilidades = []
    for token in doc:
        if token.text.lower() in ['habilidades', 'competencias', 'habilidades:', 'competencias:']:
            for child in token.children:
                habilidades.append(child.text)

    return habilidades

def main(parametros):
    

    # Si el parametro es lecturacv leemos el pdf de la carpeta pdfs_ejemplos
    if parametros[0] == 'lecturacv':
        # Obtenemos los archivos pdf de la carpeta pdfs_ejemplos
        pdfs = os.listdir('pdfs_ejemplos')

        # Iteramos sobre los archivos pdf
        for pdf in pdfs:

            print(f'Archivo: {pdf}')

            # Obtenemos el texto del pdf
            texto = pdf_a_texto('pdfs_ejemplos/' + pdf)

            # Imprimimos el texto
            datos_cv(texto)




# Ejecutar la función main, y pasa los parametros que recibe
if __name__ == '__main__':
    main(sys.argv[1:])

