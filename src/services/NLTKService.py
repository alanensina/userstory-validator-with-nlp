import nltk, joblib, timeit
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from src.classes.Response import Response
from src.classes import Constantes
from src.services.UtilsService import utils

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')

class NLTKService():
    
    def processarHistoria(idioma:str, historia:str):
        start = timeit.default_timer()
        
        bem_formada = NLTKService.verifica_C1_historia(historia, idioma)
        atomica = NLTKService.verifica_C2_historia(historia, idioma)
        minima = utils.verifica_C3_historia(historia, bem_formada)
        ator = NLTKService.retorna_ator_historia(historia, idioma)    
        acao = NLTKService.retorna_acao_historia(historia, idioma)      
        finalidade = NLTKService.retorna_finalidade_historia(historia, idioma)  
        erros = utils.verifica_erros_historia(bem_formada, atomica, minima, ator, acao, finalidade)
        end = timeit.default_timer()  
        tempo = utils.formatar_tempo(start, end)

        if erros == None:
            return Response(historia, Constantes.NLTK, tempo, bem_formada, atomica, minima, ator, acao, finalidade, erros)
        else:
            ator = utils.limpar_mensagem_de_erro(ator)
            acao = utils.limpar_mensagem_de_erro(acao)   
            finalidade = utils.limpar_mensagem_de_erro(finalidade)
            return Response(historia, Constantes.NLTK, tempo, bem_formada, atomica, minima, ator, acao, finalidade, erros)   
           
        
    def processarCenario(idioma:str, cenario:str):
        start = timeit.default_timer()
        
        bem_formada = NLTKService.verifica_C1_cenario(cenario, idioma)
        atomica = NLTKService.verifica_C2_cenario(cenario, idioma)
        minima = utils.verifica_C3_cenario(cenario, bem_formada)
        ator = NLTKService.retorna_ator_cenario(cenario, idioma)    
        acao = NLTKService.retorna_acao_cenario(cenario, idioma)      
        finalidade = NLTKService.retorna_finalidade_cenario(cenario, idioma)
        erros = utils.verifica_erros_cenario(bem_formada, atomica, minima, ator, acao, finalidade)        
        end = timeit.default_timer()  
        tempo = utils.formatar_tempo(start, end)

        if erros == None:
            return Response(cenario, Constantes.NLTK, tempo, bem_formada, atomica, minima, ator, acao, finalidade, erros)
        else:
            ator = utils.limpar_mensagem_de_erro(ator)
            acao = utils.limpar_mensagem_de_erro(acao)   
            finalidade = utils.limpar_mensagem_de_erro(finalidade)
            return Response(cenario, Constantes.NLTK, tempo, bem_formada, atomica, minima, ator, acao, finalidade, erros)
    
    
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
    def verifica_C1_historia(texto, idioma):
        sentencas = utils.separar_sentencas(texto)
        
        if len(sentencas) < 2:
            return False
        
        ator = NLTKService.retorna_ator_historia(texto, idioma)
        acao = NLTKService.retorna_acao_historia(texto, idioma)
        finalidade =  NLTKService.retorna_finalidade_historia(texto, idioma)
        
        if ator != Constantes.ERRO_ATOR_INCONSISTENTE and acao != Constantes.ERRO_ACAO_INCONSISTENTE and finalidade != Constantes.ERRO_FINALIDADE_INCONSISTENTE:
            return True
        
        return False
    

    def verifica_C1_cenario(texto, idioma):
        sentencas = utils.separar_sentencas(texto)
        
        if len(sentencas) < 3:
            return False
        
        ator = NLTKService.retorna_ator_cenario(texto, idioma)
        acao = NLTKService.retorna_acao_cenario(texto, idioma)
        finalidade =  NLTKService.retorna_finalidade_cenario(texto, idioma)
        
        if ator != Constantes.ERRO_ATOR_INCONSISTENTE_2 and acao != Constantes.ERRO_ACAO_INCONSISTENTE_2 and acao != Constantes.ERRO_ACAO_INCONSISTENTE_3  and finalidade != Constantes.ERRO_ACAO_INCONSISTENTE_3:
            return True
        
        return False
    
    
    # Função responsável para verificar o segundo critério de qualidade: Atômica
    # Uma história é atômica quando há apenas um objetivo na tarefa
    # Para validar se a história de usuário é atômica, as sentenças são separadas e em seguida é verificado se a segunda sentença possui menos que 3 verbos
    # Caso a sentença não se enquadre no templete de ação, a história de usuário não será atômica
    def verifica_C2_historia(texto, idioma):
        sentencas = utils.separar_sentencas(texto)
        sentencas_tamanho = len(sentencas)
        verbos = 0

        if sentencas_tamanho < 2:
            return False

        # Processa a sentença destinada a ação (2ª sentença)
        tags = NLTKService.processar(sentencas[1], idioma)

        for tag in tags:
            if tag.classe == Constantes.VERBO and tag.palavra != 'would':
                verbos = verbos + 1
            
        return verbos < 3

    # Função responsável para verificar o segundo critério de qualidade: Atômica
    # Um cenário é atômico quando há apenas um objetivo na tarefa
    # Para validar se o cenário é atômico, as sentenças são separadas e em seguida é verificado a sentenção de ação (QUANDO/WHEN) possui menos que 3 verbos
    # Caso a sentença não se enquadre no templete de ação, o cenário não será atômico
    def verifica_C2_cenario(texto, idioma):
        sentencas = utils.separar_sentencas(texto)
        acoes = []

        if len(sentencas) < 3:
            return False

        for s in sentencas:
            if Constantes.QUANDO.lower() in s.lower() or Constantes.WHEN.lower() in s.lower():
                acoes.append(s)

        if len(acoes) > 1:
            return False

       # Processa a sentença destinada a ação
        tags = NLTKService.processar(acoes[0], idioma)

        verbos = 0

        for tag in tags:
            if tag.classe == Constantes.VERBO and tag.palavra != 'would':
                verbos = verbos + 1 

        return verbos < 3
    
        
    # Conforme layout de Cohn, uma história de usuário deve ser escrita em no máximo 3 sentenças, 
    # o ator deverá ser identificado na primeira sentença
    def retorna_ator_historia(texto, idioma):
        sentencas = utils.separar_sentencas(texto)
        sentenca = sentencas[0]
        tags = NLTKService.processar(sentenca, idioma)
        
        return utils.valida_ator_historia(tags)

        
    # Conforme o layout de cenário (Dado/Quando/Então), o ator deverá ser identificado na primeira sentença
    # A palavra Dado/Given também deve estar presente
    def retorna_ator_cenario(texto, idioma):
        sentencas = utils.separar_sentencas(texto)
        sentenca = sentencas[0]
        tags = NLTKService.processar(sentenca, idioma)
        return utils.valida_ator_cenario(tags, sentenca)
       
        
    # Conforme layout de Cohn, uma história de usuário deve ser escrita em no máximo 3 sentenças, 
    # a ação deverá ser identificado na segunda sentença
    def retorna_acao_historia(texto, idioma):
        sentencas = utils.separar_sentencas(texto)
        
        if len(sentencas) >= 2:
            sentenca = sentencas[1]
        else:
            return Constantes.ERRO_ACAO_INCONSISTENTE

        tags = NLTKService.processar(sentenca, idioma)
        
        return utils.valida_acao_historia(tags)

        
    # Conforme o layout de cenário (Dado/Quando/Então), a ação deverá ser identificada em uma sentença posterior a sentença do ator
    # A palavra Quando/When também deve estar presente nessa sentença
    def retorna_acao_cenario(texto, idioma):
        acao = ''
        sentencas = utils.separar_sentencas(texto)
        posicao_ator = 0
        ator_encontrado = False
        posicao_acao = 0
        acao_encontrada = False
        
        for sentenca in sentencas:
            if (Constantes.DADO.lower() in sentenca.lower() or Constantes.GIVEN.lower() in sentenca.lower()) and not ator_encontrado:
                ator_encontrado = True
                posicao_ator = sentencas.index(sentenca)
            elif (Constantes.QUANDO.lower() in sentenca.lower() or Constantes.WHEN.lower() in sentenca.lower()) and not acao_encontrada:
                acao_encontrada = True
                posicao_acao = sentencas.index(sentenca)
            elif utils.verifica_ator_e_acao_e_finalidade_ja_encontrados(sentenca, ator_encontrado, acao_encontrada, False):
                return Constantes.ERRO_ACAO_INCONSISTENTE_3

        ator_antes_da_acao = posicao_ator < posicao_acao
        
        sentenca = ''
        
        if posicao_acao > 0 :
            sentenca = sentencas[posicao_acao]
        else:
            return Constantes.ERRO_ACAO_INCONSISTENTE_2
        
        tags = NLTKService.processar(sentenca, idioma)
        
        verbo = False
        substantivo = False
        pronome = False
        preposicao = False
        adverbio = False
        
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
            
        if verbo and substantivo and (pronome or preposicao or adverbio) and ator_antes_da_acao:        
            return acao
        
        return Constantes.ERRO_ACAO_INCONSISTENTE_2
        
    
    # Conforme layout de Cohn, uma história de usuário deve ser escrita em no máximo 3 sentenças, 
    # a finalidade é opcional, mas caso ocorra deverá ser identificada na terceira sentença
    def retorna_finalidade_historia(texto, idioma):
        sentencas = utils.separar_sentencas(texto)

        if len(sentencas) >= 3:
            sentenca = sentencas[2]
            tags = NLTKService.processar(sentenca, idioma)
            return utils.valida_finalidade_historia(tags)
        return None
    
   
    # Conforme o layout de cenário (Dado/Quando/Então), a finalidade deverá ser identificada em uma sentença posterior a sentença do ator e da ação
    # A palavra Então/Then também deve estar presente nessa sentença
    def retorna_finalidade_cenario(texto, idioma):
        finalidade = ''
        sentencas = utils.separar_sentencas(texto)
        posicao_ator = 0
        ator_encontrado = False
        posicao_acao = 0
        acao_encontrada = False
        posicao_finalidade = 0
        finalidade_encontrada = False
        
        for sentenca in sentencas:
            if (Constantes.DADO.lower() in sentenca.lower() or Constantes.GIVEN.lower() in sentenca.lower()) and not ator_encontrado:
                ator_encontrado = True
                posicao_ator = sentencas.index(sentenca)
            elif (Constantes.QUANDO.lower() in sentenca.lower() or Constantes.WHEN.lower() in sentenca.lower()) and not acao_encontrada:
                acao_encontrada = True
                posicao_acao = sentencas.index(sentenca)
            elif (Constantes.ENTAO.lower() in sentenca.lower() or Constantes.THEN.lower() in sentenca.lower()) and not finalidade_encontrada:
                finalidade_encontrada = True
                posicao_finalidade = sentencas.index(sentenca)
            elif utils.verifica_ator_e_acao_e_finalidade_ja_encontrados(sentenca, ator_encontrado, acao_encontrada, finalidade_encontrada):
                return Constantes.ERRO_ACAO_INCONSISTENTE_3
            
        ordem_correta = posicao_ator < posicao_acao and posicao_acao < posicao_finalidade
        verbo = False
        substantivo = False
        pronome = False
        preposicao = False
        adverbio = False
        
        sentenca = ''
        
        if posicao_finalidade > 0 :
            sentenca = sentencas[posicao_finalidade]
        else:
            return Constantes.ERRO_FINALIDADE_INCONSISTENTE_2
        
        tags = NLTKService.processar(sentenca, idioma)
        
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
                    
        if verbo and (pronome or preposicao or substantivo or adverbio) and ordem_correta:        
            return finalidade
        
        return Constantes.ERRO_FINALIDADE_INCONSISTENTE_2