import spacy
from src.classes.Response import Response
from src.classes.Palavra import Palavra
from src.classes import Constantes

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
            return SPACY.unificar_tagset(doc)

        elif idioma == Constantes.PTBR: 
            nlp = spacy.load(Constantes.SPACY_PT)
            doc = nlp(texto)
            return SPACY.unificar_tagset(doc)
        
        return None


    def unificar_tagset(tags):
        tagsets = []
        for token in tags:
            tagsets.append(Palavra(token.text, token.tag_, SPACY.get_classe_gramatical(token.tag_))) 

        for tagset in tagsets:
            print('--------------------------')
            print(tagset)
            print('--------------------------')
            
        return tagsets


     # Função responsável em retornar a classe gramatical conforme o tagset
    def get_classe_gramatical(tagset):
          if SPACY.verifica_artigo(tagset):
              return Constantes.ARTIGO
          elif SPACY.verifica_adjetivo(tagset):
              return Constantes.ADJETIVO
          elif SPACY.verifica_substantivo(tagset):
              return Constantes.SUBSTANTIVO
          elif SPACY.verifica_numeral(tagset):
              return Constantes.NUMERAL
          elif SPACY.verifica_pronome(tagset):
              return Constantes.PRONOME
          elif SPACY.verifica_adverbio(tagset):
              return Constantes.ADVERBIO
          elif SPACY.verifica_conjuncao(tagset):
              return Constantes.CONJUNCAO
          elif SPACY.verifica_preposicao(tagset):
              return Constantes.PREPOSICAO
          elif SPACY.verifica_interjeicao(tagset):
              return Constantes.INTERJEICAO
          elif SPACY.verifica_verbo(tagset):
              return Constantes.VERBO
          elif SPACY.verifica_verbo_aux(tagset):
              return Constantes.VERBO_AUX
          elif SPACY.verifica_participio(tagset):
              return Constantes.PARTICIPIO
          elif SPACY.verifica_denotativo(tagset):
              return Constantes.PALAVRA_DEN
          elif SPACY.verifica_moeda(tagset):
              return Constantes.MOEDA        
          else:
              return Constantes.INVALIDO
          
          
    def verifica_pronome(tagset):
        return tagset == 'PROADJ' or tagset == 'PROSUB' or tagset == 'PROPESS' or tagset == 'PRON' or tagset == 'PRO-KS' or tagset == 'PRO-KS-REL' or tagset == 'PRP' or tagset == 'PRP$' or tagset == 'WP'
    

    def verifica_numeral(tagset):
        return tagset == 'NUM' or tagset == 'CD'


    def verifica_verbo_aux(tagset):
        return tagset == 'VAUX' or tagset == 'AUX'


    def verifica_denotativo(tagset):
        return tagset == 'PDEN'


    def verifica_moeda(tagset):
        return tagset == 'CUR'


    def verifica_participio(tagset):
        return tagset == 'PCP' or tagset == 'RP'


    def verifica_interjeicao(tagset):
        return tagset == 'IN' or tagset == 'UH'
        
    
    def verifica_adverbio(tagset):
        return tagset == 'ADV' or tagset == 'ADV-KS' or tagset == 'ADV-KS-REL' or tagset == 'RB' or tagset == 'RBS' or tagset == 'RBR' or tagset == 'WRB'
    
    
    def verifica_substantivo(tagset):
        return tagset == 'N' or tagset == 'NOUN' or tagset == 'NPROP' or tagset == 'NN' or tagset == 'NNP' or tagset == 'NNS'
    
    
    def verifica_conjuncao(tagset):
        return tagset == 'KC' or tagset == 'KS' or tagset == 'CONJ' or tagset == 'CC' or tagset == 'IN' or tagset == 'SCONJ'
    
    
    def verifica_verbo(tagset):
        return tagset == 'V' or tagset == 'VERB' or tagset == 'VB' or tagset == 'VBD' or tagset == 'VBG' or tagset == 'VBN' or tagset == 'VBP' or tagset == 'VBG'or tagset == 'VBZ' or tagset == 'MD'
    
    
    def verifica_adjetivo(tagset):
        return tagset == 'ADJ' or tagset == 'JJ' or tagset == 'JJR' or tagset == 'JJS'
    
    
    def verifica_preposicao(tagset):
        return tagset == 'PREP' or tagset == 'PRP' or tagset == 'TO' or tagset == 'ADP'
    
    
    def verifica_artigo(tagset):
        return tagset == 'ART' or tagset == 'DET' or tagset == 'DT' or tagset == 'WDT'