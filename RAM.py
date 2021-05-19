class RAM:

    def __init__(self) :
        #Tamanho da RAM definido no escopo
        #Paginas de 4k, RAM total de 200k (Numero maximo de paginas 50)
        self.__memoria = [None] * 50
    
    def getMemoriaVirtual(self):
        return self.__id
    
    def setEndereco(self, pagina, posicao):
        self.__memoria[posicao] = pagina
    
    def getEndereco(self, posicao):
        return self.__memoria[posicao]

    def alocarProcessoNaMemoria(self, processo):
        paginas = processo.getPaginas()
        tamanhoProcesso = len(paginas)
        base = -1 #Base da memoria aplicada
        deslocamento = 0 #Deslocamento ate a posicao final de alocacao do processo na memoria
        flagAlocacao = True

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
                    flagAlocacao = False
        
        if deslocamento == tamanhoProcesso and base != -1 and flagAlocacao:
            for i in range(base, base + deslocamento):
                self.__memoria[i] = paginas[base - i]
            print("Processo " + str(processo.getId()) + " alocado na memoria")
        elif not flagAlocacao:
            print("Processo " + str(processo.getId()) + " recuperado da memoria")
        else:
            base = -1
            print("Processo " + str(processo.getId()) + " nao pode ser alocado em memoria real")
        
        return base
        
        
