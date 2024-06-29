import base64
import requests
from datetime import datetime

#OpenAI API Key
api_key = "sk-proj-YWvg1sqYhOjtC49QWSvhT3BlbkFJra5LfugJegdSK92NuGgB"

#Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


#Getting the base64 string

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}



def ask_gpt(image_link, prompt):
  inicio = datetime.now()
  base64_image1 = encode_image(image_link)

  fin1 = datetime.now()
  tiempo_transcurrido_base = fin1 - inicio


  payload = {
    "model": "gpt-4o",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": prompt,
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image1}",
            },
          }
        ],
      }
    ],
    "max_tokens": 300
  }


  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

  fin2 = datetime.now()
  tiempo_transcurrido_request = fin2 - inicio

  return response.json()['choices'][0]['message']['content'], tiempo_transcurrido_base, tiempo_transcurrido_request


