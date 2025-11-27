import os
import requests
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Разрешаем фронтенду обращаться
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SSO_URL = "https://platform-sso.stratpro.hse.ru/realms/platform.stratpro.hse.ru/protocol/openid-connect/token"
PREDICT_URL = "https://platform.stratpro.hse.ru/pu-krgazizullina-pa-200108/nevoscan/predict"

USERNAME = os.getenv("SSO_USERNAME")
PASSWORD = os.getenv("SSO_PASSWORD")

def get_token():
    data = {
        "client_id": "end-users",
        "grant_type": "password",
        "username": USERNAME,
        "password": PASSWORD
    }
    res = requests.post(SSO_URL, data=data)
    res.raise_for_status()
    return res.json()["access_token"]

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    token = get_token()

    # Формируем inputs для твоего inference
    inputs = [{
        "name": "image",
        "datatype": "str",
        "content_type": file.content_type,
        "data": file.file.read().decode("latin1")  # можно заменить на base64
    }]

    payload = {
        "parameters": [],
        "inputs": inputs,
        "output_fields": [
            {"name": "label"},
            {"name": "prob_benign"},
            {"name": "prob_malign"}
        ],
        "model_key": "default"
    }

    res = requests.post(PREDICT_URL,
                        headers={"Authorization": f"Bearer {token}"},
                        json=payload)
    res.raise_for_status()
    return res.json()
