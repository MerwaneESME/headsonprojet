# headsonprojet
# Mini API Cloud

Cette API FastAPI démontre l'intégration avec Google Cloud Platform, incluant Cloud Storage et Vertex AI.

## Fonctionnalités

- Endpoint de bienvenue (`/hello`)
- Statut du serveur (`/status`)
- Lecture/écriture de données dans Google Cloud Storage (`/data`)
- Génération de blagues avec Vertex AI (`/joke`)

## Prérequis

- Python 3.9+
- Compte Google Cloud Platform (GCP)
- Google Cloud SDK
- Docker (optionnel, pour le déploiement conteneurisé)

## Configuration de Google Cloud

1. Installez le [SDK Google Cloud](https://cloud.google.com/sdk/docs/install)

2. Connectez-vous à votre compte Google Cloud :
```bash
gcloud auth login
```

3. Configurez votre projet :
```bash
gcloud config set project VOTRE_PROJECT_ID
```

4. Activez les APIs nécessaires :
```bash
gcloud services enable run.googleapis.com storage.googleapis.com aiplatform.googleapis.com
```

5. Créez un compte de service et téléchargez les credentials :
```bash
# Créer le compte de service
gcloud iam service-accounts create mini-api-sa --display-name="Mini API Service Account"

# Télécharger les credentials
gcloud iam service-accounts keys create credentials.json --iam-account=mini-api-sa@VOTRE_PROJECT_ID.iam.gserviceaccount.com
```

6. Créez un bucket Cloud Storage :
```bash
gsutil mb -l us-central1 gs://VOTRE_BUCKET_NAME
```

## Configuration du Projet

1. Clonez le projet et accédez au répertoire :
```bash
git clone [URL_DU_REPO]
cd [NOM_DU_REPO]
```

2. Créez un fichier `.env` avec les variables suivantes :
```plaintext
BUCKET_NAME=VOTRE_BUCKET_NAME
PROJECT_ID=VOTRE_PROJECT_ID
LOCATION=europe-west4
GOOGLE_APPLICATION_CREDENTIALS=./credentials.json
```

## Installation locale

1. Créez et activez un environnement virtuel Python :
```bash
# Création
python -m venv venv

# Activation
## Pour Windows :
venv\Scripts\activate
## Pour Linux/Mac :
source venv/bin/activate
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Vérifiez que le fichier `credentials.json` est bien présent à la racine du projet

4. Lancez l'API :
```bash
uvicorn main:app --reload --port 8000
```

5. Accédez à l'application :
- Interface Swagger : http://localhost:8000/docs
- API directement : http://localhost:8000

## Résolution des problèmes courants

1. **Erreur d'authentification GCP** :
   - Vérifiez que le fichier `credentials.json` est présent
   - Vérifiez que le chemin dans `GOOGLE_APPLICATION_CREDENTIALS` est correct

2. **Erreur de connexion au bucket** :
   - Vérifiez que le nom du bucket dans `.env` est correct
   - Vérifiez que le bucket a été créé dans GCP

3. **L'API ne démarre pas** :
   - Vérifiez que toutes les dépendances sont installées
   - Vérifiez que le port 8000 n'est pas déjà utilisé

## Déploiement avec Docker (Optionnel)

1. Construisez l'image :
```bash
docker build -t mini-api-cloud .
```

2. Lancez le conteneur :
```bash
docker run -p 8000:8000 --env-file .env mini-api-cloud
```

## Documentation API

La documentation interactive Swagger est disponible à l'URL : http://localhost:8000/docs

## Endpoints disponibles

- `GET /hello` : Message de bienvenue
- `GET /status` : Date/heure du serveur
- `GET /data` : Lecture des données depuis GCS
- `POST /data` : Ajout de données dans GCS
- `GET /joke` : ⚠️ **EN MAINTENANCE** - Cet endpoint n'est actuellement pas fonctionnel malgré plusieurs tentatives de résolution. Nous avons essayé de résoudre les problèmes d'intégration avec Vertex AI (vérification des APIs, permissions, configurations) mais n'avons pas réussi à le faire fonctionner correctement. Les autres endpoints restent pleinement opérationnels. 
