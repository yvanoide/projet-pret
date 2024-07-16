from transformers import pipeline
from config.parametres import VERSIONS
from model.prompt import Prompt

def traduire(prompt:Prompt) :
    if prompt.version == VERSIONS[0] :
        translator = pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en")

    prompt.traduction = translator(prompt.atraduire)
    return(prompt)