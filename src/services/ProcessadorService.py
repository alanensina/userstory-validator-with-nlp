import timeit
from src.services.NLTKService import NLTKService
from src.services.SpacyService import SpacyService
from src.services.UtilsService import UtilsService
from src.classes.ResponseHistoria import ResponseHistoria
from src.classes.ResponseCenario import ResponseCenario
from src.classes import Constantes

class ProcessadorService():
    
    def __init__(self):
        pass   
         
    
    def processar(self, payload, type):
        
        response = []
        
        for p in payload:
            idioma = p.get('idioma')
            
            if type == 'historia':
                historia = p.get('historia')
                response.append(ProcessadorService.processarHistoria(idioma, historia, Constantes.NLTK))
                response.append(ProcessadorService.processarHistoria(idioma, historia, Constantes.SPACY))
            elif type == 'cenario':
                cenario = p.get('cenario')
                response.append(ProcessadorService.processarCenario(idioma, cenario, Constantes.NLTK))
                response.append(ProcessadorService.processarCenario(idioma, cenario, Constantes.SPACY))
                
        return response
    
    
    def processarHistoria(idioma:str, historia:str, tecnologia:str):
        start = timeit.default_timer()
        finalidade = None
        erros = None

        sentencas = utils.separar_sentencas_historia(historia)
        
        sentencas_processadas = []
        
        if len(sentencas) > 1 and not utils.verifica_erro_separacao(sentencas):
            x = 0

            while x < len(sentencas):
                if tecnologia == Constantes.NLTK:
                    sentencas_processadas.append(NLTKService.processar(sentencas[x], idioma))
                if tecnologia == Constantes.SPACY:
                    sentencas_processadas.append(SpacyService.processar(sentencas[x], idioma))
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
                return ResponseHistoria(historia, tecnologia, tempo, bem_formada, atomica, minima, ator, acao, finalidade, tags, erros)
            else:
                return ResponseHistoria(historia, tecnologia, tempo, bem_formada, atomica, minima, None, None, None, tags, erros)
        else:
            end = timeit.default_timer()  
            tempo = utils.formatar_tempo(start, end)
            return utils.retorna_erro_historia(historia, tecnologia, sentencas, tempo)
        
    
    def processarCenario(idioma:str, cenario:str, tecnologia:str):
        start = timeit.default_timer()

        sentencas = utils.separar_sentencas_cenario(cenario)
        
        sentencas_processadas = []

        if len(sentencas) > 1 and not utils.verifica_erro_separacao(sentencas):
            x = 0

            while x < len(sentencas):
                if tecnologia == Constantes.NLTK:
                    sentencas_processadas.append(NLTKService.processar(sentencas[x], idioma))
                if tecnologia == Constantes.SPACY:
                    sentencas_processadas.append(SpacyService.processar(sentencas[x], idioma))
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
                return ResponseCenario(cenario, tecnologia, tempo, bem_formada, atomica, minima, precondicao, acao, finalidade, tags, erros)
            else:
                return ResponseCenario(cenario, tecnologia, tempo, bem_formada, atomica, minima, None, None, None, tags, erros)
        else:
            end = timeit.default_timer()  
            tempo = utils.formatar_tempo(start, end)
            return utils.retorna_erro_historia(cenario, tecnologia, sentencas, tempo)    
    

processador = ProcessadorService()
utils = UtilsService()