from flask import Flask
from flask_restx import Api

class Server():
    def __init__(self, ):
        self.app = Flask(__name__)
        self.app.config.setdefault('RESTPLUS_MASK_SWAGGER', False)
        self.api = Api(self.app,
                       default='Analisador de História de Usuário',
                       default_label='Endpoints para análise de histórias de usuário',
                       version='1.0',
                       title='Analisador de História de Usuário com PLN',
                       description='API voltada para análise de Histórias de Usuário utilizando Processamento de Linguagem Natural. \n Tecnologias utilizadas: NLTK e spaCy',
                       doc='/analisador')
        
    def run(self, ):
        self.app.run(
            debug=True
            )
        
server = Server()