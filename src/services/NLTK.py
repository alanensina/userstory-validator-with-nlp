from xmlrpc.client import Boolean
import nltk, joblib, timeit
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from src.classes.Response import Response
from src.classes.Palavra import Palavra
from src.classes import Constantes

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')

class NLTK:
    
    def processarHistoria(idioma:str, historia:str):
        start = timeit.default_timer()
        
        bem_formada = NLTK.verifica_C1_historia(historia, idioma)
        atomica = NLTK.verifica_C2_historia(historia, idioma)
        minima = NLTK.verifica_C3_historia(historia, bem_formada)
        ator = NLTK.retorna_ator_historia(historia, idioma)    
        acao = NLTK.retorna_acao_historia(historia, idioma)      
        finalidade = NLTK.retorna_finalidade_historia(historia, idioma)  
        erros = NLTK.verifica_erros_historia(bem_formada, atomica, minima, ator, acao, finalidade)
        end = timeit.default_timer()  
        tempo = NLTK.formatar_tempo(start, end)

        if erros == None:
            return Response(historia, Constantes.NLTK, tempo, bem_formada, atomica, minima, ator, acao, finalidade, erros)
        else:
            ator = NLTK.limpar_mensagem_de_erro(ator)
            acao = NLTK.limpar_mensagem_de_erro(acao)   
            finalidade = NLTK.limpar_mensagem_de_erro(finalidade)
            return Response(historia, Constantes.NLTK, tempo, bem_formada, atomica, minima, ator, acao, finalidade, erros)   
           
        
    def processarCenario(idioma:str, cenario:str):
        start = timeit.default_timer()
        
        bem_formada = NLTK.verifica_C1_cenario(cenario, idioma)
        atomica = NLTK.verifica_C2_cenario(cenario, idioma)
        minima = NLTK.verifica_C3_cenario(cenario, bem_formada)
        ator = NLTK.retorna_ator_cenario(cenario, idioma)    
        acao = NLTK.retorna_acao_cenario(cenario, idioma)      
        finalidade = NLTK.retorna_finalidade_cenario(cenario, idioma)
        erros = NLTK.verifica_erros_cenario(bem_formada, atomica, minima, ator, acao, finalidade)        
        end = timeit.default_timer()  
        tempo = NLTK.formatar_tempo(start, end)

        if erros == None:
            return Response(cenario, Constantes.NLTK, tempo, bem_formada, atomica, minima, ator, acao, finalidade, erros)
        else:
            ator = NLTK.limpar_mensagem_de_erro(ator)
            acao = NLTK.limpar_mensagem_de_erro(acao)   
            finalidade = NLTK.limpar_mensagem_de_erro(finalidade)
            return Response(cenario, Constantes.NLTK, tempo, bem_formada, atomica, minima, ator, acao, finalidade, erros)
    
    
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
        return NLTK.unificar_tagset(pre_tags)
    
    
    def unificar_tagset(tags):
        tagsets = []
        for tupla in tags:
            tagsets.append(Palavra(tupla[0], tupla[1], NLTK.get_classe_gramatical(tupla[1])))        
        return tagsets
    
    
    # Função responsável em retornar a classe gramatical conforme o tagset
    def get_classe_gramatical(tagset):
          if NLTK.verifica_artigo(tagset):
              return Constantes.ARTIGO
          elif NLTK.verifica_adjetivo(tagset):
              return Constantes.ADJETIVO
          elif NLTK.verifica_substantivo(tagset):
              return Constantes.SUBSTANTIVO
          elif tagset == 'NUM' or tagset == 'CD':
              return Constantes.NUMERAL
          elif NLTK.verifica_pronome(tagset):
              return Constantes.PRONOME
          elif NLTK.verifica_adverbio(tagset):
              return Constantes.ADVERBIO
          elif NLTK.verifica_conjuncao(tagset):
              return Constantes.CONJUNCAO
          elif NLTK.verifica_preposicao(tagset):
              return Constantes.PREPOSICAO
          elif tagset == 'IN' or tagset == 'UH':
              return Constantes.INTERJEICAO
          elif NLTK.verifica_verbo(tagset):
              return Constantes.VERBO
          elif tagset == 'VAUX':
              return Constantes.VERBO_AUX
          elif tagset == 'PCP' or tagset == 'RP':
              return Constantes.PARTICIPIO
          elif tagset == 'PDEN':
              return Constantes.PALAVRA_DEN
          elif tagset == 'CUR':
              return Constantes.MOEDA        
          else:
              return Constantes.INVALIDO
          
          
    def verifica_pronome(tagset):
        return tagset == 'PROADJ' or tagset == 'PROSUB' or tagset == 'PROPESS' or tagset == 'PRON' or tagset == 'PRO-KS' or tagset == 'PRO-KS-REL' or tagset == 'PRP' or tagset == 'PRP$'
    
    
    def verifica_adverbio(tagset):
        return tagset == 'ADV' or tagset == 'ADV-KS' or tagset == 'ADV-KS-REL' or tagset == 'RB' or tagset == 'RBS' or tagset == 'RBR'
    
    
    def verifica_substantivo(tagset):
        return tagset == 'N' or tagset == 'NOUN' or tagset == 'NPROP' or tagset == 'NN' or tagset == 'NNP' or tagset == 'NNS'
    
    
    def verifica_conjuncao(tagset):
        return tagset == 'KC' or tagset == 'KS' or tagset == 'CONJ' or tagset == 'CC' or tagset == 'IN'
    
    
    def verifica_verbo(tagset):
        return tagset == 'V' or tagset == 'VERB' or tagset == 'VB' or tagset == 'VBD' or tagset == 'VBG' or tagset == 'VBN' or tagset == 'VBP' or tagset == 'VBG'or tagset == 'VBZ'
    
    
    def verifica_adjetivo(tagset):
        return tagset == 'ADJ' or tagset == 'JJ' or tagset == 'JJR' or tagset == 'JJS'
    
    
    def verifica_preposicao(tagset):
        return tagset == 'PREP' or tagset == 'PRP' or tagset == 'TO'
    
    
    def verifica_artigo(tagset):
        return tagset == 'ART' or tagset == 'DET' or tagset == 'DT'
    
    
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
        sentencas = NLTK.separar_sentencas(texto)
        
        if len(sentencas) < 2:
            return False
        
        ator = NLTK.retorna_ator_historia(texto, idioma)
        acao = NLTK.retorna_acao_historia(texto, idioma)
        finalidade =  NLTK.retorna_finalidade_historia(texto, idioma)
        
        if ator != Constantes.ERRO_ATOR_INCONSISTENTE and acao != Constantes.ERRO_ACAO_INCONSISTENTE and finalidade != Constantes.ERRO_FINALIDADE_INCONSISTENTE:
            return True
        
        return False
    
    def verifica_C1_cenario(texto, idioma):
        sentencas = NLTK.separar_sentencas(texto)
        
        if len(sentencas) < 3:
            return False
        
        ator = NLTK.retorna_ator_cenario(texto, idioma)
        acao = NLTK.retorna_acao_cenario(texto, idioma)
        finalidade =  NLTK.retorna_finalidade_cenario(texto, idioma)
        
        if ator != Constantes.ERRO_ATOR_INCONSISTENTE_2 and acao != Constantes.ERRO_ACAO_INCONSISTENTE_2 and acao != Constantes.ERRO_ACAO_INCONSISTENTE_3  and finalidade != Constantes.ERRO_ACAO_INCONSISTENTE_3:
            return True
        
        return False
    
    
    # Função responsável para verificar o segundo critério de qualidade: Atômica
    # Uma história é atômica quando há apenas um objetivo na tarefa
    # Para validar se a história de usuário é atômica, as sentenças são separadas e em seguida é verificado se a segunda sentença possui menos que 3 verbos
    # Caso a sentença não se enquadre no templete de ação, a história de usuário não será atômica
    def verifica_C2_historia(texto, idioma):
        sentencas = NLTK.separar_sentencas(texto)
        sentencas_tamanho = len(sentencas)
        verbos = 0

        if sentencas_tamanho < 2:
            return False

        # Processa a sentença destinada a ação (2ª sentença)
        tags = NLTK.processar(sentencas[1], idioma)

        for tag in tags:
            if tag.classe == Constantes.VERBO:
                verbos = verbos + 1
            
        return verbos < 3

    # Função responsável para verificar o segundo critério de qualidade: Atômica
    # Um cenário é atômico quando há apenas um objetivo na tarefa
    # Para validar se o cenário é atômico, as sentenças são separadas e em seguida é verificado a sentenção de ação (QUANDO/WHEN) possui menos que 3 verbos
    # Caso a sentença não se enquadre no templete de ação, o cenário não será atômico
    def verifica_C2_cenario(texto, idioma):
        sentencas = NLTK.separar_sentencas(texto)
        acoes = []

        if len(sentencas) < 3:
            return False

        for s in sentencas:
            if Constantes.QUANDO.lower() in s.lower() or Constantes.WHEN.lower() in s.lower():
                acoes.append(s)

        if len(acoes) > 1:
            return False

       # Processa a sentença destinada a ação
        tags = NLTK.processar(acoes[0], idioma)

        verbos = 0

        for tag in tags:
            if tag.classe == Constantes.VERBO:
                verbos = verbos + 1 

        return verbos < 3
    
    
    # Função responsável para verificar o terceiro critério de qualidade: Mínima
    # Uma história é mínima quando contém apenas as informações referentes ao critério de qualidade Bem Formada, qualquer informação extra como comentários 
    # e descrição esperada do comportamento deverá ser deixada de lado.
    def verifica_C3_historia(texto, bem_formada):
        sentencas = NLTK.separar_sentencas(texto)
        
        if bem_formada and len(sentencas) <= 3:
            return True
        
        return False


    # Função responsável para verificar o terceiro critério de qualidade: Mínima
    # Um cenário é mínima quando contém apenas as informações referentes ao critério de qualidade Bem Formada, qualquer informação extra como comentários e descrição esperada do comportamento deverá ser deixada de lado.
    # É verificado quantas vezes o DADO/QUANDO/ENTÃO é chamado, caso tenha sido chamado mais que uma vez cada, o cenário não é mínimo
    def verifica_C3_cenario(texto, bem_formada):
        sentencas = NLTK.separar_sentencas(texto)
        dado = 0
        quando = 0
        entao = 0

        for s in sentencas:
            if (Constantes.DADO.lower() in s.lower()) or (Constantes.GIVEN.lower() in s.lower()):
                dado = dado + 1
            elif (Constantes.QUANDO.lower() in s.lower()) or (Constantes.WHEN.lower() in s.lower()):
                quando = quando + 1
            elif (Constantes.ENTAO.lower() in s.lower()) or (Constantes.THEN.lower() in s.lower()):
                entao = entao + 1

        minima = dado == 1 and quando == 1 and entao == 1

        return bem_formada and minima and len(sentencas) >= 3
    
    
    def verifica_erros_historia(bem_formada, atomica, minima, ator, acao, finalidade):
        erros = ''
        if not bem_formada:
            erros = 'A história não atende o primeiro critério de qualidade que é Bem formada. '
        if not atomica:
            erros = erros + 'A história não atende o segundo critério de qualidade que é Atômica. '
        if not minima:
            erros = erros + 'A história não atende o terceiro critério de qualidade que é Mínima. '
        if ator == Constantes.ERRO_ATOR_INCONSISTENTE:
            erros = erros + Constantes.ERRO_ATOR_INCONSISTENTE + ' '
        if acao == Constantes.ERRO_ACAO_INCONSISTENTE:
            erros = erros + Constantes.ERRO_ACAO_INCONSISTENTE + ' '
        if finalidade == Constantes.ERRO_FINALIDADE_INCONSISTENTE:
            erros = erros + Constantes.ERRO_FINALIDADE_INCONSISTENTE + ' '
        if bem_formada and atomica and minima and ator != Constantes.ERRO_ATOR_INCONSISTENTE and acao != Constantes.ERRO_ACAO_INCONSISTENTE and finalidade != Constantes.ERRO_FINALIDADE_INCONSISTENTE:
            return None
        
        return erros

    
    def verifica_erros_cenario(bem_formada, atomica, minima, ator, acao, finalidade):
        erros = ''
        if not bem_formada:
            erros = 'O cenário não atende ao primeiro critério de qualidade que é Bem formada. '
        if not atomica:
            erros = erros + 'O cenário não atende ao segundo critério de qualidade que é Atômica. '
        if not minima:
            erros = erros + 'O cenário não atende ao terceiro critério de qualidade que é Mínima. '
        if ator == Constantes.ERRO_ATOR_INCONSISTENTE_2:
            erros = erros + Constantes.ERRO_ATOR_INCONSISTENTE_2 + ' '
        if acao == Constantes.ERRO_ACAO_INCONSISTENTE_2:
            erros = erros + Constantes.ERRO_ACAO_INCONSISTENTE_2 + ' '
        if acao == Constantes.ERRO_ACAO_INCONSISTENTE_3:
            erros = erros + Constantes.ERRO_ACAO_INCONSISTENTE_3 + ' '
        if finalidade == Constantes.ERRO_FINALIDADE_INCONSISTENTE_2:
            erros = erros + Constantes.ERRO_FINALIDADE_INCONSISTENTE_2 + ' '
        if finalidade == Constantes.ERRO_ACAO_INCONSISTENTE_3:
            erros = erros + Constantes.ERRO_FINALIDADE_INCONSISTENTE_2 + ' '
        if bem_formada and atomica and minima and ator != Constantes.ERRO_ATOR_INCONSISTENTE_2 and acao != Constantes.ERRO_ACAO_INCONSISTENTE_2 and acao != Constantes.ERRO_ACAO_INCONSISTENTE_3 and finalidade != Constantes.ERRO_FINALIDADE_INCONSISTENTE_2 and finalidade != Constantes.ERRO_ACAO_INCONSISTENTE_3:
            return None
        
        return erros
    
        
    # Conforme layout de Cohn, uma história de usuário deve ser escrita em no máximo 3 sentenças, 
    # o ator deverá ser identificado na primeira sentença
    def retorna_ator_historia(texto, idioma):
        ator = ''
        sentencas = NLTK.separar_sentencas(texto)
        sentenca = sentencas[0]
        tags = NLTK.processar(sentenca, idioma)
        
        substantivo = False
        pronome = False
        preposicao = False
        artigo = False
        
        for tag in tags:
            if tag.classe == Constantes.SUBSTANTIVO or tag.classe == Constantes.ARTIGO or tag.classe == Constantes.PRONOME or tag.classe == Constantes.CONJUNCAO or tag.classe == Constantes.PREPOSICAO:
                if ator == '':
                    ator = tag.palavra
                else:
                    ator = ator + ' ' + tag.palavra
            
            if tag.classe == Constantes.SUBSTANTIVO:
                substantivo = True
            elif tag.classe == Constantes.PRONOME:
                pronome = True
            elif tag.classe == Constantes.PREPOSICAO:
                preposicao = True
            elif tag.classe == Constantes.ARTIGO:
                artigo = True
                    
        if substantivo and (pronome or preposicao or artigo):
            return ator
        else:
            return Constantes.ERRO_ATOR_INCONSISTENTE
        
    # Conforme o layout de cenário (Dado/Quando/Então), o ator deverá ser identificado na primeira sentença
    # A palavra Dado/Given também deve estar presente
    def retorna_ator_cenario(texto, idioma):
        ator = ''
        sentencas = NLTK.separar_sentencas(texto)
        sentenca = sentencas[0]
        tags = NLTK.processar(sentenca, idioma)
        
        dado_given = False
        substantivo = False
        pronome = False
        preposicao = False
        artigo = False
        
        if Constantes.DADO.lower() in sentenca.lower() or Constantes.GIVEN.lower() in sentenca.lower():
            dado_given = True
            
        for tag in tags:
            if tag.classe == Constantes.SUBSTANTIVO or tag.classe == Constantes.ARTIGO or tag.classe == Constantes.PRONOME or tag.classe == Constantes.CONJUNCAO or tag.classe == Constantes.PREPOSICAO or tag.classe == Constantes.VERBO or tag.classe == Constantes.VERBO_AUX:
                if ator == '':
                    ator = tag.palavra
                else:
                    ator = ator + ' ' + tag.palavra
            
            if tag.classe == Constantes.SUBSTANTIVO:
                substantivo = True
            elif tag.classe == Constantes.PRONOME:
                pronome = True
            elif tag.classe == Constantes.PREPOSICAO:
                preposicao = True
            elif tag.classe == Constantes.ARTIGO:
                artigo = True
                
        if dado_given and substantivo and (pronome or preposicao or artigo):
            return ator
            
        return Constantes.ERRO_ATOR_INCONSISTENTE_2
        
        
    # Conforme layout de Cohn, uma história de usuário deve ser escrita em no máximo 3 sentenças, 
    # a ação deverá ser identificado na segunda sentença
    def retorna_acao_historia(texto, idioma):
        acao = ''
        sentencas = NLTK.separar_sentencas(texto)
        
        if len(sentencas) >= 2:
            sentenca = sentencas[1]
        else:
            return None

        tags = NLTK.processar(sentenca, idioma)
        
        verbo = False
        substantivo = False
        pronome = False
        preposicao = False
        
        for tag in tags:
            if tag.classe == Constantes.VERBO or tag.classe == Constantes.SUBSTANTIVO or tag.classe == Constantes.PRONOME or tag.classe == Constantes.CONJUNCAO or tag.classe == Constantes.PREPOSICAO:
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
            
        if verbo and substantivo and pronome and preposicao:        
            return acao
        else:
            return Constantes.ERRO_ACAO_INCONSISTENTE

        
    # Conforme o layout de cenário (Dado/Quando/Então), a ação deverá ser identificada em uma sentença posterior a sentença do ator
    # A palavra Quando/When também deve estar presente nessa sentença
    def retorna_acao_cenario(texto, idioma):
        acao = ''
        sentencas = NLTK.separar_sentencas(texto)
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
            elif NLTK.verifica_ator_e_acao_e_finalidade_ja_encontrados(sentenca, ator_encontrado, acao_encontrada, False):
                return Constantes.ERRO_ACAO_INCONSISTENTE_3

        ator_antes_da_acao = posicao_ator < posicao_acao
        
        sentenca = ''
        
        if posicao_acao > 0 :
            sentenca = sentencas[posicao_acao]
        else:
            return Constantes.ERRO_ACAO_INCONSISTENTE_2
        
        tags = NLTK.processar(sentenca, idioma)
        
        verbo = False
        substantivo = False
        pronome = False
        preposicao = False
        
        for tag in tags:
            if tag.classe == Constantes.VERBO or tag.classe == Constantes.VERBO_AUX or tag.classe == Constantes.SUBSTANTIVO or tag.classe == Constantes.PRONOME or tag.classe == Constantes.CONJUNCAO or tag.classe == Constantes.PREPOSICAO:
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
            
        if verbo and substantivo and pronome and preposicao and ator_antes_da_acao:        
            return acao
        
        return Constantes.ERRO_ACAO_INCONSISTENTE_2
        
    
    # Conforme layout de Cohn, uma história de usuário deve ser escrita em no máximo 3 sentenças, 
    # a finalidade é opcional, mas caso ocorra deverá ser identificada na terceira sentença
    def retorna_finalidade_historia(texto, idioma):
        finalidade = ''
        sentencas = NLTK.separar_sentencas(texto)
        
        verbo = False
        substantivo = False
        pronome = False
        preposicao = False
        
        if len(sentencas) >= 3:
            sentenca = sentencas[2]
            tags = NLTK.processar(sentenca, idioma)
            for tag in tags:
                if tag.classe == Constantes.VERBO or tag.classe == Constantes.SUBSTANTIVO or tag.classe == Constantes.PRONOME or tag.classe == Constantes.CONJUNCAO or tag.classe == Constantes.PREPOSICAO:
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
        else:
            return None
                    
        if verbo and (pronome or preposicao or substantivo):        
            return finalidade
        else:
            return Constantes.ERRO_FINALIDADE_INCONSISTENTE
    
   
    # Conforme o layout de cenário (Dado/Quando/Então), a finalidade deverá ser identificada em uma sentença posterior a sentença do ator e da ação
    # A palavra Então/Then também deve estar presente nessa sentença
    def retorna_finalidade_cenario(texto, idioma):
        finalidade = ''
        sentencas = NLTK.separar_sentencas(texto)
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
            elif NLTK.verifica_ator_e_acao_e_finalidade_ja_encontrados(sentenca, ator_encontrado, acao_encontrada, finalidade_encontrada):
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
        
        tags = NLTK.processar(sentenca, idioma)
        
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
   
    
    def separar_sentencas(texto):
        return texto.split(',')  
    
    
    def formatar_tempo(start, end):
        return round(end - start, 5).__str__().replace('.',',') + ' segundos'
    
            
    def limpar_mensagem_de_erro(input):
        if input == Constantes.ERRO_ATOR_INCONSISTENTE:
            return None
        if input == Constantes.ERRO_ATOR_INCONSISTENTE_2:
            return None
        elif input == Constantes.ERRO_ACAO_INCONSISTENTE:
            return None
        elif input == Constantes.ERRO_ACAO_INCONSISTENTE_2:
            return None
        elif input == Constantes.ERRO_ACAO_INCONSISTENTE_3:
            return None
        elif input == Constantes.ERRO_FINALIDADE_INCONSISTENTE:
            return None
        elif input == Constantes.ERRO_FINALIDADE_INCONSISTENTE_2:
            return None
        
        
    def verifica_ator_e_acao_e_finalidade_ja_encontrados(sentenca, ator_encontrado, acao_encontrada, finalidade_encontrada):
        return ((Constantes.DADO.lower() in sentenca.lower() or Constantes.GIVEN.lower() in sentenca.lower()) and ator_encontrado) or ((Constantes.QUANDO.lower() in sentenca.lower() or Constantes.WHEN.lower() in sentenca.lower()) and acao_encontrada) or ((Constantes.ENTAO.lower() in sentenca.lower() or Constantes.THEN.lower() in sentenca.lower()) and finalidade_encontrada)   