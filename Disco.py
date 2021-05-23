class Disco:

    def __init__(self, tamanhoDisco) :
        self.__memoriaVirtual = [None] * tamanhoDisco
    
    def getMemoriaVirtual(self):
        return self.__memoriaVirtual
    
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
            print("Processo p" + str(processo.getId()) + " alocado na memoria virtual")
        else:
            print("Disco nao possui espaco suficiente para alocacao do processo " + str(processo.getId()))
        
        return base

    def liberarProcessoDoDisco(self, processo):

        controleLiberacao = False

        for i in range(len(self.__memoriaVirtual)):
            
            if self.__memoriaVirtual[i] != None:
                if self.__memoriaVirtual[i].getProcessoId() == processo.getId():
                    self.__memoriaVirtual[i] = None
                    controleLiberacao = True

        
        if controleLiberacao:
            print("Processo p" + str(processo.getId()) + " liberado na memoria virtual")
        
        return processo