from src.services.NLTK import NLTK
from src.services.spaCy import spaCy

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
                #response.append(spaCy.processarHistoria(idioma, historia))
            elif type == 'cenario':
                cenario = p.get('cenario')
                response.append(NLTK.processarCenario(idioma, cenario))
               #response.append(spaCy.processarCenario(idioma, cenario))
            else:
                return Response(None, None, None, False, False, False, None, None, None, 'Tipo inválido')
                
        return response

processador = Processador()