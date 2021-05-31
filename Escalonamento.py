def alocarProcessoPronto(memoriaRAM, memoriaVirtual, processo, tipoPaginacao):
    enderecoAlocacao = None

    enderecoAlocacao = memoriaRAM.verificarProcessoNaMemoria(processo, tipoPaginacao)
    
    if enderecoAlocacao == -1:
        enderecoAlocacao = memoriaRAM.alocarProcessoNaMemoria(processo)
        if enderecoAlocacao == -1:
            enderecoAlocacaoVirtual = memoriaVirtual.alocarProcessoNoDisco(processo)

def alocarProcesso(memoriaRAM, memoriaVirtual, processo, tipoPaginacao):
    #Todo: Processo finalizado nao deve ser alocado na memoria virtual
    enderecoAlocacao = None

    enderecoAlocacao = memoriaRAM.verificarProcessoNaMemoria(processo, tipoPaginacao)
    
    if enderecoAlocacao == -1:
        enderecoAlocacao = memoriaRAM.alocarProcessoNaMemoria(processo)
        while enderecoAlocacao == -1:
            processoLiberado = liberarProcessoRAM(memoriaRAM, tipoPaginacao)
            enderecoAlocacaoVirtual = memoriaVirtual.alocarProcessoNoDisco(processoLiberado)
            enderecoAlocacao = memoriaRAM.alocarProcessoNaMemoria(processo)
        liberarProcessoDisco(memoriaVirtual, processo)

    return enderecoAlocacao

def liberarProcessoRAM(memoriaRAM, tipoPaginacao):
    #Todo: Verificar processos alocados
    processoLiberado = memoriaRAM.liberarProcessoDaMemoria(tipoPaginacao)
    return processoLiberado

def liberarProcessoDisco(memoriaVirtual, processo):
    #Todo: Verificar processos alocados
    memoriaVirtual.liberarProcessoDoDisco(processo)

def imprimeProcessosProntos(filaPronto):
    processosProntos = ""
    for p in filaPronto:
        if len(processosProntos) > 0:
            processosProntos = processosProntos + " | p" + str(p.getId())
        else:
            processosProntos = "p" + str(p.getId())
    print("Fila de processos prontos: " + processosProntos)

def logUsoProcessador(processoEmExecucao, tempoExecucao, processosProntos):
    status = None

    if processoEmExecucao is not None:
        processoEmExecucao.setLogUsoProcessador(tempoExecucao, tempoExecucao + 1)
    if processosProntos is not None:
        for processo in processosProntos:
            processo.setLogUsoProcessador(tempoExecucao, tempoExecucao + 1)

def FIFO(tipoPaginacao, processos, memoriaRAM, memoriaVirtual, tempoLimite=None):
    
    filaPronto = []
    
    tempoExecutado = 0 #Conta tempo de execucao do processo
    processosFinalizados = 0 #Conta quantos processos foram finalizados
    tempoRelativo = 0 #Conta tempo relativo de execucao do processo
    tempoTotal = 0 #Tempo de execucao
    
    processoEmExecucao = None

    while (processosFinalizados < len(processos) and (tempoLimite is None or tempoTotal <= tempoLimite)):
        
        print("----------------------------------")
        print("Intervalo tempo: " + str(tempoTotal) + " - " + str(tempoTotal + 1))

        #Atualiza fila de pronto
        for i in range(len(processos)):
            if processos[i].getTempoChegada() == tempoTotal:
                filaPronto.append(processos[i])
                alocarProcessoPronto(memoriaRAM, memoriaVirtual, processos[i], tipoPaginacao)
                processos[i].setStatusExecucao("Pronto")
        
        if len(filaPronto) > 0 or processoEmExecucao is not None:

            if processoEmExecucao is None:
                processoEmExecucao = filaPronto.pop(0)
                print("Processo p" + str(processoEmExecucao.getId()) + " comecou a executar")
                tempoExecutado = processoEmExecucao.getTempoExecutado()
                enderecoAlocacao = alocarProcesso(memoriaRAM, memoriaVirtual, processoEmExecucao, tipoPaginacao)
                processoEmExecucao.setStatusExecucao("Executando")
                logUsoProcessador(processoEmExecucao, tempoTotal, filaPronto)

                tempoExecutado += 1

                if tempoExecutado == processoEmExecucao.getTempoExecucao():
                    tempoRelativo = tempoTotal - processoEmExecucao.getTempoChegada()
                    processoEmExecucao.setTempoExecutado(tempoExecutado)
                    processoEmExecucao.setTempoTermino(tempoRelativo)
                    processoEmExecucao = None
                    processosFinalizados += 1
            else:
                tempoExecutado += 1
                if tempoExecutado < processoEmExecucao.getTempoExecucao():
                    print("Processo p" + str(processoEmExecucao.getId()) + " esta em execucao")
                    processoEmExecucao.setStatusExecucao("Executando")
                    logUsoProcessador(processoEmExecucao, tempoTotal, filaPronto)
                else:
                    print("Processo p" + str(processoEmExecucao.getId()) + " finalizou a execucao")
                    processoEmExecucao.setStatusExecucao("Finalizando")
                    logUsoProcessador(processoEmExecucao, tempoTotal, filaPronto)
                    tempoRelativo = tempoTotal - processoEmExecucao.getTempoChegada()
                    processoEmExecucao.setTempoExecutado(tempoExecutado)
                    processoEmExecucao.setTempoTermino(tempoRelativo)
                    processoEmExecucao = None
                    processosFinalizados += 1

            imprimeProcessosProntos(filaPronto)

        tempoTotal += 1

