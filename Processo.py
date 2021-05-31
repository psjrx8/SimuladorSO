class Processo:

    #ToDo: Paginas (Processo de paginacao nao foi feito)

    def __init__(self, id, tempoChegada, tempoExecucao, quantum, deadline, prioridade, sobrecarga, paginas):
        self.__id = id
        self.__tempoChegada = tempoChegada
        self.__tempoExecucao = tempoExecucao
        self.__quantum = quantum
        self.__tempoExecutado = 0
        self.__logUsoProcessador = []
        self.__turnRound = 0

        if deadline is not None:
            self.__deadline = deadline
        if prioridade is not None:
            self.__prioridade = prioridade
        if sobrecarga is not None:
            self.__sobrecarga = sobrecarga
        if paginas is not None:
            self.__paginas = paginas
        else:
            self.__paginas = []
    
    def getId(self):
        return self.__id

    def setTempoChegada(self, tempoChegada):
        self.__tempoChegada = tempoChegada
    
    def getTempoChegada(self):
        return self.__tempoChegada
    
    def setTempoExecucao(self, tempoExecucao):
        self.__tempoExecucao = tempoExecucao
    
    def getTempoExecucao(self):
        return self.__tempoExecucao
    
    def setDeadline(self, deadline):
        self.__deadline = deadline

    def getDeadline(self):
        return self.__deadline
    
    def setPrioridade(self, prioridade):
        self.__prioridade = prioridade

    def getPrioridade(self):
        return self.__prioridade

    def setQuantum(self, quantum):
        self.__quantum = quantum

    def getQuantum(self):
        return self.__quantum
    
    def setSobrecarga(self, sobrecarga):
        self.__sobrecarga = sobrecarga

    def getSobrecarga(self):
        return self.__sobrecarga

    def setTempoExecutado(self, tempoExecutado):
        self.__tempoExecutado = tempoExecutado

    def getTempoExecutado(self):
        return self.__tempoExecutado

    def setTempoTermino(self, tempoTermino):
        self.__tempoTermino = tempoTermino

    def getTempoTermino(self):
        return self.__tempoTermino
    
    def setPaginas(self, paginas):
        self.__paginas = paginas

    def getPaginas(self):
        return self.__paginas
    
    def setLogUsoProcessador(self, inicio, fim):
        if self.__tempoExecutado < self.__tempoExecucao:
            if self.__statusExecucao == "Pausando":
                self.__logUsoProcessador.append([inicio, fim, "Executando"])
                self.__statusExecucao = "Pausado"
            elif self.__statusExecucao == "Finalizando":
                self.__logUsoProcessador.append([inicio, fim, "Executando"])
                self.__statusExecucao = "Finalizado"
            else: self.__logUsoProcessador.append([inicio, fim, self.__statusExecucao])
    
    def getLogUsoProcessador(self):
        return self.__logUsoProcessador

    def setStatusExecucao(self, statusExecucao):
        self.__statusExecucao = statusExecucao
