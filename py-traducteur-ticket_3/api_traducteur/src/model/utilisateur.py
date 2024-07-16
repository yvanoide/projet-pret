from pydantic import BaseModel

class Utilisateur(BaseModel) :
    id : int = None
    login : str
    mdp : str
    authentifie : bool = False