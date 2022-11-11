import nltk, joblib
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from src.classes import Constantes
from src.services.UtilsService import utils

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')

class NLTKService(): 
       
    def tokenizar(sentenca:str, idioma:str):   
        tokens_sentencas = []
        tokens_palavras = []
             
        # Tokenização das sentenças
        if idioma == Constantes.EN:
            tokens_sentencas = sent_tokenize(sentenca)
        elif idioma ==  Constantes.PTBR:
            tokens_sentencas = sent_tokenize(sentenca, language='portuguese')
            
        # Tokenização das palavras
        for token in tokens_sentencas:
            if idioma == Constantes.EN:
                tokens_palavras.extend(word_tokenize(token))
            elif idioma ==  Constantes.PTBR:
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
        tags = []
        
        if idioma == Constantes.EN:
            tags = pos_tag(lemmas)
        elif idioma ==  Constantes.PTBR:    
            tags = ptbr_tagger_brill.tag(lemmas)
            
        return tags
    

    # Fluxo de processamento de texto no NLTK
    def processar(texto:str, idioma:str):
        tokens_palavras = NLTKService.tokenizar(texto, idioma)
        lemas = NLTKService.lematizar(tokens_palavras)
        pre_tags = NLTKService.tagging(lemas, idioma)
        return utils.unificar_tagset(pre_tags, Constantes.NLTK)