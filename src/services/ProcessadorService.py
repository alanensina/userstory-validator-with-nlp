from src.services.NLTKService import NLTKService
from src.services.SpacyService import SpacyService

class ProcessadorService():
    
    def __init__(self):
        pass    
    
    def processar(self, payload, type):
        
        response = []
        
        for p in payload:
            idioma = p.get('idioma')
            
            if type == 'historia':
                historia = p.get('historia')
                response.append(NLTKService.processarHistoria(idioma, historia))
                response.append(SpacyService.processarHistoria(idioma, historia))
            elif type == 'cenario':
                cenario = p.get('cenario')
                response.append(NLTKService.processarCenario(idioma, cenario))
                response.append(SpacyService.processarCenario(idioma, cenario))
                
        return response

processador = ProcessadorService()