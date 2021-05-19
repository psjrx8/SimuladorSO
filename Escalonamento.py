def alocarProcesso(memoriaRAM, memoriaVirtual, processo):
    #Todo: Verificar processos alocados
    enderecoAlocacao = None
    enderecoAlocacao = memoriaRAM.alocarProcessoNaMemoria(processo)
    #if enderecoAlocacao == -1:
    #    enderecoAlocacao = memoriaVirtual.alocarProcessoNoDisco(processo)
        
    return enderecoAlocacao

def imprimeProcessosProntos(filaPronto):
    processosProntos = ""
    for p in filaPronto:
        if len(processosProntos) > 0:
            processosProntos = processosProntos + " | p" + str(p.getId())
        else:
            processosProntos = "p" + str(p.getId())
    print("Fila de processos prontos: " + processosProntos)

def FIFO(tipoPaginacao, processos, memoriaRAM, memoriaVirtual):
    
    filaPronto = []
    
    tempoExecutado = 0 #Conta tempo de execucao do processo
    processosFinalizados = 0 #Conta quantos processos foram finalizados
    tempoRelativo = 0 #Conta tempo relativo de execucao do processo
    tempoTotal = 0 #Tempo de execucao
    
    processoEmExecucao = None

    while (processosFinalizados < len(processos)):
        
        print("----------------------------------")
        print("Intervalo tempo: " + str(tempoTotal) + " - " + str(tempoTotal + 1))

        #Atualiza fila de pronto
        for i in range(len(processos)):
            if processos[i].getTempoChegada() == tempoTotal:
                filaPronto.append(processos[i]) 
        
        if len(filaPronto) > 0 or processoEmExecucao is not None:

            if processoEmExecucao is None:
                processoEmExecucao = filaPronto.pop(0)
                print("Processo p" + str(processoEmExecucao.getId()) + " comecou a executar")
                tempoExecutado = processoEmExecucao.getTempoExecutado()
                alocarProcesso(memoriaRAM, memoriaVirtual, processoEmExecucao)
                tempoExecutado += 1
            else:
                tempoExecutado += 1
                if tempoExecutado < processoEmExecucao.getTempoExecucao():
                    print("Processo p" + str(processoEmExecucao.getId()) + " esta em execucao")
                else:
                    print("Processo p" + str(processoEmExecucao.getId()) + " finalizou a execucao")
                    tempoRelativo = tempoTotal - processoEmExecucao.getTempoChegada()
                    processoEmExecucao.setTempoExecutado(tempoExecutado)
                    processoEmExecucao.setTempoTermino(tempoRelativo)
                    processoEmExecucao = None
                    processosFinalizados += 1

            imprimeProcessosProntos(filaPronto)

        tempoTotal += 1

def SJF(tipoPaginacao, processos, memoriaRAM, memoriaVirtual):
    
    filaPronto = []
    
    tempoExecutado = 0 #Conta tempo de execucao do processo
    processosFinalizados = 0 #Conta quantos processos foram finalizados
    tempoRelativo = 0 #Conta tempo relativo de execucao do processo
    tempoTotal = 0 #Tempo de execucao
    
    processoEmExecucao = None

    while (processosFinalizados < len(processos)):
        
        print("----------------------------------")
        print("Intervalo tempo: " + str(tempoTotal) + " - " + str(tempoTotal + 1))

        #Atualiza fila de pronto
        for i in range(len(processos)):
            if processos[i].getTempoChegada() == tempoTotal:
                filaPronto.append(processos[i])
        
        filaPronto.sort(key=lambda processo: processo.getTempoExecucao())

        if len(filaPronto) > 0 or processoEmExecucao is not None:

            if processoEmExecucao is None:
                processoEmExecucao = filaPronto.pop(0)
                print("Processo p" + str(processoEmExecucao.getId()) + " comecou a executar")
                tempoExecutado = processoEmExecucao.getTempoExecutado()
                alocarProcesso(memoriaRAM, memoriaVirtual, processoEmExecucao)
                tempoExecutado += 1
            else:
                tempoExecutado += 1
                if tempoExecutado < processoEmExecucao.getTempoExecucao():
                    print("Processo p" + str(processoEmExecucao.getId()) + " esta em execucao")
                else:
                    print("Processo p" + str(processoEmExecucao.getId()) + " finalizou a execucao")
                    tempoRelativo = tempoTotal - processoEmExecucao.getTempoChegada()
                    processoEmExecucao.setTempoExecutado(tempoExecutado)
                    processoEmExecucao.setTempoTermino(tempoRelativo)
                    processoEmExecucao = None
                    processosFinalizados += 1

            imprimeProcessosProntos(filaPronto)

        tempoTotal += 1

