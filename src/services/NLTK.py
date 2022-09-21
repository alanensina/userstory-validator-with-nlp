import nltk, joblib
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from src.classes.Response import Response
from nltk.tokenize import word_tokenize, sent_tokenize

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
        else:
            return 'Idioma inválido'
        
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
        tags = NLTK.tagging(lemas, idioma)
        print(tags)
        return tags    