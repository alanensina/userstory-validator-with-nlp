from src.classes.Response import Response

class spaCy:
    def processarHistoria(idioma:str, historia:str):
        return Response(historia, 'spaCy', 'TESTE', True, True, True, 'TESTE', 'TESTE', 'TESTE', None)
    
    def processarCenario(idioma:str, cenario:str):
        return Response(cenario, 'spaCy', 'TESTE', True, True, True, 'TESTE', 'TESTE', 'TESTE', None)