from src.classes import Constantes
from src.classes.Palavra import Palavra
from src.classes.ResponseHistoria import ResponseHistoria

class UtilsService():

    def __init__(self):
        pass 

    def unificar_tagset(self, tags, tecnologia):
        tagsets = []

        if tecnologia == Constantes.NLTK:
            for tupla in tags:
                tagsets.append(Palavra(tupla[0], tupla[1], UtilsService.get_classe_gramatical(tupla[1])))

        elif tecnologia == Constantes.SPACY:
            for token in tags:
                tagsets.append(Palavra(token.text, token.tag_, UtilsService.get_classe_gramatical(token.tag_))) 

        return tagsets

    # Função responsável em retornar a classe gramatical conforme o tagset
    def get_classe_gramatical(tagset):
          if UtilsService.verifica_artigo(tagset):
              return Constantes.ARTIGO
          elif UtilsService.verifica_adjetivo(tagset):
              return Constantes.ADJETIVO
          elif UtilsService.verifica_substantivo(tagset):
              return Constantes.SUBSTANTIVO
          elif UtilsService.verifica_numeral(tagset):
              return Constantes.NUMERAL
          elif UtilsService.verifica_pronome(tagset):
              return Constantes.PRONOME
          elif UtilsService.verifica_adverbio(tagset):
              return Constantes.ADVERBIO
          elif UtilsService.verifica_conjuncao(tagset):
              return Constantes.CONJUNCAO
          elif UtilsService.verifica_preposicao(tagset):
              return Constantes.PREPOSICAO
          elif UtilsService.verifica_interjeicao(tagset):
              return Constantes.INTERJEICAO
          elif UtilsService.verifica_verbo(tagset):
              return Constantes.VERBO
          elif UtilsService.verifica_verbo_aux(tagset):
              return Constantes.VERBO_AUX
          elif UtilsService.verifica_participio(tagset):
              return Constantes.PARTICIPIO
          elif UtilsService.verifica_denotativo(tagset):
              return Constantes.PALAVRA_DEN
          elif UtilsService.verifica_moeda(tagset):
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


    def verifica_erro_separacao(self, erro):
        return erro == Constantes.ERRO_ATOR_INEXISTENTE or erro == Constantes.ERRO_ACAO_INEXISTENTE or erro == Constantes.ERRO_PRECONDICAO_INEXISTENTE or erro == Constantes.ERRO_ACAO_INEXISTENTE_CENARIO or erro == Constantes.ERRO_FINALIDADE_INEXISTENTE_CENARIO or erro == Constantes.ERRO_ORDENACAO_CENARIO

    # As histórias devem ter suas sentenças separadas através de palavras-chave para que cada sentença seja avaliada independentemente
    # Palavras-chave:
    # Eu como, Como -> primeira sentença, identificará o ator
    # gostaria -> segunda sentença, identificará a ação
    # para que, para -> terceira sentença, identificará a finalidade
    def separar_sentencas_historia(self, texto):
        sentencas = []
        palavras = texto.split()

        pos_eu = -1
        pos_como = -1
        pos_gostaria = -1
        pos_para = -1

        for p in palavras:
            if (p.lower() == 'eu' or  p == 'I') and pos_eu == -1:
                pos_eu = palavras.index(p)
            elif (p.lower() == 'como' or p.lower() == 'as') and pos_como == -1:
                pos_como = palavras.index(p)
            elif (p.lower() == 'gostaria' or p.lower() == 'would') and pos_gostaria == -1:
                pos_gostaria = palavras.index(p)
            elif (p.lower() == 'para' or p.lower() == 'so') and pos_para == -1:
                pos_para = palavras.index(p)

        ator = ''
        acao = ''
        finalidade = ''

        if pos_eu == -1 and pos_como == -1:
            return Constantes.ERRO_ATOR_INEXISTENTE

        if pos_eu != -1 and pos_como == -1:
            return Constantes.ERRO_ATOR_INEXISTENTE

        if pos_gostaria == -1:
            return Constantes.ERRO_ACAO_INEXISTENTE

        for x in range(pos_gostaria):
            if ator == '':
                ator = palavras[x]
            else:
                ator = ator + ' ' + palavras[x]

        if pos_para > -1:
            while pos_gostaria < pos_para:
                if acao == '':
                    acao = palavras[pos_gostaria]
                    pos_gostaria = pos_gostaria + 1
                else:
                    acao = acao + ' ' + palavras[pos_gostaria]
                    pos_gostaria = pos_gostaria + 1
        else:
            while pos_gostaria < len(palavras):
                if acao == '':
                    acao = palavras[pos_gostaria]
                    pos_gostaria = pos_gostaria + 1
                else:
                    acao = acao + ' ' + palavras[pos_gostaria]
                    pos_gostaria = pos_gostaria + 1

        if pos_para > -1:
            while pos_para < len(palavras):
                if finalidade == '':
                    finalidade = palavras[pos_para]
                    pos_para = pos_para + 1
                else:
                    finalidade = finalidade + ' ' + palavras[pos_para]
                    pos_para = pos_para + 1

        sentencas.append(ator)
        sentencas.append(acao)

        if finalidade != '':
            sentencas.append(finalidade)

        return sentencas


    # Os cenários devem ter suas sentenças separadas através de palavras-chave para que cada sentença seja avaliada independentemente
    # Palavras-chave:
    # Dado/Given -> primeira sentença, identificará a pré-condição
    # Quando/When -> segunda sentença, identificará a ação
    # Então/Then -> terceira sentença, identificará a finalidade
    def separar_sentencas_cenario(self, texto):
        sentencas = []
        palavras = texto.split()

        pos_dado = -1
        pos_quando = -1
        pos_entao = -1

        for p in palavras:
            if (p.lower() == 'dado' or  p.lower() == 'given') and pos_dado == -1:
                pos_dado = palavras.index(p)
            elif (p.lower() == 'quando' or p.lower() == 'when') and pos_quando == -1:
                pos_quando = palavras.index(p)
            elif (p.lower() == 'então' or p.lower() == 'then') and pos_entao == -1:
                pos_entao = palavras.index(p)

        preCondicao = ''
        acao = ''
        finalidade = ''

        if pos_dado == -1:
            return Constantes.ERRO_PRECONDICAO_INEXISTENTE

        if pos_quando == -1:
            return Constantes.ERRO_ACAO_INEXISTENTE_CENARIO

        if pos_entao == -1:
            return Constantes.ERRO_FINALIDADE_INEXISTENTE_CENARIO

        if not ((pos_dado < pos_quando) and (pos_quando < pos_entao)):
             return Constantes.ERRO_ORDENACAO_CENARIO        

        for x in range(pos_quando):
            if preCondicao == '':
                preCondicao = palavras[x]
            else:
                preCondicao = preCondicao + ' ' + palavras[x]

        while pos_quando < pos_entao:
            if acao == '':
                acao = palavras[pos_quando]
                pos_quando = pos_quando + 1
            else:
                acao = acao + ' ' + palavras[pos_quando]
                pos_quando = pos_quando + 1
       

        while pos_entao < len(palavras):
            if finalidade == '':
                finalidade = palavras[pos_entao]
                pos_entao = pos_entao + 1
            else:
                finalidade = finalidade + ' ' + palavras[pos_entao]
                pos_entao = pos_entao + 1

        sentencas.append(preCondicao)
        sentencas.append(acao)

        if finalidade != '':
            sentencas.append(finalidade)

        return sentencas

    
    def formatar_tempo(self, start, end):
        return round(end - start, 5).__str__().replace('.',',') + ' segundos'
    
        
    def verifica_erros_historia(self, bem_formada, atomica, minima, ator, acao, finalidade):
        erros = ''
        if not bem_formada:
            erros = 'A história não é Bem formada. '
        if not atomica:
            erros = erros + 'A história não é Atômica. '
        if not minima:
            erros = erros + 'A história não é Mínima. '
        if ator == Constantes.ERRO_ATOR_INCONSISTENTE_COM_ACAO:
            erros = erros + Constantes.ERRO_ATOR_INCONSISTENTE_COM_ACAO + ' '
        if ator == Constantes.ERRO_ATOR_INCONSISTENTE:
            erros = erros + Constantes.ERRO_ATOR_INCONSISTENTE + ' '
        if acao == Constantes.ERRO_ACAO_INCONSISTENTE:
            erros = erros + Constantes.ERRO_ACAO_INCONSISTENTE + ' '
        if finalidade == Constantes.ERRO_FINALIDADE_INCONSISTENTE:
            erros = erros + Constantes.ERRO_FINALIDADE_INCONSISTENTE + ' '
        if bem_formada and atomica and minima and ator != Constantes.ERRO_ATOR_INCONSISTENTE and ator != Constantes.ERRO_ATOR_INCONSISTENTE_COM_ACAO  and acao != Constantes.ERRO_ACAO_INCONSISTENTE and finalidade != Constantes.ERRO_FINALIDADE_INCONSISTENTE:
            return None
        
        return erros

    
    def verifica_erros_cenario(self, bem_formada, atomica, minima, precondicao, acao, finalidade):
        erros = ''
        if not bem_formada:
            erros = 'O cenário não é Bem formada. '
        if not atomica:
            erros = erros + 'O cenário não é Atômica. '
        if not minima:
            erros = erros + 'O cenário não é Mínima. '
        if precondicao == Constantes.ERRO_PRECONDICAO_INCONSISTENTE:
            erros = erros + Constantes.ERRO_PRECONDICAO_INCONSISTENTE + ' '
        if acao == Constantes.ERRO_ACAO_INCONSISTENTE_2:
            erros = erros + Constantes.ERRO_ACAO_INCONSISTENTE_2 + ' '
        if acao == Constantes.ERRO_ACAO_INCONSISTENTE_3:
            erros = erros + Constantes.ERRO_ACAO_INCONSISTENTE_3 + ' '
        if finalidade == Constantes.ERRO_FINALIDADE_INCONSISTENTE_2:
            erros = erros + Constantes.ERRO_FINALIDADE_INCONSISTENTE_2 + ' '
        if finalidade == Constantes.ERRO_ACAO_INCONSISTENTE_3:
            erros = erros + Constantes.ERRO_FINALIDADE_INCONSISTENTE_2 + ' '
        if bem_formada and atomica and minima and precondicao != Constantes.ERRO_PRECONDICAO_INCONSISTENTE and acao != Constantes.ERRO_ACAO_INCONSISTENTE_2 and acao != Constantes.ERRO_ACAO_INCONSISTENTE_3 and finalidade != Constantes.ERRO_FINALIDADE_INCONSISTENTE_2 and finalidade != Constantes.ERRO_ACAO_INCONSISTENTE_3:
            return None
        
        return erros

    def valida_ator_historia(self, tags):
        substantivo = False
        pronome = False
        preposicao = False
        artigo = False
        verbo = False
        ator = ''

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
            elif tag.classe == Constantes.VERBO or tag.classe == Constantes.VERBO_AUX:
                verbo = True

        if verbo:
            return Constantes.ERRO_ATOR_INCONSISTENTE_COM_ACAO           
        elif substantivo and (pronome or preposicao or artigo):
            return ator
        else:
            return Constantes.ERRO_ATOR_INCONSISTENTE


    def extrair_ator(self, tags):
        atores = ''
        for tag in tags:
            if tag.classe == Constantes.SUBSTANTIVO:
                if atores == '':
                    atores = tag.palavra
                else:
                    atores = atores + ', ' + tag.palavra
        
        return atores

    
    def extrair_acao(self, tags):
        acao = ''
        for tag in tags:
            if acao == '':
                acao = tag.palavra
            else:
                acao = acao + ' ' + tag.palavra

        return acao


    def extrair_finalidade(self, tags):
        finalidade = ''

        for tag in tags:
            if finalidade == '':
                finalidade = tag.palavra
            else:
                finalidade = finalidade + ' ' + tag.palavra

        return finalidade


    def extrair_preCondicao(self, tags):
        preCondicao = ''

        for tag in tags:
            if preCondicao == '':
                preCondicao = tag.palavra
            else:
                preCondicao = preCondicao + ' ' + tag.palavra

        return preCondicao

    
    def valida_precondicao_cenario(self, tags):
        substantivo = False
        pronome = False
        preposicao = False
        artigo = False
        precondicao = ''
        
        for tag in tags:
            if tag.classe == Constantes.SUBSTANTIVO or tag.classe == Constantes.ARTIGO or tag.classe == Constantes.PRONOME or tag.classe == Constantes.CONJUNCAO or tag.classe == Constantes.PREPOSICAO or tag.classe == Constantes.VERBO or tag.classe == Constantes.VERBO_AUX:
                if precondicao == '':
                    precondicao = tag.palavra
                else:
                    precondicao = precondicao + ' ' + tag.palavra
            
            if tag.classe == Constantes.SUBSTANTIVO:
                substantivo = True
            elif tag.classe == Constantes.PRONOME:
                pronome = True
            elif tag.classe == Constantes.PREPOSICAO:
                preposicao = True
            elif tag.classe == Constantes.ARTIGO:
                artigo = True
                
        if substantivo and (pronome or preposicao or artigo):
            return precondicao
            
        return Constantes.ERRO_PRECONDICAO_INCONSISTENTE


    def valida_acao_historia(self, tags):
        acao = ''
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
            
        if verbo and substantivo and pronome and (preposicao or adverbio):        
            return acao
        else:
            return Constantes.ERRO_ACAO_INCONSISTENTE

    
    def valida_finalidade_historia(self, tags):
        verbo = False
        substantivo = False
        pronome = False
        preposicao = False
        adverbio = False
        finalidade = ''

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

        else:
            return Constantes.ERRO_FINALIDADE_INCONSISTENTE

    # Função responsável para verificar o terceiro critério de qualidade: Mínima
    # Uma história é mínima quando contém apenas as informações referentes ao critério de qualidade Bem Formada, qualquer informação extra como comentários 
    # e descrição esperada do comportamento deverá ser deixada de lado.
    def verifica_C3_historia(self, sentencas_processadas, bem_formada):

        if not bem_formada:
            return False

        for s in sentencas_processadas:
            if len(s) > 10:
                return False        
        
        return True

    
    # Função responsável para verificar o terceiro critério de qualidade: Mínima
    # Um cenário é mínima quando contém apenas as informações referentes ao critério de qualidade Bem Formada, qualquer informação extra como comentários e descrição esperada do comportamento deverá ser deixada de lado.
    # É verificado quantas vezes o DADO/QUANDO/ENTÃO é chamado, caso tenha sido chamado mais que uma vez cada, o cenário não é mínimo
    def verifica_C3_cenario(self, sentencas_processadas, bem_formada):
        if not bem_formada:
            return False

        for s in sentencas_processadas:
            if len(s) > 25:
                return False        
        
        return True


    def retorna_erro_historia(self, historia, tecnologia, erro, tempo):
        return ResponseHistoria(historia, tecnologia, tempo, False, False, False, None, None, None, None, erro)

    def retorna_erro_cenario(self, cenario, tecnologia, erro, tempo):
        return ResponseHistoria(cenario, tecnologia, tempo, False, False, False, None, None, None, None, erro)  

    
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
    def verifica_C1_historia(self, sentencas_processadas):
        if len(sentencas_processadas) < 2:
            return False
        
        finalidade = None
        ator = utils.retorna_ator_historia(sentencas_processadas[0])
        acao = utils.retorna_acao_historia(sentencas_processadas[1])
        if len(sentencas_processadas) > 2:
            finalidade =  utils.retorna_finalidade_historia(sentencas_processadas[2])
        
        if ator != Constantes.ERRO_ATOR_INCONSISTENTE and acao != Constantes.ERRO_ACAO_INCONSISTENTE and finalidade != Constantes.ERRO_FINALIDADE_INCONSISTENTE:
            return True
        
        return False
    

    def verifica_C1_cenario(self, sentencas_processadas):
        if len(sentencas_processadas) < 3:
            return False
        
        precondicao = utils.retorna_precondicao_cenario(sentencas_processadas[0])
        acao = utils.retorna_acao_cenario(sentencas_processadas[1])
        finalidade =  utils.retorna_finalidade_cenario(sentencas_processadas[2])
        
        if precondicao != Constantes.ERRO_PRECONDICAO_INCONSISTENTE and acao != Constantes.ERRO_ACAO_INCONSISTENTE_2 and acao != Constantes.ERRO_ACAO_INCONSISTENTE_3  and finalidade != Constantes.ERRO_ACAO_INCONSISTENTE_3:
            return True
        
        return False
    
    
    # Função responsável para verificar o segundo critério de qualidade: Atômica
    # Uma história é atômica quando há apenas um objetivo na tarefa
    # Para validar se a história de usuário é atômica, as sentenças são separadas e em seguida é verificado se a segunda sentença possui menos que 3 verbos
    # Caso a sentença não se enquadre no templete de ação, a história de usuário não será atômica
    def verifica_C2_historia(self, sentencas_processadas):
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
    def verifica_C2_cenario(self, tags):
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
    def retorna_ator_historia(self, tags):
        return utils.valida_ator_historia(tags)

        
    # Conforme o layout de cenário (Dado/Quando/Então), a pré-condição deverá ser identificado na primeira sentença
    # A palavra Dado/Given também deve estar presente
    def retorna_precondicao_cenario(self, tags):
        return utils.valida_precondicao_cenario(tags)
       
        
    # Conforme layout de Cohn, uma história de usuário deve ser escrita em no máximo 3 sentenças, 
    # a ação deverá ser identificado na segunda sentença
    def retorna_acao_historia(self, tags):
        return utils.valida_acao_historia(tags)

        
    # Conforme o layout de cenário (Dado/Quando/Então), a ação deverá ser identificada em uma sentença posterior a sentença do ator
    # A palavra Quando/When também deve estar presente nessa sentença
    def retorna_acao_cenario(self, tags):
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
    def retorna_finalidade_historia(self, tags):
            return utils.valida_finalidade_historia(tags)
   
    # Conforme o layout de cenário (Dado/Quando/Então), a finalidade deverá ser identificada em uma sentença posterior a sentença do ator e da ação
    # A palavra Então/Then também deve estar presente nessa sentença
    def retorna_finalidade_cenario(self, tags):
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


utils = UtilsService()