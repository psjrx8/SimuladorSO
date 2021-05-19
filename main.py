import Processo
import Pagina
import RAM
import Disco
import Escalonamento

def criaProcessosTeste(numeroProcessos):
    processos = []
    
    for i in range(numeroProcessos):

        paginas = []
        for j in range(10):
            p = Pagina.Pagina(i + 1, j)
            paginas.append(p)

        p = Processo.Processo(i + 1, 0, i + 3, 2, i + i % 2, 2, 1, paginas)

        processos.append(p)

    return processos

def criaProcessos(numeroProcessos, tipoEscalonamento):
    processos = []

    for i in range(numeroProcessos):
        index = str(i + 1)
        
        #Todo: Verificar dados invalidos para inclusao do processo
        #Todo: Paginacao
        #Duvida: Acredito que o quantum e do processador e nao do processo, VERIFICAR
        #Duvida: Acredito que a sobrecarga (overhead) e do processador e nao do processo, VERIFICAR

        tempoChegada = int(input("Digite o tempo de chegada do processo " + index + ": "))
        tempoExecucao = int(input("Digite o tempo de execucao do processo " + index + ": "))
        quantum = int(input("Digite o quantum do processo "+ index + ": "))
        
        deadline = None
        prioridade = None
        sobrecarga = None
        if tipoEscalonamento not in [1,2]:
            deadline = int(input("Digite o deadline do processo " + index + ": "))
            prioridade = int(input("Digite o prioridade do processo " + index + ": "))
            sobrecarga = int(input("Digite o sobrecarga do processo " + index + ": "))

        paginas = criaPaginasProcesso(index)
        print(" ")
        
        p = Processo.Processo(index, tempoChegada, tempoExecucao, quantum, deadline, prioridade, sobrecarga, paginas)

        processos.append(p)

    return processos

def criaPaginasProcesso(processoId):
    #Todo: Limitar numero a 10 o numero de paginas
    numeroPaginas = int(input("Digite o numero de paginas do processo " + processoId + ": "))
    paginas = []
    for i in range(numeroPaginas):
        p = Pagina.Pagina(processoId, i)
        paginas.append(p)
    return paginas



def executar(tipoEscalonamento, tipoPaginacao, processos):

    turnRound = 0 #Media do tempo de execucao

    if tipoEscalonamento == 1:
        Escalonamento.FIFO(tipoPaginacao, processos, memoriaRAM, memoriaVirtual)
    elif tipoEscalonamento == 2:
        Escalonamento.SJF(tipoPaginacao, processos, memoriaRAM, memoriaVirtual)
    elif tipoEscalonamento == 3:
        Escalonamento.robinRound(tipoPaginacao, processos, memoriaRAM, memoriaVirtual)
    elif tipoEscalonamento == 4:
        Escalonamento.EDF(tipoPaginacao, processos, memoriaRAM, memoriaVirtual)
    
    for p in processos:
        turnRound += p.getTempoTermino()
    turnRound = turnRound / len(processos)

    print(" ")
    print("Turnaround dos " + str(len(processos)) + " processos: " + str(turnRound))


memoriaRAM = RAM.RAM()
memoriaVirtual = Disco.Disco(100)

processos = []

try:
    tipoEscalonamento = int(input("Digite o algoritmo de escalonamento desejado (1-FIFO | 2-SJF | 3-Robin Round | 4-EDF): "))    
except: 
    print("Tipo de algoritmo nao identificado")

if tipoEscalonamento not in [1,2,3,4]:
    print("Tipo de algoritmo nao identificado")

try:
    tipoPaginacao = int(input("Digite o algoritmo de paginacao desejado (1-FIFO | 2-MRU): "))
except: 
    print("Tipo de algoritmo nao identificado")

if tipoPaginacao not in [1,2]:
    print("Tipo de algoritmo nao identificado")

try:
    numeroProcessos = int(input("Digite a quantidade de processos: "))    
except: 
    print("Numero invalido")

print(" ")

#processos = criaProcessos(numeroProcessos, tipoEscalonamento)

processos = criaProcessosTeste(numeroProcessos)

executar(tipoEscalonamento, tipoPaginacao, processos)