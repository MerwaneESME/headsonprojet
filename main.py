from fastapi import FastAPI, HTTPException
from firebase_admin import credentials, initialize_app, storage
from google.cloud import aiplatform_v1
from datetime import datetime
import os
from dotenv import load_dotenv
import json
from typing import Dict, Any

# Chargement des variables d'environnement
load_dotenv()

app = FastAPI(title="Mini API Cloud")

# Configuration Firebase
cred = credentials.Certificate(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
firebase_app = initialize_app(cred, {
    'storageBucket': os.getenv("BUCKET_NAME")
})

# Configuration GCP pour Vertex AI
PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION", "europe-west4")
FILE_PATH = os.getenv("FILE_PATH", "data.json")

@app.get("/hello")
async def hello():
    return {"message": "Bienvenue sur notre API Cloud!"}

@app.get("/status")
async def status():
    return {"timestamp": datetime.now().isoformat()}

@app.get("/data")
async def read_data():
    try:
        bucket = storage.bucket()
        blob = bucket.blob(FILE_PATH)
        content = blob.download_as_text()
        return json.loads(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/data")
async def write_data(data: Dict[str, Any]):
    try:
        bucket = storage.bucket()
        blob = bucket.blob(FILE_PATH)
        
        # Lire les données existantes
        try:
            existing_data = json.loads(blob.download_as_text())
        except:
            existing_data = []
            
        # Ajouter les nouvelles données
        existing_data.append(data)
        
        # Écrire les données mises à jour
        blob.upload_from_string(json.dumps(existing_data, indent=2))
        return {"message": "Données ajoutées avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/joke")
async def get_joke():
    try:
        client = aiplatform_v1.PredictionServiceClient()
        # Utilisation du modèle text-bison-32k qui est plus récent et disponible
        endpoint = f"projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/text-bison-32k"
        
        instances = [
            {
                "content": "Raconte-moi une blague courte et drôle en français."
            }
        ]
        
        parameters = {
            "temperature": 0.8,
            "maxOutputTokens": 1024,
            "topP": 0.9,
            "topK": 40
        }
        
        print(f"Tentative de connexion à Vertex AI avec l'endpoint : {endpoint}")
        response = client.predict(
            endpoint=endpoint,
            instances=instances,
            parameters=parameters
        )
        
        prediction = response.predictions[0]
        return {"joke": prediction}
    except Exception as e:
        print(f"Erreur détaillée : {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/debug-env")
async def debug_env():
    return {
        "PROJECT_ID": os.getenv("PROJECT_ID"),
        "LOCATION": os.getenv("LOCATION"),
        "BUCKET_NAME": os.getenv("BUCKET_NAME"),
        "GOOGLE_APPLICATION_CREDENTIALS": os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080) 