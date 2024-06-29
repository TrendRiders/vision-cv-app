from flask import Flask, request, render_template, redirect, url_for
import os
import base64
from PIL import Image
from io import BytesIO
from datetime import datetime
import verify_image
import time






app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/<numero>')
def index(numero):
    user_id = request.args.get('user_id')
    return render_template('index.html', user_id=numero)

@app.route('/upload', methods=['POST'])
def upload():
    # Registramos el tiempo de inicio

    

    # Calculamos el tiempo transcurrido
    user_id = request.args.get('user_id')
    resized_file_data = request.form['resized_file']
    if resized_file_data:
        # Decodificar el Data URL de la imagen comprimida
        header, encoded = resized_file_data.split(",", 1)
        data = base64.b64decode(encoded)
        
        # Guardar la imagen comprimida en el servidor
        file_path = os.path.join(UPLOAD_FOLDER, f"{user_id}_compressed_image.jpg")
        with open(file_path, 'wb') as f:
            f.write(data)
        
        timestamp = datetime.now()
        date_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        latitude = request.form.get('latitude', 'Unknown')
        longitude = request.form.get('longitude', 'Unknown')
        
        approved, score, reasons, within, marca, tbase, trequest = verify_image.verify(file_path, latitude, longitude)
        result = 'approved' if approved else 'rejected'
        

        return render_template(
            'result.html', result=result, score=score, date_time=date_time, 
            latitude=latitude, longitude=longitude, user_id=user_id, 
            approved=approved, reasons=reasons, within=within, marca=marca, tbase=tbase, trequest = trequest
        )
    else:
        return redirect(url_for('index', user_id=user_id))

@app.route('/return_to_whatsapp')
def return_to_whatsapp():
    user_id = request.args.get('user_id')
    return redirect(f'https://wa.me/51988583623')

@app.route('/retake_photo/<user_id>')
def retake_photo(user_id):
    return redirect(f'https://17db-132-191-0-32.ngrok-free.app/{user_id}')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
