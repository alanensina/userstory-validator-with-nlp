import spacy, timeit
from src.classes.Response import Response
from src.classes import Constantes
from src.services.Utils import utils

class SPACY:
    def processarHistoria(idioma:str, historia:str):
        start = timeit.default_timer()
        
        bem_formada = SPACY.verifica_C1_historia(historia, idioma)
        atomica = SPACY.verifica_C2_historia(historia, idioma)
        minima = utils.verifica_C3_historia(historia, bem_formada)
        ator = SPACY.retorna_ator_historia(historia, idioma)    
        acao = SPACY.retorna_acao_historia(historia, idioma)      
        finalidade = SPACY.retorna_finalidade_historia(historia, idioma)  
        erros = utils.verifica_erros_historia(bem_formada, atomica, minima, ator, acao, finalidade)
        end = timeit.default_timer()  
        tempo = utils.formatar_tempo(start, end)

        if erros == None:
            return Response(historia, Constantes.SPACY, tempo, bem_formada, atomica, minima, ator, acao, finalidade, erros)
        else:
            ator = utils.limpar_mensagem_de_erro(ator)
            acao = utils.limpar_mensagem_de_erro(acao)   
            finalidade = utils.limpar_mensagem_de_erro(finalidade)
            return Response(historia, Constantes.SPACY, tempo, bem_formada, atomica, minima, ator, acao, finalidade, erros) 

    
    def processarCenario(idioma:str, cenario:str):
        SPACY.processar(cenario, idioma)
        return Response(cenario, 'spaCy', 'TESTE', True, True, True, 'TESTE', 'TESTE', 'TESTE', None)


    def processar(texto, idioma):

        if idioma == Constantes.EN:
            nlp = spacy.load(Constantes.SPACY_EN)
            doc = nlp(texto)
            return utils.unificar_tagset(doc, Constantes.SPACY)

        elif idioma == Constantes.PTBR: 
            nlp = spacy.load(Constantes.SPACY_PT)
            doc = nlp(texto)
            return utils.unificar_tagset(doc, Constantes.SPACY)
        
        return None

    # Conforme layout de Cohn, uma história de usuário deve ser escrita em no máximo 3 sentenças, 
    # o ator deverá ser identificado na primeira sentença
    def retorna_ator_historia(texto, idioma):
        sentencas = utils.separar_sentencas(texto)
        sentenca = sentencas[0]
        tags = SPACY.processar(sentenca, idioma)
        
        return utils.valida_ator_historia(tags)

    
     # Conforme layout de Cohn, uma história de usuário deve ser escrita em no máximo 3 sentenças, 
    # a ação deverá ser identificado na segunda sentença
    def retorna_acao_historia(texto, idioma):
        sentencas = utils.separar_sentencas(texto)
        
        if len(sentencas) >= 2:
            sentenca = sentencas[1]
        else:
            return Constantes.ERRO_ACAO_INCONSISTENTE

        tags = SPACY.processar(sentenca, idioma)
        
        return utils.valida_acao_historia(tags)


    # Conforme layout de Cohn, uma história de usuário deve ser escrita em no máximo 3 sentenças, 
    # a finalidade é opcional, mas caso ocorra deverá ser identificada na terceira sentença
    def retorna_finalidade_historia(texto, idioma):
        sentencas = utils.separar_sentencas(texto)

        if len(sentencas) >= 3:
            sentenca = sentencas[2]
            tags = SPACY.processar(sentenca, idioma)
            return utils.valida_finalidade_historia(tags)
        return None

    
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
        
        ator = SPACY.retorna_ator_historia(texto, idioma)
        acao = SPACY.retorna_acao_historia(texto, idioma)
        finalidade =  SPACY.retorna_finalidade_historia(texto, idioma)
        
        if ator != Constantes.ERRO_ATOR_INCONSISTENTE and acao != Constantes.ERRO_ACAO_INCONSISTENTE and finalidade != Constantes.ERRO_FINALIDADE_INCONSISTENTE:
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
        tags = SPACY.processar(sentencas[1], idioma)

        for tag in tags:
            if tag.classe == Constantes.VERBO:
                verbos = verbos + 1
            
        return (verbos < 3 and idioma == Constantes.PTBR) or (verbos <= 3 and idioma == Constantes.EN)