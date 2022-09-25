class Palavra():
    def __init__(self, palavra, tagset, classe):
        self._palavra = palavra
        self._tagset = tagset
        self._classe = classe
        
    def __str__(self):
        return 'Palavra: ' + self.palavra + ', Tagset original: ' + self.tagset + ', classe gramatical: ' + self.classe
    
    @property
    def palavra(self):
        return self._palavra
    
    @property
    def tagset(self):
        return self._tagset
    
    @property
    def classe(self):
        return self._classe