"""
Procesador Automático de PDFs

Este script automatiza el proceso de extracción de texto de archivos PDF,
limpieza del texto extraído y organización de los archivos resultantes.

Funcionalidad:
1. Busca todos los archivos PDF en el directorio actual.
2. Para cada PDF encontrado:
   a. Extrae el texto completo.
   b. Limpia el texto extraído (elimina números de página, une palabras divididas, etc.).
   c. Guarda el texto limpio como un archivo TXT en la carpeta introducida.
   d. Mueve el archivo PDF original a la carpeta "__PDFs".

Requisitos:
- Python 3.x
- Bibliotecas: PyPDF2, tqdm
  (Instalar con: py -m pip install PyPDF2 tqdm)

Notas:
- Los acentos se eliminan de los nombres de archivo para evitar problemas de compatibilidad.
- Si las carpetas no existen, se crearán automáticamente.

Uso:
Ejecute el script en el directorio que contiene los archivos PDF que desea procesar.
`py nombre_del_script.py`

Autor: Yago Mendoza Juan
Fecha: 05/09/2042
"""

import os
import glob
import re
import PyPDF2
from tqdm import tqdm
import shutil
import unicodedata

def list_pdf_files():
    return glob.glob('*.pdf')

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in tqdm(reader.pages, desc="Extrayendo texto", unit="página"):
            text += page.extract_text() + " "
    return text

def clean_text(text):
    text = re.sub(r'\s+\d+\s+', ' ', text)
    text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
    text = re.sub(r'(?<=[a-zá-úñ])\s*\n\s*(?=[a-zá-úñ])', ' ', text, flags=re.IGNORECASE)
    text = re.sub(r'(\.\s*)\n+(\s*[A-ZÁÉÍÓÚÑ])', r'\1\n\n\2', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'([.!?])\s+', r'\1\n\n', text)
    return text.strip()

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Se ha creado el directorio: {directory}")

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def move_pdf_to_folder(pdf_path, destination_folder):
    ensure_directory_exists(destination_folder)
    base_name = os.path.basename(pdf_path)
    name_without_extension = os.path.splitext(base_name)[0]
    name_without_accents = remove_accents(name_without_extension)
    new_name = f"{name_without_accents}.pdf"
    destination_path = os.path.join(destination_folder, new_name)
    shutil.move(pdf_path, destination_path)
    print(f"PDF movido a: {destination_path}")

def process_pdf(pdf_path, output_folder):
    print(f"Procesando {pdf_path}...")
    
    text = extract_text_from_pdf(pdf_path)
    
    print("Limpiando el texto...")
    text = clean_text(text)
    
    ensure_directory_exists(output_folder)
    
    base_name = os.path.basename(pdf_path)
    name_without_extension = os.path.splitext(base_name)[0]
    name_without_accents = remove_accents(name_without_extension)
    output_name = f"{name_without_accents}.txt"
    
    output_path = os.path.join(output_folder, output_name)
    print(f"Guardando el resultado en {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)
    
    print(f"Texto extraído y guardado en {output_path}")
    
    move_pdf_to_folder(pdf_path, "__PDFs")

def main():
    output_folder = input('Introduce una carpeta para guardar el/los TXT resultantes ("books" by default): ') or "books"
    pdf_files = list_pdf_files()
    if not pdf_files:
        print("No se encontraron archivos PDF en el directorio actual.")
        return
    
    for pdf_file in pdf_files:
        process_pdf(pdf_file, output_folder)

if __name__ == "__main__":
    main()