def SJF(tipoPaginacao, processos, memoriaRAM, memoriaVirtual, tempoLimite=None):
    
    filaPronto = []
    
    tempoExecutado = 0 #Conta tempo de execucao do processo
    processosFinalizados = 0 #Conta quantos processos foram finalizados
    tempoRelativo = 0 #Conta tempo relativo de execucao do processo
    tempoTotal = 0 #Tempo de execucao
    
    processoEmExecucao = None

    while (processosFinalizados < len(processos) and (tempoLimite is None or tempoTotal <= tempoLimite)):
        
        print("----------------------------------")
        print("Intervalo tempo: " + str(tempoTotal) + " - " + str(tempoTotal + 1))

        #Atualiza fila de pronto
        for i in range(len(processos)):
            if processos[i].getTempoChegada() == tempoTotal:
                filaPronto.append(processos[i])
                alocarProcessoPronto(memoriaRAM, memoriaVirtual, processos[i], tipoPaginacao)
                processos[i].setStatusExecucao("Pronto")
        
        filaPronto.sort(key=lambda processo: processo.getTempoExecucao())

        if len(filaPronto) > 0 or processoEmExecucao is not None:

            if processoEmExecucao is None:
                processoEmExecucao = filaPronto.pop(0)
                print("Processo p" + str(processoEmExecucao.getId()) + " comecou a executar")
                tempoExecutado = processoEmExecucao.getTempoExecutado()
                enderecoAlocacao = alocarProcesso(memoriaRAM, memoriaVirtual, processoEmExecucao, tipoPaginacao)
                
                processoEmExecucao.setStatusExecucao("Executando")
                logUsoProcessador(processoEmExecucao, tempoTotal, filaPronto)
                
                tempoExecutado += 1

                if tempoExecutado == processoEmExecucao.getTempoExecucao():
                    tempoRelativo = tempoTotal - processoEmExecucao.getTempoChegada()
                    processoEmExecucao.setTempoExecutado(tempoExecutado)
                    processoEmExecucao.setTempoTermino(tempoRelativo)
                    processoEmExecucao = None
                    processosFinalizados += 1

            else:
                tempoExecutado += 1
                if tempoExecutado < processoEmExecucao.getTempoExecucao():
                    print("Processo p" + str(processoEmExecucao.getId()) + " esta em execucao")
                    processoEmExecucao.setStatusExecucao("Executando")
                    logUsoProcessador(processoEmExecucao, tempoTotal, filaPronto)
                else:
                    print("Processo p" + str(processoEmExecucao.getId()) + " finalizou a execucao")
                    processoEmExecucao.setStatusExecucao("Finalizando")
                    logUsoProcessador(processoEmExecucao, tempoTotal, filaPronto)
                    tempoRelativo = tempoTotal - processoEmExecucao.getTempoChegada()
                    processoEmExecucao.setTempoExecutado(tempoExecutado)
                    processoEmExecucao.setTempoTermino(tempoRelativo)
                    processoEmExecucao = None
                    processosFinalizados += 1

            if len(filaPronto) > 0:
                filaPronto.sort(key=lambda processo: processo.getTempoExecucao())

            imprimeProcessosProntos(filaPronto)

        tempoTotal += 1

