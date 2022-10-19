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

        print('---------- ' + tecnologia + ' ----------')
        
        for tag in tagsets:
            print(tag)
        
        print('-----------------------')

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

    
    def separar_sentencas(self, texto):
        return texto.split(',')

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
            return Constantes.ERRO_ATOR_INCONSISTENTE

        if pos_gostaria == -1:
            return Constantes.ERRO_ACAO_INCONSISTENTE

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

    
    def formatar_tempo(self, start, end):
        return round(end - start, 5).__str__().replace('.',',') + ' segundos'
    
            
    def limpar_mensagem_de_erro(self, input):
        if input == Constantes.ERRO_ATOR_INCONSISTENTE:
            return None
        if input == Constantes.ERRO_PRECONDICAO_INCONSISTENTE:
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
        
        
    def verifica_ator_e_acao_e_finalidade_ja_encontrados(self, sentenca, ator_encontrado, acao_encontrada, finalidade_encontrada):
        return ((Constantes.DADO.lower() in sentenca.lower() or Constantes.GIVEN.lower() in sentenca.lower()) and ator_encontrado) or ((Constantes.QUANDO.lower() in sentenca.lower() or Constantes.WHEN.lower() in sentenca.lower()) and acao_encontrada) or ((Constantes.ENTAO.lower() in sentenca.lower() or Constantes.THEN.lower() in sentenca.lower()) and finalidade_encontrada)


    def verifica_erros_historia(self, bem_formada, atomica, minima, ator, acao, finalidade):
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

    
    def verifica_erros_cenario(self, bem_formada, atomica, minima, precondicao, acao, finalidade):
        erros = ''
        if not bem_formada:
            erros = 'O cenário não atende ao primeiro critério de qualidade que é Bem formada. '
        if not atomica:
            erros = erros + 'O cenário não atende ao segundo critério de qualidade que é Atômica. '
        if not minima:
            erros = erros + 'O cenário não atende ao terceiro critério de qualidade que é Mínima. '
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
                    
        if substantivo and (pronome or preposicao or artigo):
            return ator
        else:
            return Constantes.ERRO_ATOR_INCONSISTENTE

    
    def valida_precondicao_cenario(self, tags, sentenca):
        dado_given = False
        substantivo = False
        pronome = False
        preposicao = False
        artigo = False
        precondicao = ''
        
        if Constantes.DADO.lower() in sentenca.lower() or Constantes.GIVEN.lower() in sentenca.lower():
            dado_given = True
            
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
                
        if dado_given and substantivo and (pronome or preposicao or artigo):
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
    def verifica_C3_historia(self, sentencas, bem_formada):
        if bem_formada and len(sentencas) <= 3:
            return True
        
        return False

    
    # Função responsável para verificar o terceiro critério de qualidade: Mínima
    # Um cenário é mínima quando contém apenas as informações referentes ao critério de qualidade Bem Formada, qualquer informação extra como comentários e descrição esperada do comportamento deverá ser deixada de lado.
    # É verificado quantas vezes o DADO/QUANDO/ENTÃO é chamado, caso tenha sido chamado mais que uma vez cada, o cenário não é mínimo
    def verifica_C3_cenario(self, texto, bem_formada):
        sentencas = utils.separar_sentencas(texto)
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


    def retorna_erro_historia(self, historia, tecnologia, erro):
        return ResponseHistoria(historia, tecnologia, None, False, False, False, None, None, None, erro)

    def retorna_erro_cenario(self, cenario, tecnologia, erro):
        return ResponseHistoria(cenario, tecnologia, None, False, False, False, None, None, None, erro)  


utils = UtilsService()