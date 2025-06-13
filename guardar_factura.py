from flask import Flask, request, jsonify
from docx import Document
from docx2pdf import convert
import os
import tempfile
from datetime import datetime

app = Flask(__name__)

@app.route('/guardar_pdf', methods=['POST'])
def guardar_pdf():
    data = request.json

    # Ruta a la plantilla .docx
    plantilla_path = 'plantilla_factura.docx'

    # Cargar la plantilla
    doc = Document(plantilla_path)

    # Reemplazar los campos en el documento
    for p in doc.paragraphs:
        for key, value in data.items():
            placeholder = f'{{{{{key}}}}}'  # Ej: {{numero_factura}}
            if placeholder in p.text:
                p.text = p.text.replace(placeholder, value)

    # Crear un archivo temporal para guardar el .docx
    temp_dir = tempfile.mkdtemp()
    temp_docx = os.path.join(temp_dir, 'factura.docx')
    doc.save(temp_docx)

    # Convertir a PDF
    escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
    pdf_name = f"factura_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    salida_pdf = os.path.join(escritorio, pdf_name)
    convert(temp_docx, salida_pdf)

    return jsonify({'message': f'Factura guardada en {salida_pdf}'})

if __name__ == '__main__':
    app.run(debug=True)