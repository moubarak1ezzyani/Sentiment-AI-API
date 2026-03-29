# 🧠 Sentiment-AI-API

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/Framework-FastAPI-009688)
![Hugging Face](https://img.shields.io/badge/AI-BERT%20Model-yellow)
![Security](https://img.shields.io/badge/Auth-JWT-red)

## 🔗 Lien vers le Frontend
Ce backend fonctionne de pair avec l'interface utilisateur disponible ici :  
👉 **[Sentiment-SaaS-Dashboard](https://github.com/moubarak1ezzyani/Application-d-Analyse-de-Sentiment---Front-End.git)**

## 📄 Contexte
Ce microservice est le moteur d'intelligence de notre SaaS d'analyse de sentiment. Il sécurise l'accès aux ressources IA via des tokens JWT et fait l'intermédiaire avec l'API d'inférence de **Hugging Face**.

Le modèle utilisé est `nlptown/bert-base-multilingual-uncased-sentiment`, capable de noter un texte de 1 à 5 étoiles (multilingue).

## ⚙️ Architecture Technique
1. **Sécurité** : Validation des tokens JWT via `PyJWT` et `HTTPBearer`.
2. **API Gateway** : FastAPI gère les requêtes REST et les CORS (pour autoriser le frontend).
3. **IA Externe** : Les textes sont envoyés à Hugging Face, et la réponse est normalisée avant d'être renvoyée au client.

## 📂 Structure du Projet
```bash
├── backend_main.py      # Point d'entrée de l'API (Routes & Logique)
├── Test_File.py         # Script de vérification des modules
├── requirements.txt     # Dépendances (fastapi, pyjwt, requests...)
└── .env                 # Variables d'environnement (Clés API, Secrets)

```

## 🚀 Installation et Lancement

### 1. Pré-requis

Cloner le dépôt et installer les dépendances :

```bash
pip install -r requirements.txt

```

### 2. Configuration (.env)

Créez un fichier `.env` à la racine :

```env
HF_TOKEN=votre_token_hugging_face_ici
API_URL_env=[https://api-inference.huggingface.co/models/nlptown/bert-base-multilingual-uncased-sentiment](https://api-inference.huggingface.co/models/nlptown/bert-base-multilingual-uncased-sentiment)
JWT_SECRET_env=votre_secret_tres_complique
algo_env=HS256

```

### 3. Démarrer le Serveur

```bash
uvicorn backend_main:app --reload

```

L'API sera accessible sur `http://127.0.0.1:8000`.

## 📡 Documentation API

### 🔐 Authentification (`POST /login`)

Permet de récupérer un token d'accès.

* **Body** : `{"username": "admin", "password": "password"}`
* **Response** : `{"token": "eyJhbGciOiJIUzI1..."}`

### 🧠 Prédiction (`POST /predict`)

*Route protégée (Header: Authorization: Bearer <token>)*

* **Body** : `{"text": "J'adore ce service, c'est génial !"}`
* **Response** :

```json
{
  "sentiment": "5 stars",
  "score": 0.95
}

```

## ✅ Tests

Un script est inclus pour vérifier que tous les modules sont bien chargés :

```bash
python Test_File.py

```

