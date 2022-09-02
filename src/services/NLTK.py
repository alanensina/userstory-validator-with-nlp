from src.classes.Response import Response

class NLTK:
    def processarHistoria(idioma:str, historia:str):
        return Response(historia, 'NLTK', 'TESTE', True, True, True, 'TESTE', 'TESTE', 'TESTE', None)
    
    def processarCenario(idioma:str, cenario:str):
        return Response(cenario, 'NLTK', 'TESTE', True, True, True, 'TESTE', 'TESTE', 'TESTE', None)
    