def robinRound(tipoPaginacao, processos, memoriaRAM, memoriaVirtual):
    
    filaPronto = []
    
    tempoExecutado = 0 #Conta tempo de execucao do processo
    processosFinalizados = 0 #Conta quantos processos foram finalizados
    tempoRelativo = 0 #Conta tempo relativo de execucao do processo
    tempoTotal = 0 #Tempo de execucao
    
    processoEmExecucao = None

    sobrecarga = 0

    while (processosFinalizados < len(processos)):
        
        print("----------------------------------")
        print("Intervalo tempo: " + str(tempoTotal) + " - " + str(tempoTotal + 1))
        
        #Atualiza fila de pronto
        for i in range(len(processos)):
            if processos[i].getTempoChegada() == tempoTotal:
                filaPronto.append(processos[i])
        
        if len(filaPronto) > 0 or processoEmExecucao is not None:
        
            if sobrecarga == 0:

                if processoEmExecucao is None:
                    processoEmExecucao = filaPronto.pop(0)
                    tempoExecutado = processoEmExecucao.getTempoExecutado()
                    alocarProcesso(memoriaRAM, memoriaVirtual, processoEmExecucao)
                    
                tempoExecutado += 1
                
                if tempoExecutado == 1:
                    print("Processo p" + str(processoEmExecucao.getId()) + " comecou a executar")
                elif tempoExecutado < processoEmExecucao.getTempoExecucao() and (tempoExecutado % processoEmExecucao.getQuantum() != 0 or len(filaPronto) == 0):
                    print("Processo p" + str(processoEmExecucao.getId()) + " esta em execucao com " + str(processoEmExecucao.getTempoExecucao() - tempoExecutado) + "ut pendente")
                elif tempoExecutado % processoEmExecucao.getQuantum() == 0 and tempoExecutado != processoEmExecucao.getTempoExecucao() and len(filaPronto) > 0:
                    print("Processo p" + str(processoEmExecucao.getId()) + " pausou a execucao com " + str(processoEmExecucao.getTempoExecucao() - tempoExecutado) + "ut pendente")
                    processoEmExecucao.setTempoExecutado(tempoExecutado)
                    sobrecarga = processoEmExecucao.getSobrecarga()
                    filaPronto.append(processoEmExecucao)
                    processoEmExecucao = None
                else:
                    print("Processo p" + str(processoEmExecucao.getId()) + " finalizou a execucao")
                    tempoRelativo = tempoTotal - processoEmExecucao.getTempoChegada()
                    processoEmExecucao.setTempoExecutado(tempoExecutado)
                    processoEmExecucao.setTempoTermino(tempoRelativo)
                    processoEmExecucao = None
                    processosFinalizados += 1

            else:
                print("Sobrecarga do sistema: " + str(sobrecarga))
                sobrecarga -= 1
            
            imprimeProcessosProntos(filaPronto)
    
        tempoTotal += 1

def EDF(tipoPaginacao, processos, memoriaRAM, memoriaVirtual):
    
    filaPronto = []
    
    tempoExecutado = 0 #Conta tempo de execucao do processo
    processosFinalizados = 0 #Conta quantos processos foram finalizados
    tempoRelativo = 0 #Conta tempo relativo de execucao do processo
    tempoTotal = 0 #Tempo de execucao
    
    processoEmExecucao = None

    sobrecarga = 0

    while (processosFinalizados < len(processos)):
        
        print("----------------------------------")
        print("Intervalo tempo: " + str(tempoTotal) + " - " + str(tempoTotal + 1))
        
        #Atualiza fila de pronto
        for i in range(len(processos)):
            if processos[i].getTempoChegada() == tempoTotal:
                filaPronto.append(processos[i])
        
        filaPronto.sort(key=lambda processo: processo.getDeadline())

        if len(filaPronto) > 0 or processoEmExecucao is not None:
        
            if sobrecarga == 0:

                if processoEmExecucao is None:
                    processoEmExecucao = filaPronto.pop(0)
                    tempoExecutado = processoEmExecucao.getTempoExecutado()
                    alocarProcesso(memoriaRAM, memoriaVirtual, processoEmExecucao)
                    
                tempoExecutado += 1
                
                if tempoExecutado == 1:
                    print("Processo p" + str(processoEmExecucao.getId()) + " comecou a executar")
                elif tempoExecutado < processoEmExecucao.getTempoExecucao() and tempoExecutado % processoEmExecucao.getQuantum() != 0:
                    print("Processo p" + str(processoEmExecucao.getId()) + " esta em execucao com " + str(processoEmExecucao.getTempoExecucao() - tempoExecutado) + "ut pendente")
                elif tempoExecutado % processoEmExecucao.getQuantum() == 0 and tempoExecutado != processoEmExecucao.getTempoExecucao():
                    print("Processo p" + str(processoEmExecucao.getId()) + " pausou a execucao com " + str(processoEmExecucao.getTempoExecucao() - tempoExecutado) + "ut pendente")
                    processoEmExecucao.setTempoExecutado(tempoExecutado)
                    sobrecarga = processoEmExecucao.getSobrecarga()
                    filaPronto.append(processoEmExecucao)
                    processoEmExecucao = None
                else:
                    print("Processo p" + str(processoEmExecucao.getId()) + " finalizou a execucao")
                    tempoRelativo = tempoTotal - processoEmExecucao.getTempoChegada()
                    processoEmExecucao.setTempoExecutado(tempoExecutado)
                    processoEmExecucao.setTempoTermino(tempoRelativo)
                    processoEmExecucao = None
                    processosFinalizados += 1

            else:
                print("Sobrecarga do sistema: " + str(sobrecarga))
                sobrecarga -= 1
    
            imprimeProcessosProntos(filaPronto)

        tempoTotal += 1