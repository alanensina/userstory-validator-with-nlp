from src.classes import Constantes
from src.services.UtilsService import utils
import spacy

class SpacyService():

    def processar(texto, idioma):

        if idioma == Constantes.EN:
            nlp = spacy.load(Constantes.SPACY_EN)
            doc = nlp(texto)
            return utils.unificar_tagset(doc, Constantes.SPACY)

        elif idioma == Constantes.PTBR: 
            nlp = spacy.load(Constantes.SPACY_PT)
            doc = nlp(texto)
            return utils.unificar_tagset(doc, Constantes.SPACY)
        
        return None 
    