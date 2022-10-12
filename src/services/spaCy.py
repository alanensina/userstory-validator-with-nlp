import spacy
from src.classes.Response import Response
from src.classes.Palavra import Palavra
from src.classes import Constantes

class SPACY:
    def processarHistoria(idioma:str, historia:str):
        return Response(historia, 'spaCy', 'TESTE', True, True, True, 'TESTE', 'TESTE', 'TESTE', None)

    
    def processarCenario(idioma:str, cenario:str):
        return Response(cenario, 'spaCy', 'TESTE', True, True, True, 'TESTE', 'TESTE', 'TESTE', None)


    def processar(texto, idioma):

        if idioma == Constantes.EN:
            nlp = spacy.load(Constantes.SPACY_EN)
            doc = nlp(texto)
            return SPACY.unificar_tagset(doc)

        elif idioma == Constantes.PTBR: 
            nlp = spacy.load(Constantes.SPACY_PT)
            doc = nlp(texto)
            return SPACY.unificar_tagset(doc)
        
        return None


    def unificar_tagset(tags):
        tagsets = []
        for token in tags:
            tagsets.append(Palavra(token.text, token.pos_, SPACY.get_classe_gramatical(token.pos_)))        
        return tagsets


    def get_classe_gramatical(tagset):
        if tagset == 'ARTIGO':
              return Constantes.ARTIGO
        else:
              return Constantes.INVALIDO