import nltk, joblib
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from src.classes.Response import Response
from src.classes.Palavra import Palavra
from src.classes import Tagset

class NLTK:
    
    def processarHistoria(idioma:str, historia:str):
        texto_processado = NLTK.processar(historia, idioma)
        return Response(historia, 'NLTK', 'TESTE', True, True, True, 'TESTE', 'TESTE', 'TESTE', None)
    
    def processarCenario(idioma:str, cenario:str):
        texto_processado = NLTK.processar(cenario, idioma)
        return Response(cenario, 'NLTK', 'TESTE', True, True, True, 'TESTE', 'TESTE', 'TESTE', None)
    
    def tokenizar(sentenca:str, idioma:str):   
        tokens_sentencas = []
        tokens_palavras = []
             
        # Tokenização das sentenças
        if idioma == 'en':
            tokens_sentencas = sent_tokenize(sentenca)
        elif idioma == 'ptbr':
            tokens_sentencas = sent_tokenize(sentenca, language='portuguese')
        
        # Tokenização das palavras
        for token in tokens_sentencas:
            if idioma == 'en':
                tokens_palavras.extend(word_tokenize(token))
            elif idioma == 'ptbr':
                tokens_palavras.extend(word_tokenize(token, language='portuguese'))
        
        return tokens_palavras
    
    # Lematização das palavras
    def lematizar(tokens_palavras):
        lemmas = []
        wordnet_lemmatizer = WordNetLemmatizer()
        for token in tokens_palavras:
            lemma = wordnet_lemmatizer.lemmatize(token, pos='v')
            lemmas.append(lemma)
        return lemmas
    
    # Tagging dos lemas das palavras
    def tagging(lemmas, idioma:str):
        ptbr_tagger_brill = joblib.load('POS_tagger_brill.pkl')
        #ptbr_tagger_trigram = joblib.load('POS_tagger_trigram.pkl')   
        tags = []
        
        if idioma == 'en':
            tags = pos_tag(lemmas)
        elif idioma == 'ptbr':    
            tags = ptbr_tagger_brill.tag(lemmas)
            
        return tags

    # Fluxo de processamento de texto
    def processar(texto:str, idioma:str):
        tokens_palavras = NLTK.tokenizar(texto, idioma)
        lemas = NLTK.lematizar(tokens_palavras)
        pre_tags = NLTK.tagging(lemas, idioma)
        tags = NLTK.unificar_tagset(pre_tags)
        #TODO: remover depois:
        for tag in tags:
            print(tag)
        return tags
    
    def unificar_tagset(tags):
        tagsets = []
        for tupla in tags:
            palavra = tupla[0]  
            tagset = tupla[1]  
            classe = NLTK.get_classe_gramatical(tagset)
            tagsets.append(Palavra(palavra, tagset, classe))        
        return tagsets
    
    # Função responsável em retornar a classe gramatical conforme o tagset
    def get_classe_gramatical(tagset):
          if tagset == 'ART' or tagset == 'DET':
              return Tagset.ARTIGO
          elif tagset == 'ADJ':
              return Tagset.ADJETIVO
          elif tagset == 'N' or tagset == 'NOUN':
              return Tagset.SUBSTANTIVO
          elif tagset == 'NPROP':
              return Tagset.SUBSTANTIVO_P
          elif tagset == 'NUM':
              return Tagset.NUMERAL
          elif tagset == 'PROADJ':
              return Tagset.PRONOME_ADJ
          elif tagset == 'PROSUB':
              return Tagset.PRONOME_SUBS
          elif tagset == 'PROPESS':
              return Tagset.PRONOME_PESS
          elif tagset == 'PRO-KS':
              return Tagset.PRONOME_CON
          elif tagset == 'ADV':
              return Tagset.ADVERBIO
          elif tagset == 'ADV-KS':
              return Tagset.ADVERBIO_CON_SUBORD
          elif tagset == 'ADV-KS-REL':
              return Tagset.ADVERBIO_REL_SUBORD
          elif tagset == 'KC':
              return Tagset.CONJUNCAO_COORD
          elif tagset == 'KS':
              return Tagset.CONJUNCAO_COORD
          elif tagset == 'PREP':
              return Tagset.PREPOSICAO
          elif tagset == 'IN':
              return Tagset.INTERJEICAO
          elif tagset == 'V' or tagset == 'VERB':
              return Tagset.VERBO
          elif tagset == 'VAUX':
              return Tagset.VERBO_AUX
          elif tagset == 'PCP':
              return Tagset.PARTICIPIO
          elif tagset == 'PDEN':
              return Tagset.PALAVRA_DEN
          elif tagset == 'CUR':
              return Tagset.MOEDA        
          else:
              return Tagset.INVALIDO