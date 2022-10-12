import spacy
from src.classes.Response import Response
from src.classes.Palavra import Palavra
from src.classes import Constantes
from src.services.Utils import utils

class SPACY:
    def processarHistoria(idioma:str, historia:str):
        SPACY.processar(historia, idioma)
        return Response(historia, 'spaCy', 'TESTE', True, True, True, 'TESTE', 'TESTE', 'TESTE', None)

    
    def processarCenario(idioma:str, cenario:str):
        SPACY.processar(cenario, idioma)
        return Response(cenario, 'spaCy', 'TESTE', True, True, True, 'TESTE', 'TESTE', 'TESTE', None)


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