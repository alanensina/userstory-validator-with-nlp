class Palavra():
    def __init__(self, palavra, tagset, classe):
        self.palavra = palavra
        self.tagset = tagset
        self.classe = classe
        
    def __str__(self):
        return 'Palavra: ' + self.palavra + ', Tagset original: ' + self.tagset + ', classe gramatical: ' + self.classe