from flask import Flask, request, jsonify
from openai import OpenAI
import openai
import os
import time
from pymongo import MongoClient, ASCENDING
from datetime import datetime, timedelta
import base64
import requests

#CREDENCIALES
openai.api_key = 'sk-proj-YWvg1sqYhOjtC49QWSvhT3BlbkFJra5LfugJegdSK92NuGgB'
assistant_id = 'asst_mLivId9Q6vNjUm8cuWHs2HxB'
client = OpenAI(api_key='sk-proj-YWvg1sqYhOjtC49QWSvhT3BlbkFJra5LfugJegdSK92NuGgB')


app = Flask(__name__)

mongo_user = 'Molitalia'
mongo_pwd = 'kg6Ui75GhtdHTESy45ygKUgo78IghTY54s'
server_ip = '34.125.134.86:27017'
auth_db = 'admin'
clientm = MongoClient('mongodb://{}:{}@{}/?authSource={}'.format(mongo_user,mongo_pwd,server_ip,auth_db))



def format_image(filename):
    with open(filename, 'rb') as file:
        response = client.files.create(
            file = file,
            purpose = 'vision'
        )
        return response.id

def send_message(thread_id, image_link):

    image_file = format_image(image_link)


    thread_message = client.beta.threads.messages.create(
    thread_id,
    role="user",
    content=[
        
        {
            "type":"image_file",
            "image_file": {
                "file_id": image_file
            }

        }

    ]
    )
        
    run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id
    )


    run1 = client.beta.threads.runs.retrieve(
    thread_id = thread_id,
    run_id = run.id
    )

    while(run1.status !='completed'):
        time.sleep(0.5)
        run1 = client.beta.threads.runs.retrieve(
        thread_id = thread_id,
        run_id = run.id
        )

    if run1.status=='completed':
        thread_messages = client.beta.threads.messages.list(thread_id)
        print(thread_id)
        return thread_messages.data[0]




def get_message(image_link, number):
    content = image_link
    client_id = number
    db = clientm['moli-codigos']
    threads_collection = db['threads_mercados']

    now = datetime.utcnow()

    thread = threads_collection.find_one({'client_id': client_id})

    if thread:
        print('ENCONTRO THREAD')
        last_updated = thread['last_updated']

        #todavia esta dentro de la hora se actualiza el tiempo
        if now - last_updated <= timedelta(hours=1):
            threads_collection.update_one(
            {'client_id': client_id},
            {'$set': {'last_updated': now}},
            upsert=True)
            thread_openai = thread['thread']
            print("sigue dentro de la hora", thread_openai)
        
        #si esta fuera de la hora se crea nuevo thread
        else:
            thread_openai = client.beta.threads.create().id
            threads_collection.update_one(
                {'client_id': client_id},
                {'$set': {'thread': thread_openai, 'last_updated': now}},
                upsert=True
            )
            print("se creó nuevo thread timeout", thread_openai)

    else:
        thread_openai = client.beta.threads.create().id
        threads_collection.update_one(
            {'client_id': client_id},
            {'$set': {'thread': thread_openai, 'last_updated': now}},
            upsert=True
        )
        print("se creó nuevo thread, nuevo ", thread_openai)



    response = send_message(thread_openai, content)

   
    return response



image = "images/1717710106879.jpg"


print(get_message(image, "999"))