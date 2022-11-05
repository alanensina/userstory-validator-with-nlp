import nltk, joblib, timeit
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from src.classes.ResponseHistoria import ResponseHistoria
from src.classes.ResponseCenario import ResponseCenario
from src.classes import Constantes
from src.services.UtilsService import utils

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')

class NLTKService():
    
    def processarHistoria(idioma:str, historia:str):
        start = timeit.default_timer()
        finalidade = None
        erros = None

        sentencas = utils.separar_sentencas_historia(historia)
        
        sentencas_processadas = []
        
        if len(sentencas) > 1 and not utils.verifica_erro_separacao(sentencas):
            x = 0

            while x < len(sentencas):
                sentencas_processadas.append(NLTKService.processar(sentencas[x], idioma))
                x = x + 1

            tags = []
            for sp in sentencas_processadas:
                for s in sp:
                    tags.append(s.retorna_estrutura())

            bem_formada = utils.verifica_C1_historia(sentencas_processadas)
            atomica = utils.verifica_C2_historia(sentencas_processadas)
            minima = utils.verifica_C3_historia(sentencas_processadas, bem_formada)
            ator = utils.extrair_ator(sentencas_processadas[0])    
            acao = utils.extrair_acao(sentencas_processadas[1])

            if len(sentencas) > 2:      
                finalidade = utils.extrair_finalidade(sentencas_processadas[2])  
                erros = utils.verifica_erros_historia(bem_formada, atomica, minima, utils.valida_ator_historia(sentencas_processadas[0]), utils.valida_acao_historia(sentencas_processadas[1]), utils.valida_finalidade_historia(sentencas_processadas[2]))
            else:
                erros = utils.verifica_erros_historia(bem_formada, atomica, minima, utils.valida_ator_historia(sentencas_processadas[0]), utils.valida_acao_historia(sentencas_processadas[1]), None)
                
            end = timeit.default_timer()  
            tempo = utils.formatar_tempo(start, end)

            if erros == None:
                return ResponseHistoria(historia, Constantes.NLTK, tempo, bem_formada, atomica, minima, ator, acao, finalidade, tags, erros)
            else:
                return ResponseHistoria(historia, Constantes.NLTK, tempo, bem_formada, atomica, minima, None, None, None, tags, erros)
        else:
            end = timeit.default_timer()  
            tempo = utils.formatar_tempo(start, end)
            return utils.retorna_erro_historia(historia, Constantes.NLTK, sentencas, tempo)  
           
        
    def processarCenario(idioma:str, cenario:str):
        start = timeit.default_timer()

        sentencas = utils.separar_sentencas_cenario(cenario)
        
        sentencas_processadas = []

        if len(sentencas) > 1 and not utils.verifica_erro_separacao(sentencas):
            x = 0

            while x < len(sentencas):
                sentencas_processadas.append(NLTKService.processar(sentencas[x], idioma))
                x = x + 1

            tags = []
            for sp in sentencas_processadas:
                for s in sp:
                    tags.append(s.retorna_estrutura())
        
            bem_formada = utils.verifica_C1_cenario(sentencas_processadas)
            atomica = utils.verifica_C2_cenario(sentencas_processadas)
            minima = utils.verifica_C3_cenario(sentencas_processadas, bem_formada)

            precondicao = utils.extrair_preCondicao(sentencas_processadas[0])    
            acao = utils.extrair_acao(sentencas_processadas[1])     
            finalidade = utils.extrair_finalidade(sentencas_processadas[2]) 
            erros = utils.verifica_erros_cenario(bem_formada, atomica, minima, utils.valida_precondicao_cenario(sentencas_processadas[0]), utils.retorna_acao_cenario(sentencas_processadas[1]), utils.retorna_finalidade_cenario(sentencas_processadas[2]))        
            end = timeit.default_timer()  
            tempo = utils.formatar_tempo(start, end)

            if erros == None:
                return ResponseCenario(cenario, Constantes.NLTK, tempo, bem_formada, atomica, minima, precondicao, acao, finalidade, tags, erros)
            else:
                return ResponseCenario(cenario, Constantes.NLTK, tempo, bem_formada, atomica, minima, None, None, None, tags, erros)
        else:
            end = timeit.default_timer()  
            tempo = utils.formatar_tempo(start, end)
            return utils.retorna_erro_historia(cenario, Constantes.NLTK, sentencas, tempo)
    
    
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