from xmlrpc.client import Boolean
import nltk, joblib
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from src.classes.Response import Response
from src.classes.Palavra import Palavra
from src.classes import Constantes

class NLTK:
    
    def processarHistoria(idioma:str, historia:str):
        tempo = 'TEMPO' # Iniciar contagem
        texto_processado = NLTK.processar(historia, idioma)
        
        bem_formada = NLTK.verifica_criterio_um(texto_processado)
        atomica = NLTK.verifica_criterio_dois(texto_processado)
        minima = NLTK.verifica_criterio_tres(texto_processado)
        erros = NLTK.verifica_erros(bem_formada, atomica, minima)  
        
        ator = NLTK.retorna_ator(historia, idioma)    
        acao = NLTK.retorna_acao(historia, idioma)      
        finalidade = NLTK.retorna_finalidade(historia, idioma)        
        
        tempo = 'TEMPO' # Finalizar contagem
        return Response(historia, Constantes.NLTK, tempo, bem_formada, atomica, minima, ator, acao, finalidade, erros)
    
    def processarCenario(idioma:str, cenario:str):
        texto_processado = NLTK.processar(cenario, idioma)
        return Response(cenario, Constantes.NLTK, 'TESTE', True, True, True, 'TESTE', 'TESTE', 'TESTE', None)
    
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
        #for tag in tags:
         #   print(tag)
        return tags
    
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
    # Formato esperado: Sujeito + Adjetivo (opcional) + Verbo + Objeto indireto (opcional) + Objeto direto
    # Formato das tagsets:
    # Sujeito -> Substantivo ou pronome
    # Adjetivo (opcional) -> Adjetivo
    # Verbo -> Verbo
    # Objeto indireto (opcional) -> Substantivo ou pronome
    # Objeto direto -> Substantivo ou pronome
    def verifica_criterio_um(tagsets):
        
            
            
        
        
        return True
    
    
    # Função responsável para verificar o segundo critério de qualidade: Atômica
    # Uma história é atômica quando há apenas um objetivo na tarefa
    def verifica_criterio_dois(tagsets):
        
        
        
        
        return True
    
    
    # Função responsável para verificar o terceiro critério de qualidade: Mínima
    # Uma história é mínima quando contém apenas as informações referentes ao critério de qualidade Bem Formada, qualquer informação extra como comentários 
    # e descrição esperada do comportamento deverá ser deixada de lado.
    def verifica_criterio_tres(tagsets):
        
        
        
        
        
        
        return True
    
    def verifica_erros(bem_formada, atomica, minima):
        erros = ''
        if not bem_formada:
            erros = 'A história não atende o primeiro critério de qualidade que é Bem formada. '
        if not atomica:
            erros = erros + 'A história não atende o segundo critério de qualidade que é Atômica. '
        if not minima:
            erros = erros + 'A história não atende o terceiro critério de qualidade que é Mínima.'
        if bem_formada and atomica and minima:
            return None
        else:
            return erros
        
    # Conforme layout de Cohn, uma história de usuário deve ser escrita em no máximo 3 sentenças, 
    # o ator deverá ser identificado na primeira sentença
    def retorna_ator(texto, idioma):
        ator = ''
        sentencas = NLTK.separar_sentencas(texto)
        sentenca = sentencas[0]
        tags = NLTK.processar(sentenca, idioma)
        
        for tag in tags:
            if tag.classe == Constantes.SUBSTANTIVO or tag.classe == Constantes.PRONOME or tag.classe == Constantes.CONJUNCAO:
                if ator == '':
                    ator = tag.palavra
                else:
                    ator = ator + ' ' + tag.palavra
        
        return ator
    
    # Conforme layout de Cohn, uma história de usuário deve ser escrita em no máximo 3 sentenças, 
    # a ação deverá ser identificado na segunda sentença
    def retorna_acao(texto, idioma):
        acao = ''
        sentencas = NLTK.separar_sentencas(texto)
        sentenca = sentencas[1]
        tags = NLTK.processar(sentenca, idioma)
        for tag in tags:
            if tag.classe == Constantes.VERBO or tag.classe == Constantes.SUBSTANTIVO or tag.classe == Constantes.PRONOME or tag.classe == Constantes.CONJUNCAO or tag.classe == Constantes.PREPOSICAO:
                if acao == '':
                    acao = tag.palavra
                else:
                    acao = acao + ' ' + tag.palavra        
        
        return acao
    
    # Conforme layout de Cohn, uma história de usuário deve ser escrita em no máximo 3 sentenças, 
    # a finalidade é opcional, mas caso ocorra deverá ser identificada na terceira sentença
    def retorna_finalidade(texto, idioma):
        finalidade = ''
        sentencas = NLTK.separar_sentencas(texto)
        
        if sentencas.__sizeof__() >= 3:
            sentenca = sentencas[2]
            tags = NLTK.processar(sentenca, idioma)
            for tag in tags:
                if tag.classe == Constantes.VERBO or tag.classe == Constantes.SUBSTANTIVO or tag.classe == Constantes.PRONOME or tag.classe == Constantes.CONJUNCAO or tag.classe == Constantes.PREPOSICAO:
                    if finalidade == '':
                        finalidade = tag.palavra
                    else:
                        finalidade = finalidade + ' ' + tag.palavra 
        
        
        return finalidade
    
    
    def separar_sentencas(texto):
        return texto.split(',')  
            