def robinRound(tipoPaginacao, processos, memoriaRAM, memoriaVirtual, tempoLimite=None):
    
    filaPronto = []
    
    tempoExecutado = 0 #Conta tempo de execucao do processo
    processosFinalizados = 0 #Conta quantos processos foram finalizados
    tempoRelativo = 0 #Conta tempo relativo de execucao do processo
    tempoTotal = 0 #Tempo de execucao
    
    processoEmExecucao = None
    ultimoProcessoExecutado = None

    sobrecarga = 0

    while (processosFinalizados < len(processos) and (tempoLimite is None or tempoTotal <= tempoLimite)):
        
        print("----------------------------------")
        print("Intervalo tempo: " + str(tempoTotal) + " - " + str(tempoTotal + 1))
        
        #Atualiza fila de pronto
        for i in range(len(processos)):
            if processos[i].getTempoChegada() == tempoTotal:
                filaPronto.append(processos[i])
                alocarProcessoPronto(memoriaRAM, memoriaVirtual, processos[i], tipoPaginacao)
                processos[i].setStatusExecucao("Pronto")

        if len(filaPronto) > 0 or processoEmExecucao is not None:
        
            if sobrecarga == 0:

                if processoEmExecucao is None:
                    processoEmExecucao = filaPronto.pop(0)
                    tempoExecutado = processoEmExecucao.getTempoExecutado()
                    enderecoAlocacao = alocarProcesso(memoriaRAM, memoriaVirtual, processoEmExecucao, tipoPaginacao)
                    
                tempoExecutado += 1
                
                #filaPronto.sort(key=lambda processo: processo.getPrioridade())
                if tempoExecutado == 1:
                    print("Processo p" + str(processoEmExecucao.getId()) + " comecou a executar")
                    processoEmExecucao.setStatusExecucao("Executando")
                    logUsoProcessador(processoEmExecucao, tempoTotal, filaPronto)

                    if tempoExecutado == processoEmExecucao.getTempoExecucao():
                        tempoRelativo = tempoTotal - processoEmExecucao.getTempoChegada()
                        processoEmExecucao.setTempoExecutado(tempoExecutado)
                        processoEmExecucao.setTempoTermino(tempoRelativo)
                        processoEmExecucao = None
                        processosFinalizados += 1

                elif tempoExecutado < processoEmExecucao.getTempoExecucao() and (tempoExecutado % processoEmExecucao.getQuantum() != 0 or len(filaPronto) == 0):
                    print("Processo p" + str(processoEmExecucao.getId()) + " esta em execucao com " + str(processoEmExecucao.getTempoExecucao() - tempoExecutado) + "ut pendente")
                    processoEmExecucao.setStatusExecucao("Executando")
                    logUsoProcessador(processoEmExecucao, tempoTotal, filaPronto)
                elif tempoExecutado % processoEmExecucao.getQuantum() == 0 and tempoExecutado != processoEmExecucao.getTempoExecucao() and len(filaPronto) > 0:
                    print("Processo p" + str(processoEmExecucao.getId()) + " pausou a execucao com " + str(processoEmExecucao.getTempoExecucao() - tempoExecutado) + "ut pendente")
                    processoEmExecucao.setStatusExecucao("Pausando")
                    logUsoProcessador(processoEmExecucao, tempoTotal, filaPronto)
                    processoEmExecucao.setTempoExecutado(tempoExecutado)
                    sobrecarga = processoEmExecucao.getSobrecarga()
                    filaPronto.append(processoEmExecucao)
                    ultimoProcessoExecutado = processoEmExecucao
                    processoEmExecucao = None
                else:
                    print("Processo p" + str(processoEmExecucao.getId()) + " finalizou a execucao")
                    processoEmExecucao.setStatusExecucao("Finalizando")
                    logUsoProcessador(processoEmExecucao, tempoTotal, filaPronto)
                    tempoRelativo = tempoTotal - processoEmExecucao.getTempoChegada()
                    processoEmExecucao.setTempoExecutado(tempoExecutado)
                    processoEmExecucao.setTempoTermino(tempoRelativo)
                    ultimoProcessoExecutado = processoEmExecucao
                    processoEmExecucao = None
                    processosFinalizados += 1

            else:
                print("Sobrecarga do sistema: " + str(sobrecarga))
                ultimoProcessoExecutado.setStatusExecucao("Overhead")
                logUsoProcessador(ultimoProcessoExecutado, tempoTotal, filaPronto)
                ultimoProcessoExecutado.setStatusExecucao("Pausado")
                sobrecarga -= 1
            
            #filaPronto.sort(key=lambda processo: processo.getPrioridade())
            imprimeProcessosProntos(filaPronto)
    
        tempoTotal += 1

