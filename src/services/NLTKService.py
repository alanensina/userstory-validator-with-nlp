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

            bem_formada = NLTKService.verifica_C1_historia(sentencas_processadas)
            atomica = NLTKService.verifica_C2_historia(sentencas_processadas)
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
        
            bem_formada = NLTKService.verifica_C1_cenario(sentencas_processadas)
            atomica = NLTKService.verifica_C2_cenario(sentencas_processadas)
            minima = utils.verifica_C3_cenario(sentencas_processadas, bem_formada)

            precondicao = utils.extrair_preCondicao(sentencas_processadas[0])    
            acao = utils.extrair_acao(sentencas_processadas[1])     
            finalidade = utils.extrair_finalidade(sentencas_processadas[2]) 
            erros = utils.verifica_erros_cenario(bem_formada, atomica, minima, NLTKService.retorna_precondicao_cenario(sentencas_processadas[0]), NLTKService.retorna_acao_cenario(sentencas_processadas[1]), NLTKService.retorna_finalidade_cenario(sentencas_processadas[2]))        
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
        #ptbr_tagger_trigram = joblib.load('POS_tagger_trigram.pkl')   
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
    
    
    # Função responsável para verificar o primeiro critério de qualidade: Bem formada
    # Uma história é bem formada quando há o seguinte formato: Quem realizará a tarefa + objetivo da tarefa + finalidade para a realização da tarefa (opcional)
    # A história deve ter no mínimo 2 sentenças (uma para o ator + uma para a ação)
    # Formato esperado: Sujeito + Adjetivo (opcional) + Verbo + Objeto indireto (opcional) + Objeto direto
    # Formato das tagsets:
    # Sujeito -> Substantivo ou pronome
    # Adjetivo (opcional) -> Adjetivo
    # Verbo -> Verbo
    # Objeto indireto (opcional) -> Substantivo ou pronome
    # Objeto direto -> Substantivo ou pronome
    def verifica_C1_historia(sentencas_processadas):
        if len(sentencas_processadas) < 2:
            return False
        
        finalidade = None
        ator = NLTKService.retorna_ator_historia(sentencas_processadas[0])
        acao = NLTKService.retorna_acao_historia(sentencas_processadas[1])
        if len(sentencas_processadas) > 2:
            finalidade =  NLTKService.retorna_finalidade_historia(sentencas_processadas[2])
        
        if ator != Constantes.ERRO_ATOR_INCONSISTENTE and acao != Constantes.ERRO_ACAO_INCONSISTENTE and finalidade != Constantes.ERRO_FINALIDADE_INCONSISTENTE:
            return True
        
        return False
    

    def verifica_C1_cenario(sentencas_processadas):
        if len(sentencas_processadas) < 3:
            return False
        
        precondicao = NLTKService.retorna_precondicao_cenario(sentencas_processadas[0])
        acao = NLTKService.retorna_acao_cenario(sentencas_processadas[1])
        finalidade =  NLTKService.retorna_finalidade_cenario(sentencas_processadas[2])
        
        if precondicao != Constantes.ERRO_PRECONDICAO_INCONSISTENTE and acao != Constantes.ERRO_ACAO_INCONSISTENTE_2 and acao != Constantes.ERRO_ACAO_INCONSISTENTE_3  and finalidade != Constantes.ERRO_ACAO_INCONSISTENTE_3:
            return True
        
        return False
    
    
    # Função responsável para verificar o segundo critério de qualidade: Atômica
    # Uma história é atômica quando há apenas um objetivo na tarefa
    # Para validar se a história de usuário é atômica, as sentenças são separadas e em seguida é verificado se a segunda sentença possui menos que 3 verbos
    # Caso a sentença não se enquadre no templete de ação, a história de usuário não será atômica
    def verifica_C2_historia(sentencas_processadas):
        verbos = 0

        if len(sentencas_processadas) < 2:
            return False

        tags = sentencas_processadas[1]

        for tag in tags:
            if tag.classe == Constantes.VERBO and tag.palavra != 'would':
                verbos = verbos + 1
            
        return verbos < 3

    # Função responsável para verificar o segundo critério de qualidade: Atômica
    # Um cenário é atômico quando o número de ações seja maior que zero e seja igual ao número de condicionais
    #TODO: verificar se esse critério se aplica a cenários
    def verifica_C2_cenario(tags):
        num_acoes = 0
        num_condicoes = 0
        sentenca = tags[1] # Tags da sentença da ação

        for tag in sentenca:
            if (tag.classe == Constantes.VERBO or tag.classe == Constantes.VERBO_AUX) and tag.palavra != 'would':
                num_acoes = num_acoes + 1

            elif tag.palavra.lower() == 'e' or tag.palavra.lower() == 'and':
                num_condicoes = num_condicoes + 1

        if num_condicoes == 0:
            return num_acoes >= 1
        else:       
            return (num_acoes > num_condicoes) and num_acoes != 0
    
        
    # Conforme layout de Cohn, uma história de usuário deve ser escrita em no máximo 3 sentenças, 
    # o ator deverá ser identificado na primeira sentença
    def retorna_ator_historia(tags):
        return utils.valida_ator_historia(tags)

        
    # Conforme o layout de cenário (Dado/Quando/Então), a pré-condição deverá ser identificado na primeira sentença
    # A palavra Dado/Given também deve estar presente
    def retorna_precondicao_cenario(tags):
        return utils.valida_precondicao_cenario(tags)
       
        
    # Conforme layout de Cohn, uma história de usuário deve ser escrita em no máximo 3 sentenças, 
    # a ação deverá ser identificado na segunda sentença
    def retorna_acao_historia(tags):
        return utils.valida_acao_historia(tags)

        
    # Conforme o layout de cenário (Dado/Quando/Então), a ação deverá ser identificada em uma sentença posterior a sentença do ator
    # A palavra Quando/When também deve estar presente nessa sentença
    def retorna_acao_cenario(tags):
        verbo = False
        substantivo = False
        pronome = False
        preposicao = False
        adverbio = False
        acao = ''
        
        for tag in tags:
            if tag.classe == Constantes.VERBO or tag.classe == Constantes.VERBO_AUX or tag.classe == Constantes.SUBSTANTIVO or tag.classe == Constantes.PRONOME or tag.classe == Constantes.CONJUNCAO or tag.classe == Constantes.PREPOSICAO or tag.classe == Constantes.ARTIGO or tag.classe == Constantes.ADVERBIO:
                if acao == '':
                    acao = tag.palavra
                else:
                    acao = acao + ' ' + tag.palavra
            
            if tag.classe == Constantes.VERBO or tag.classe == Constantes.VERBO_AUX:
                verbo = True
            elif tag.classe == Constantes.SUBSTANTIVO:
                substantivo = True
            elif tag.classe == Constantes.PRONOME:
                pronome = True
            elif tag.classe == Constantes.PREPOSICAO:
                preposicao = True
            elif tag.classe == Constantes.ADVERBIO:
                adverbio = True
            
        if verbo and substantivo and (pronome or preposicao or adverbio):        
            return acao
        
        return Constantes.ERRO_ACAO_INCONSISTENTE_2
        
    
    # Conforme layout de Cohn, uma história de usuário deve ser escrita em no máximo 3 sentenças, 
    # a finalidade é opcional, mas caso ocorra deverá ser identificada na terceira sentença
    def retorna_finalidade_historia(tags):
            return utils.valida_finalidade_historia(tags)
   
    # Conforme o layout de cenário (Dado/Quando/Então), a finalidade deverá ser identificada em uma sentença posterior a sentença do ator e da ação
    # A palavra Então/Then também deve estar presente nessa sentença
    def retorna_finalidade_cenario(tags):
        finalidade = ''
        verbo = False
        pronome = False
        preposicao = False
        substantivo = False
        adverbio = False

        for tag in tags:
                if tag.classe == Constantes.VERBO or tag.classe == Constantes.VERBO_AUX or tag.classe == Constantes.SUBSTANTIVO or tag.classe == Constantes.PRONOME or tag.classe == Constantes.CONJUNCAO or tag.classe == Constantes.PREPOSICAO or tag.classe == Constantes.ADVERBIO or tag.classe == Constantes.PARTICIPIO or tag.classe == Constantes.ADJETIVO or tag.classe == Constantes.ARTIGO:
                    if finalidade == '':
                        finalidade = tag.palavra
                    else:
                        finalidade = finalidade + ' ' + tag.palavra 
                        
                if tag.classe == Constantes.VERBO or tag.classe == Constantes.VERBO_AUX:
                    verbo = True
                elif tag.classe == Constantes.SUBSTANTIVO:
                    substantivo = True
                elif tag.classe == Constantes.PRONOME:
                    pronome = True
                elif tag.classe == Constantes.PREPOSICAO:
                    preposicao = True
                elif tag.classe == Constantes.ADVERBIO:
                    adverbio = True
                    
        if verbo and (pronome or preposicao or substantivo or adverbio):        
            return finalidade
        
        return Constantes.ERRO_FINALIDADE_INCONSISTENTE_2