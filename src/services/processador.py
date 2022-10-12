from src.services.NLTK import NLTK
from src.services.SPACY import SPACY

from src.classes.Response import Response

class Processador():
    
    def __init__(self):
        pass    
    
    def processar(self, payload, type):
        
        response = []
        
        #TODO: descomentar as linhas do spacy quando começar a implementar.
        for p in payload:
            idioma = p.get('idioma')
            
            if type == 'historia':
                historia = p.get('historia')
                response.append(NLTK.processarHistoria(idioma, historia))
                response.append(SPACY.processarHistoria(idioma, historia))
            elif type == 'cenario':
                cenario = p.get('cenario')
                response.append(NLTK.processarCenario(idioma, cenario))
                #response.append(SPACY.processarCenario(idioma, cenario))
            else:
                return Response(None, None, None, False, False, False, None, None, None, 'Tipo inválido')
                
        return response

processador = Processador()