def EDF(tipoPaginacao, processos, memoriaRAM, memoriaVirtual, tempoLimite=None):
    
    filaPronto = []
    
    tempoExecutado = 0 #Conta tempo de execucao do processo
    processosFinalizados = 0 #Conta quantos processos foram finalizados
    tempoRelativo = 0 #Conta tempo relativo de execucao do processo
    tempoTotal = 0 #Tempo de execucao
    
    processoEmExecucao = None
    ultimoProcessoExecutado = None

    sobrecarga = 0

    while (processosFinalizados < len(processos) and (tempoLimite is None or tempoTotal <= tempoLimite)):
        
        print("----------------------------------")
        print("Intervalo tempo: " + str(tempoTotal) + " - " + str(tempoTotal + 1))
        
        #Atualiza fila de pronto
        for i in range(len(processos)):
            if processos[i].getTempoChegada() == tempoTotal:
                filaPronto.append(processos[i])
                alocarProcessoPronto(memoriaRAM, memoriaVirtual, processos[i], tipoPaginacao)
                processos[i].setStatusExecucao("Pronto")
        
        filaPronto.sort(key=lambda processo: processo.getDeadline())

        if len(filaPronto) > 0 or processoEmExecucao is not None:
        
            if sobrecarga == 0:

                if processoEmExecucao is None:
                    processoEmExecucao = filaPronto.pop(0)
                    tempoExecutado = processoEmExecucao.getTempoExecutado()
                    enderecoAlocacao = alocarProcesso(memoriaRAM, memoriaVirtual, processoEmExecucao, tipoPaginacao)
                    
                tempoExecutado += 1
                
                if tempoExecutado == 1:
                    print("Processo p" + str(processoEmExecucao.getId()) + " comecou a executar")
                    processoEmExecucao.setStatusExecucao("Executando")
                    logUsoProcessador(processoEmExecucao, tempoTotal, filaPronto)

                    if tempoExecutado == processoEmExecucao.getTempoExecucao():
                        tempoRelativo = tempoTotal - processoEmExecucao.getTempoChegada()
                        processoEmExecucao.setTempoExecutado(tempoExecutado)
                        processoEmExecucao.setTempoTermino(tempoRelativo)
                        processoEmExecucao = None
                        processosFinalizados += 1
                elif tempoExecutado < processoEmExecucao.getTempoExecucao() and (tempoExecutado % processoEmExecucao.getQuantum() != 0 or len(filaPronto) == 0):
                    print("Processo p" + str(processoEmExecucao.getId()) + " esta em execucao com " + str(processoEmExecucao.getTempoExecucao() - tempoExecutado) + "ut pendente")
                    processoEmExecucao.setStatusExecucao("Executando")
                    logUsoProcessador(processoEmExecucao, tempoTotal, filaPronto)
                elif tempoExecutado % processoEmExecucao.getQuantum() == 0 and tempoExecutado != processoEmExecucao.getTempoExecucao() and len(filaPronto) > 0:
                    print("Processo p" + str(processoEmExecucao.getId()) + " pausou a execucao com " + str(processoEmExecucao.getTempoExecucao() - tempoExecutado) + "ut pendente")
                    processoEmExecucao.setStatusExecucao("Pausando")
                    logUsoProcessador(processoEmExecucao, tempoTotal, filaPronto)
                    processoEmExecucao.setTempoExecutado(tempoExecutado)
                    sobrecarga = processoEmExecucao.getSobrecarga()
                    filaPronto.append(processoEmExecucao)
                    ultimoProcessoExecutado = processoEmExecucao
                    processoEmExecucao = None
                else:
                    print("Processo p" + str(processoEmExecucao.getId()) + " finalizou a execucao")
                    processoEmExecucao.setStatusExecucao("Finalizando")
                    logUsoProcessador(processoEmExecucao, tempoTotal, filaPronto)
                    tempoRelativo = tempoTotal - processoEmExecucao.getTempoChegada()
                    processoEmExecucao.setTempoExecutado(tempoExecutado)
                    processoEmExecucao.setTempoTermino(tempoRelativo)
                    ultimoProcessoExecutado = processoEmExecucao
                    processoEmExecucao = None
                    processosFinalizados += 1

            else:
                print("Sobrecarga do sistema: " + str(sobrecarga))
                ultimoProcessoExecutado.setStatusExecucao("Overhead")
                logUsoProcessador(ultimoProcessoExecutado, tempoTotal, filaPronto)
                ultimoProcessoExecutado.setStatusExecucao("Pausado")
                sobrecarga -= 1

            if len(filaPronto) > 0:
                filaPronto.sort(key=lambda processo: processo.getDeadline())

            imprimeProcessosProntos(filaPronto)

        tempoTotal += 1