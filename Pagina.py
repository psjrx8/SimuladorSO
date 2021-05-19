class Pagina:

    def __init__(self, processoId, id):
        self.__processoId = processoId
        self.__id = id
    
    def getProcessoId(self):
        return self.__processoId
    
    def getId(self):
        return self.__id