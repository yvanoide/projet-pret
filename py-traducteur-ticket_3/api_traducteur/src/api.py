from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

from config.parametres import VERSIONS
from model.nlp import traduire
from model.prompt import Prompt
from dto.service_traducteur import Service_Traducteur as st

app = FastAPI(
    title="Appli de traduction",
    description="API de traduction",
    version="1.0.0"
)

# Modèle pour les données d'authentification
class Utilisateur(BaseModel):
    login: str
    mdp: str

# Identifiants d'utilisateur autorisés
UTILISATEUR_AUTORISE = {
    "Cleese": "Sacré Graal!"
}

@app.post("/login")
def authentifier(utilisateur: Utilisateur):
    print(f"Received login attempt from: {utilisateur.login}")
    if utilisateur.login in UTILISATEUR_AUTORISE:
        mot_de_passe_attendu = UTILISATEUR_AUTORISE[utilisateur.login]
        if utilisateur.mdp == mot_de_passe_attendu:
            return {"authentifié": True, "id": utilisateur.login}
    
    # Si l'authentification échoue, renvoyer une erreur HTTP 401
    raise HTTPException(status_code=401, detail="Nom d'utilisateur ou mot de passe incorrect")

@app.get("/versions", tags=["index"])
def versions():
    return VERSIONS

@app.post("/traductions", tags=["traduction"])
def traducteur(prompt: Prompt):
    traduire(prompt)
    st.sauvegarder_prompt(prompt)
    return prompt

@app.get("/traductions/auteur/{id}", tags=["traduction"])
def versions_par_auteur(id: int):
    return st.lister_prompts(id)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
