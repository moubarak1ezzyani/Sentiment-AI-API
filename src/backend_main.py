import os
import jwt
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials # <--- NOUVEAU
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# --- CHARGEMENT ENV ---
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Variables & Sécurité
HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = os.getenv("API_URL_env")
JWT_SECRET = os.getenv("JWT_SECRET_env")
ALGO = os.getenv("algo_env") or "HS256"
SECRET_KEY_FINAL = str(JWT_SECRET) if JWT_SECRET else "secret_de_secours"

app = FastAPI()

# --- SECURITY SCHEME ---
# Cela dit à Swagger : "J'utilise des tokens Bearer, affiche le bouton Cadenas"
security = HTTPBearer()

# --- CORS ---
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# --- MODELES ---
class User(BaseModel):
    username: str
    password: str

class TextInput(BaseModel):
    text: str 

# --- ROUTES ---

@app.post("/login")
def login(user: User):
    if user.username == "admin" and user.password == "1234":
        token = jwt.encode({"sub": user.username}, SECRET_KEY_FINAL, algorithm=ALGO)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Mauvais identifiants")


@app.post("/sentiment") 
def analyze_sentiment(input: TextInput, credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Cette route est protégée. Swagger affichera un cadenas.
    """
    # 1. Récupération automatique du token via HTTPBearer
    # Plus besoin de split(" ") manuellement, FastAPI le fait pour vous.
    token_clean = credentials.credentials 
    
    # 2. Vérification du Token
    try:
        payload = jwt.decode(token_clean, SECRET_KEY_FINAL, algorithms=[ALGO])
        user_sub = payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expiré")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalide")
    except Exception as e:
        print(f"Erreur Token: {e}")
        raise HTTPException(status_code=401, detail="Erreur d'authentification")

    # 3. Appel Hugging Face
    import requests 
    try:
        response = requests.post(
            API_URL, 
            headers={"Authorization": f"Bearer {HF_TOKEN}"}, 
            json={"inputs": input.text}
        )
        response.raise_for_status()
        data_hf = response.json() 
        
        # Aplatir le résultat
        if isinstance(data_hf, list) and len(data_hf) > 0:
            first_result = data_hf[0]
            if isinstance(first_result, list):
                first_result = first_result[0]
            return {
                "sentiment": first_result.get('label'),
                "score": first_result.get('score'),
                "user": user_sub
            }
        return data_hf

    except Exception as e:
        print(f"Erreur API IA: {e}")
        raise HTTPException(status_code=503, detail="Erreur du service IA")