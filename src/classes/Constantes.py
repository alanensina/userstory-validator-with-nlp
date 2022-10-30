# Lista de constantes utilizadas
INVALIDO = 'INVÁLIDO'
ARTIGO = 'ARTIGO'
ADJETIVO = 'ADJETIVO'
SUBSTANTIVO = 'SUBSTANTIVO'
NUMERAL = 'NUMERAL'
PRONOME = 'PRONOME'
ADVERBIO = 'ADVÉRBIO'
CONJUNCAO = 'CONJUNÇÃO'
PREPOSICAO = 'PREPOSIÇÃO'
INTERJEICAO = 'INTERJEIÇÃO'
VERBO = 'VERBO'
VERBO_AUX = 'VERBO AUXILIAR'
PARTICIPIO = 'PARTICÍPIO'
PALAVRA_DEN = 'PALAVRA DENOTATIVA'
MOEDA = 'SÍMBOLO DA MOEDA CORRENTE'
NLTK = 'NLTK'
SPACY = 'spaCy'
DADO = 'Dado'
GIVEN = 'Given'
QUANDO = 'quando'
WHEN = 'when'
ENTAO = 'então'
THEN = 'then'

# Constantes spaCy
SPACY_EN = 'en_core_web_sm'
SPACY_PT = 'pt_core_news_sm'

# Idiomas
EN = 'en'
PTBR = 'ptbr'

# Conjunções utilizadas para validação do Critério de Qualidade 2
CONJUNCOES_C2 = ['e', 'and', 'ou', 'or']

# Caracteres inválidos para validação do Critério de Qualidade 3
CARACTERES_INVALIDOS = ['*', '[', ']', '(', ')', '{', '}', '_', ':']

# Mensagens de erro
ERRO_ATOR_INEXISTENTE = 'Ator inexistente. Não foi encontrado as palavras chaves para validação do ator: Eu como/I as ou Como/As.'
ERRO_PRECONDICAO_INEXISTENTE = 'Pré-condição inexistente. Não foi encontrado a palavra chave para validação do pré-condição: Dado/Given'
ERRO_ACAO_INEXISTENTE = 'Ação inexistente. Não foi encontrado a palavra chave para validação da ação: gostaria/would'
ERRO_ACAO_INEXISTENTE_CENARIO = 'Ação inexistente. Não foi encontrado a palavra chave para validação da ação: quando/when'
ERRO_FINALIDADE_INEXISTENTE_CENARIO = 'Finalidade inexistente. Não foi encontrado a palavra chave para validação da finalidade: então/then'
ERRO_ORDENACAO_CENARIO = 'Inconsistência no template de cenário. Ordem das palavras-chave incorretas: Dado/quando/então ou Given/when/then'
ERRO_ATOR_INCONSISTENTE = 'Inconsistência no template de validação do ator.'
ERRO_ATOR_INCONSISTENTE_COM_ACAO = 'Inconsistência no template de validação do ator. Sentença do ator não pode conter verbo'
ERRO_ACAO_INCONSISTENTE = 'Inconsistência no template de validação da ação.'
ERRO_FINALIDADE_INCONSISTENTE = 'Inconsistência no template de validação da finalidade.'
ERRO_FINALIDADE_INCONSISTENTE_2 = 'Inconsistência no template de validação da finalidade.'
ERRO_PRECONDICAO_INCONSISTENTE = 'Inconsistência no template de validação da pré-condição.'
ERRO_ACAO_INCONSISTENTE_2 = 'Inconsistência no template de validação da ação.'
ERRO_ACAO_INCONSISTENTE_3 = 'Inconsistência na validação da ação. Um ações identificadas.'