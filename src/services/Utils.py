from pydoc import Doc
from typing import Any
from src.classes import Constantes
from src.classes.Palavra import Palavra

class Utils():

    def __init__(self):
        pass 

    def unificar_tagset(self, tags, tecnologia):
        tagsets = []

        if tecnologia == Constantes.NLTK:
            for tupla in tags:
                tagsets.append(Palavra(tupla[0], tupla[1], Utils.get_classe_gramatical(tupla[1])))

        elif tecnologia == Constantes.SPACY:
            for token in tags:
                tagsets.append(Palavra(token.text, token.tag_, Utils.get_classe_gramatical(token.tag_))) 

        print('---------- ' + tecnologia + ' ----------')
        
        for tag in tagsets:
            print(tag)
        
        print('-----------------------')

        return tagsets

    # Função responsável em retornar a classe gramatical conforme o tagset
    def get_classe_gramatical(tagset):
          if Utils.verifica_artigo(tagset):
              return Constantes.ARTIGO
          elif Utils.verifica_adjetivo(tagset):
              return Constantes.ADJETIVO
          elif Utils.verifica_substantivo(tagset):
              return Constantes.SUBSTANTIVO
          elif Utils.verifica_numeral(tagset):
              return Constantes.NUMERAL
          elif Utils.verifica_pronome(tagset):
              return Constantes.PRONOME
          elif Utils.verifica_adverbio(tagset):
              return Constantes.ADVERBIO
          elif Utils.verifica_conjuncao(tagset):
              return Constantes.CONJUNCAO
          elif Utils.verifica_preposicao(tagset):
              return Constantes.PREPOSICAO
          elif Utils.verifica_interjeicao(tagset):
              return Constantes.INTERJEICAO
          elif Utils.verifica_verbo(tagset):
              return Constantes.VERBO
          elif Utils.verifica_verbo_aux(tagset):
              return Constantes.VERBO_AUX
          elif Utils.verifica_participio(tagset):
              return Constantes.PARTICIPIO
          elif Utils.verifica_denotativo(tagset):
              return Constantes.PALAVRA_DEN
          elif Utils.verifica_moeda(tagset):
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
    
    
    def formatar_tempo(self, start, end):
        return round(end - start, 5).__str__().replace('.',',') + ' segundos'
    
            
    def limpar_mensagem_de_erro(self, input):
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

    
    def verifica_erros_cenario(self, bem_formada, atomica, minima, ator, acao, finalidade):
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


utils = Utils()