class Disco:

    def __init__(self, tamanhoDisco) :
        self.__memoriaVirtual = [None] * tamanhoDisco
    
    def getMemoriaVirtual(self):
        return self.__id
    
    def setEndereco(self, endereco, posicao):
        self.__memoriaVirtual[posicao] = endereco
    
    def getEndereco(self, posicao):
        return self.__memoriaVirtual[posicao]
    
    def alocarProcessoNoDisco(self, processo):
        paginas = processo.getPaginas()
        tamanhoProcesso = len(paginas)
        base = -1 #Base da memoria aplicada
        deslocamento = 0 #Deslocamento ate a posicao final de alocacao do processo na memoria

        for i in range(len(self.__memoriaVirtual)):
            if deslocamento != tamanhoProcesso:
                if self.__memoriaVirtual[i] == None:
                    deslocamento += 1
                    if base == -1:
                        base = i
                else:
                    deslocamento = 0
                    base = -1
        
        if deslocamento == tamanhoProcesso and base != -1:
            for i in range(base, base + deslocamento):
                self.__memoriaVirtual[i] = paginas[base - i]
            print("Processo " + str(processo.getId()) + " alocado na memoria virtual")
        else:
            print("Disco nao possui espaco suficiente para alocacao do processo " + str(processo.getId()))
        
        return base