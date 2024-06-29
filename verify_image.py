import cv2
from shapely.geometry import Point, Polygon
import vision_request
from datetime import datetime
from flask import jsonify
import json

def verify(image_path, latitud, longitud):

    score = None
    approved = True
    marca = None
    tbase = None
    trequest = None
    try:

        # Registramos el tiempo de inicio
        inicio = datetime.now()
        
        score, tbase, trequest = vision_request.ask_gpt(image_path, "Identifica la marca del objeto que aparece en la foto, si no puedes identificar el objeto, devuelve '-', además da un score de que tan bien se puede identificar la marca (0-1). Entrega el resultado en el siguiente formato de ejemplo: {\"marca\":\"nombre_marca\", \"score\": 0,7}")
        score = json.loads(score)
        print('MARCA', score)
        fin = datetime.now()
        marca = score['marca']
        score = score['score']

        tiempo_transcurrido = fin - inicio
        print("Tiempo total solamente request Openai:", tiempo_transcurrido)
    except Exception as e:
        score = 0

    #try for every polygon
    coordenadas_cerca = [(-12.053844, -77.105319),(-12.053796, -77.100357),(-12.057627, -77.104079),(-12.057141, -77.100056), (-12.053599, -77.098227), (-12.057595, -77.098015)]
    poligono_cerca = Polygon(coordenadas_cerca)
    punto = Point(latitud, longitud)
    within = poligono_cerca.contains(punto)


    reasons = []
    
    if score < 0.5:
        approved = False
        reasons.append("Photo does not show an object with a visible brand name.")
    # if not within:
    #     approved = False
    #     reasons.append("Photo not in geo-polygon")

    return approved, score, reasons, within, marca, tbase, trequest
    

    
