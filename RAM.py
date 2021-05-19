class RAM:

    def __init__(self) :
        #Tamanho da RAM definido no escopo
        #Paginas de 4k, RAM total de 200k (Numero maximo de paginas 50)
        self.__memoria = [None] * 50
        self.__filaAlocacaoProcesso = []
    
    def getMemoriaVirtual(self):
        return self.__id
    
    def setEndereco(self, pagina, posicao):
        self.__memoria[posicao] = pagina
    
    def getEndereco(self, posicao):
        return self.__memoria[posicao]

    #Todo: Otimizar metodo de busca
    def alocarProcessoNaMemoria(self, processo):
        paginas = processo.getPaginas()
        tamanhoProcesso = len(paginas)
        base = -1 #Base da memoria aplicada
        deslocamento = 0 #Deslocamento ate a posicao final de alocacao do processo na memoria

        for i in range(len(self.__memoria)):
            
            areaMemoria = self.__memoria[i]
            if deslocamento != tamanhoProcesso:
                if areaMemoria == None:
                    deslocamento += 1
                    if base == -1:
                        base = i
                else:
                    deslocamento = 0
                    base = -1
            
            if areaMemoria != None:
                if areaMemoria.getProcessoId() == processo.getId():
                    base = i
                    deslocamento = tamanhoProcesso
        
        if deslocamento == tamanhoProcesso and base != -1:
            for i in range(base, base + deslocamento):
                self.__memoria[i] = paginas[base - i]
            print("Processo p" + str(processo.getId()) + " alocado na memoria")
            self.__filaAlocacaoProcesso.append(processo)
        else:
            base = -1
            print("Processo p" + str(processo.getId()) + " nao pode ser alocado em memoria")
        
        return base
    
    #Todo: Otimizar metodo de busca
    def liberarProcessoDaMemoria(self):

        #FIFO
        if len(self.__filaAlocacaoProcesso) > 0:
            processo = self.__filaAlocacaoProcesso.pop(0)
            controleLiberacao = False

            for i in range(len(self.__memoria)):
                
                if self.__memoria[i] != None:
                    if self.__memoria[i].getProcessoId() == processo.getId():
                        self.__memoria[i] = None
                controleLiberacao = True

            
            if controleLiberacao:
                print("Processo p" + str(processo.getId()) + " liberado da memoria")

            return processo

        else:
            print("Nao ha processo alocado em memoria")
        
        return None
        
    #Todo: Otimizar metodo de busca
    def verificarProcessoNaMemoria(self, processo):
        base = -1 #Base da memoria aplicada
        flagAlocado = False
        i = 0

        for i in range(len(self.__memoria)):
            if self.__memoria[i] != None and self.__memoria[i].getProcessoId() == processo.getId():
                base = i
                print("Processo p" + str(processo.getId()) + " recuperado da memoria")
                break
        
        return base