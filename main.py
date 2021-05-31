### Bibliotecas para montar o dashboard
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table as dt
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from datetime import date, timedelta

import plotly.figure_factory as ff
import plotly.graph_objects as go

import styles

import Processo
import Escalonamento
import RAM
import Disco
import Pagina

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

########################### Variaveis para execucao ###########################
processos = []
nProcessos = 0
hoje = date.today()
dataGraph = []
tempoTotalExecucao = 0
turnaround = 0

########################### Conteudo ###########################
############## Campos ##############
bTempoChegada = False
bTempoExecucao = False
bQuantum = False
bDeadline = False
bPrioridade = False
bSobrecarga = False
bNumeroPaginas = False

labelsL = ["Tempo de chegada", "Tempo de execucao", "Quantum"]
keysL = ["tempoChegada", "tempoExecucao", "quantum"]
camposProcessoL = []
for i in range(len(labelsL)):
    camposProcessoL.append(dbc.Label(f'{labelsL[i]}: ', style=styles.labelStyle))
    camposProcessoL.append(dbc.Input(id=keysL[i], placeholder=labelsL[i], type="number", min=0,))

labelsR = ["Deadline", "Prioridade", "Sobrecarga"]
keysR = ["deadline", "prioridade", "sobrecarga"]
camposProcessoR = []
for i in range(len(labelsR)):
    camposProcessoR.append(dbc.Label(f'{labelsR[i]}: ', style=styles.labelStyle))
    camposProcessoR.append(dbc.Input(id=keysR[i], placeholder=labelsR[i], type="number", min=0,))

camposProcessoL.append(dbc.Label('Numero de paginas: '))
camposProcessoL.append(dbc.Input(id="numeroPaginas", placeholder="Numero de paginas", min=0, max=10, step=1, type="number"))

############## Botão adicionar ##############
addButton = dbc.Button("Adicionar", className="mb-3", color="primary", id='add', style=styles.buttonAddStyle)
camposProcessoR.append(addButton)

############## Finalizacao do card ##############
boxForm = dbc.Row([
    dbc.Col(html.Form(camposProcessoL), md=6),
    dbc.Col(html.Form(camposProcessoR), md=6),
])

############## Opcoes de algoritmo ##############
algoritmosEscalonamento = html.Form([
    dbc.Label('Tipo de Escalonamento: '),
    dbc.RadioItems(options=
        [
            {"label": "FIFO", "value": 1},
            {"label": "SJF", "value": 2},
            {"label": "Robin round", "value": 3},
            {"label": "EDF", "value": 4},
        ], value=1, inline=True, id="radioEscalonamento",)
])

algoritmosPaginacao = html.Form([
    dbc.Label('Tipo de Paginacao: '),
    dbc.RadioItems(options=
        [
            {"label": "FIFO", "value": 1},
            {"label": "MRU", "value": 2},
        ], value=1, inline=True, id="radioPaginacao",)
])

############## Tabela de processos ##############
tableHeader = [
    html.Thead(html.Tr(
        [
            html.Th("Id", style=styles.rowStyle), 
            html.Th("Inicio", style=styles.rowStyle), 
            html.Th("Exec.", style=styles.rowStyle), 
            html.Th("Ut", style=styles.rowStyle), 
            html.Th("Deadline", style=styles.rowStyle), 
            html.Th("Prior.", style=styles.rowStyle), 
            html.Th("Overh.", style=styles.rowStyle), 
            html.Th("Pag.", style=styles.rowStyle)
        ]))
]
tableRow = []
row = []

tableBody = [
    html.Tbody(id="tableBody", children=row)
]

table = dbc.Table(tableHeader + tableBody, bordered=True, responsive=True, style=styles.tableStyle)

########################### Turnround ###########################

turnroundLabel = html.Div(id="turnround")

############## Botão executar ##############
execButton = dbc.Button("Executar", className="mb-3", color="primary", id='exec')
limparButton = dbc.Button("Limpar", className="mb-3", color="primary", id='limpar', style=styles.buttonLimparStyle)

boxDados = [turnroundLabel, boxForm, algoritmosEscalonamento, algoritmosPaginacao, table, execButton, limparButton]

############## Box grafico ##############

boxGraphProcessos = html.Div([
    html.Div(id="boxGraphProcessos", style={"height": "600px"}),
])
boxGraphMemoria = html.Div(id="boxGraphMemoria", style={"height": "600px"})

boxResult = dbc.Tabs(
    [
        dbc.Tab(children=boxGraphProcessos, label="Processos", tab_id="processos"),
        dbc.Tab(children=boxGraphMemoria, label="Disco & Memoria", tab_id="discoMemoria"),
    ],
    id="abas",
    active_tab="processos",
)

########################### Componentes HTML ###########################

sliderGraph = html.Div(id="sliderGraph", 
    children= [
        dbc.Label('Tempo de execucao: '),
        dcc.Slider(id="slider", min=0, max=1, marks={i: str(i) for i in range(1)},value=1)
    ])

boxConteudo = dbc.Row(
    [
        dbc.Col(boxDados, md=4, style=styles.boxDados),
        dbc.Col([boxResult, sliderGraph], md=8),
    ], align="center"
)

app.layout = dbc.Container(
    [
        ########################### Titulo ###########################
        html.H1("Simulação SO", style=styles.titleStyle),
        html.Hr(),
        
        ########################### Conteudo ###########################
        boxConteudo,
    ], fluid=True,
)

@app.callback(
    [Output('tableBody', 'children')],
    [Output('tempoChegada',  'invalid')],
    [Output('tempoExecucao', 'invalid')],
    [Output('quantum',       'invalid')],
    [Output('deadline',      'invalid')],
    [Output('prioridade',    'invalid')],
    [Output('sobrecarga',    'invalid')],
    [Output('numeroPaginas', 'invalid')],
    [Input('add',            'n_clicks')],
    [Input('limpar',         'n_clicks')],
    [Input('tempoChegada',  'value')],
    [Input('tempoExecucao', 'value')],
    [Input('quantum',       'value')],
    [Input('deadline',      'value')],
    [Input('prioridade',    'value')],
    [Input('sobrecarga',    'value')],
    [Input('numeroPaginas', 'value')],
)
def populaTabelaProcessos(add, limpar, tempoChegada, tempoExecucao, quantum, deadline, prioridade, sobrecarga, numeroPaginas):
    global nProcessos
    global processos

    global bTempoChegada
    global bTempoExecucao
    global bQuantum
    global bDeadline
    global bPrioridade
    global bSobrecarga
    global bNumeroPaginas

    global row
    global tableRow

    ctx = dash.callback_context

    componentId = ctx.triggered[0]['prop_id'].split('.')[0]

    if componentId == 'add':

        nProcessos += 1

        if tempoChegada is not None and tempoChegada >= 0:
            bTempoChegada = False
        else:
            bTempoChegada = True
        
        if tempoExecucao is not None and tempoExecucao >= 0:
            bTempoExecucao = False
        else:
            bTempoExecucao = True
        
        if quantum is not None and quantum >= 0:
            bQuantum = False
        else:
            bQuantum = True
        
        if deadline is not None and deadline >= 0:
            bDeadline = False
        elif deadline is None:
            bDeadline = False
            deadLine = 0
        else:
            bDeadline = True

        if prioridade is not None and prioridade >= 0:
            bPrioridade = False
        elif prioridade is None:
            bPrioridade = False
            prioridade = 0
        else:
            bPrioridade = True

        if sobrecarga is not None and sobrecarga >= 0:
            bSobrecarga = False
        elif sobrecarga is None:
            bSobrecarga = False
            sobrecarga = 0
        else:
            bSobrecarga = True
        
        bNumeroPaginas = numeroPaginas is None
        if numeroPaginas > 10 or numeroPaginas < 0:
            bNumeroPaginas = True

        if not bTempoChegada and not bTempoExecucao and not bQuantum and not bDeadline and not bPrioridade and not bSobrecarga and not bNumeroPaginas:
            
            if deadline is None:
                deadline = 0
            if prioridade is None:
                prioridade = 0
            if sobrecarga is None:
                sobrecarga = 0

            tableRow.append([nProcessos, tempoChegada, tempoExecucao, quantum, deadline, prioridade, sobrecarga, numeroPaginas])

            row.append(html.Tr([
                html.Td(nProcessos, style=styles.rowStyle), 
                html.Td(tempoChegada, style=styles.rowStyle), 
                html.Td(tempoExecucao, style=styles.rowStyle), 
                html.Td(quantum, style=styles.rowStyle), 
                html.Td(deadline, style=styles.rowStyle),
                html.Td(prioridade, style=styles.rowStyle), 
                html.Td(sobrecarga, style=styles.rowStyle), 
                html.Td(numeroPaginas, style=styles.rowStyle)
            ]))
    elif componentId == 'limpar':
        row = []
        tableRow = []
        nProcessos = 0
        turnround = []

    return (row, 
               
        ######## Validacao de campo ########
        bTempoChegada, 
        bTempoExecucao, 
        bQuantum, 
        bDeadline, 
        bPrioridade, 
        bSobrecarga, 
        bNumeroPaginas
    )

@app.callback(
    [Output('boxGraphProcessos', 'children')],
    [Output('boxGraphMemoria',   'children')],
    [Output('slider',            'min')],
    [Output('slider',            'max')],
    [Output('slider',            'marks')],
    [Output('slider',            'value')],
    [Output('turnround',         'children')],
    [Input('exec',               'n_clicks')],
    [Input('radioEscalonamento', 'value')],
    [Input('radioPaginacao',     'value')],
    [Input('slider',             'value')]
)
def montaGraficoGrantt(n, radioEscalonamento, radioPaginacao, timeLimite):
    global processos
    global dataGraph
    global tempoTotalExecucao
    global turnround
    
    ctx = dash.callback_context

    componentId = ctx.triggered[0]['prop_id'].split('.')[0]

    colors = {
        'Pronto': 'rgb(200, 200, 200)',
        'Executando': 'rgb(0, 255, 100)',
        'Pausado': 'rgb(255, 168, 81)',
        'Overhead': 'rgb(240, 68, 77)'
    }

    if componentId == 'exec':
        
        #Reinicia uso de memoria RAM e memoria virtual (disco)
        memoriaRAM = RAM.RAM()
        memoriaVirtual = Disco.Disco(100)

        #Monta array de processos
        processos = []
        for processo in tableRow:

            paginas = []
            for j in range(processo[7]):
                p = Pagina.Pagina(processo[0], j)
                paginas.append(p)

            p = Processo.Processo(processo[0], processo[1], processo[2], processo[3], processo[4], processo[5], processo[6], paginas)

            processos.append(p)

        if len(processos) > 0:

            #Identifica o tipo de escalonamento
            if radioEscalonamento == 1:
                Escalonamento.FIFO(radioPaginacao, processos, memoriaRAM, memoriaVirtual)
            elif radioEscalonamento == 2:
                Escalonamento.SJF(radioPaginacao, processos, memoriaRAM, memoriaVirtual)
            elif radioEscalonamento == 3:
                Escalonamento.robinRound(radioPaginacao, processos, memoriaRAM, memoriaVirtual)
            elif radioEscalonamento == 4:
                Escalonamento.EDF(radioPaginacao, processos, memoriaRAM, memoriaVirtual)

            #Inicia variaveis para grafico de escalonamento
            tempoTotalExecucao = 0
            dataGraph = []
            
            #Inicia variaveis para grafico de RAM e Disco
            memoGraph = []
            discoGraph = []
            totalMemo = 0
            totalDisco = 0

            #Monta valores para grafico de RAM
            idProcessosRAM = []
            dataRam = memoriaRAM.getMemoria()
            for i in range(len(dataRam)):
                pagina = dataRam[i]
                if pagina is not None and pagina.getProcessoId() not in idProcessosRAM:
                    idProcessosRAM.append(pagina.getProcessoId())

            #Monta valores para grafico de Disco
            idProcessosDisco = []
            dataDisco = memoriaVirtual.getMemoriaVirtual()
            for i in range(len(dataDisco)):
                pagina = dataDisco[i]
                if pagina is not None and pagina.getProcessoId() not in idProcessosDisco:
                    idProcessosDisco.append(pagina.getProcessoId())
            
            tempoExecucaoTotal = 0
            #Monta grafico de Escalonamento, RAM e Disco
            for processo in processos:
                processoId = processo.getId()
                task = f'p{processoId}'

                for log in processo.getLogUsoProcessador():
                    start = hoje + timedelta(days=+log[0])
                    finish = hoje + timedelta(days=+log[1])
                    dataGraph.append(dict(Task=task, Start=start, Finish=finish, Resource=log[2]))
                    
                    if log[1] > tempoTotalExecucao:
                        tempoTotalExecucao = log[1] + 1
                
                if processoId in idProcessosRAM:
                    memoGraph.append(go.Bar(name=task, x=["RAM"], y=[len(processo.getPaginas())]))
                    totalMemo += len(processo.getPaginas())

                if processoId in idProcessosDisco:
                    discoGraph.append(go.Bar(name=task, x=["Disco"], y=[len(processo.getPaginas())]))
                    totalDisco += len(processo.getPaginas())

                #Calcular tempo total de execucao dos processos
                tempoExecucaoTotal += processo.getTempoTermino() + 1
                #print(f'Processo { processo.getId() } tempo até execucao: { processo.getTempoTermino() }')

            if totalMemo <= len(dataRam):
                memoGraph.append(go.Bar(name=f'none', x=["RAM"], y=[len(dataRam) - totalMemo]))

            if totalDisco <= len(dataDisco):
                discoGraph.append(go.Bar(name=f'none', x=["Disco"], y=[len(dataDisco) - totalDisco]))

            memoriaFig = go.Figure(data=memoGraph)
            memoriaFig.update_layout(barmode='stack')

            discoFig = go.Figure(data=discoGraph)
            discoFig.update_layout(barmode='stack')

            memoriaDiscoFig = dbc.Row(
                [
                    dbc.Col(dcc.Graph(figure=memoriaFig), width=6),
                    dbc.Col(dcc.Graph(figure=discoFig), width=6)
                ]
            )

            processosFig = ff.create_gantt(dataGraph, colors=colors, index_col='Resource', show_colorbar=True, group_tasks=True,
                        showgrid_x=True, showgrid_y=True)
            processosFig['layout'].update(legend={'x': 1, 'y': 1})
            
            #Calcular turnround
            turnround = tempoExecucaoTotal/len(processos)
            #print(f'Numero de processos: {len(processos)} turnround: { turnround }')

            return (
                [dcc.Graph(id="plot_area", figure=processosFig)],
                [memoriaDiscoFig],

                1,
                tempoTotalExecucao - 1,
                {i: str(i) for i in range(tempoTotalExecucao)},
                tempoTotalExecucao - 1,
                [dbc.Alert('Turnround: {:.2f}'.format(turnround), color="primary")]
            )
    
    elif componentId == 'slider':

        #Reinicia uso de memoria RAM e memoria virtual (disco)
        memoriaRAMAux = RAM.RAM()
        memoriaVirtualAux = Disco.Disco(100)
        processosAux = processos.copy()

        #Inicia variaveis para grafico de RAM e Disco
        memoGraph = []
        discoGraph = []
        totalMemo = 0
        totalDisco = 0
        
        #Identifica o tipo de escalonamento
        if radioEscalonamento == 1:
            Escalonamento.FIFO(radioPaginacao, processosAux, memoriaRAMAux, memoriaVirtualAux, timeLimite)
        elif radioEscalonamento == 2:
            Escalonamento.SJF(radioPaginacao, processosAux, memoriaRAMAux, memoriaVirtualAux, timeLimite)
        elif radioEscalonamento == 3:
            Escalonamento.robinRound(radioPaginacao, processosAux, memoriaRAMAux, memoriaVirtualAux, timeLimite)
        elif radioEscalonamento == 4:
            Escalonamento.EDF(radioPaginacao, processosAux, memoriaRAMAux, memoriaVirtualAux, timeLimite)
        
        #Monta valores para grafico de RAM
        idProcessosRAM = []
        dataRam = memoriaRAMAux.getMemoria()
        for i in range(len(dataRam)):
            pagina = dataRam[i]
            if pagina is not None and pagina.getProcessoId() not in idProcessosRAM:
                idProcessosRAM.append(pagina.getProcessoId())

        #Monta valores para grafico de Disco
        idProcessosDisco = []
        dataDisco = memoriaVirtualAux.getMemoriaVirtual()
        for i in range(len(dataDisco)):
            pagina = dataDisco[i]
            if pagina is not None and pagina.getProcessoId() not in idProcessosDisco:
                idProcessosDisco.append(pagina.getProcessoId())

        #Monta grafico de Escalonamento, RAM e Disco
        for processo in processos:
            processoId = processo.getId()
            task = f'p{processoId}'
            
            if processoId in idProcessosRAM:
                memoGraph.append(go.Bar(name=task, x=["RAM"], y=[len(processo.getPaginas())]))
                totalMemo += len(processo.getPaginas())

            if processoId in idProcessosDisco:
                discoGraph.append(go.Bar(name=task, x=["Disco"], y=[len(processo.getPaginas())]))
                totalDisco += len(processo.getPaginas())

        if totalMemo <= len(dataRam):
            memoGraph.append(go.Bar(name=f'none', x=["RAM"], y=[len(dataRam) - totalMemo]))

        if totalDisco <= len(dataDisco):
            discoGraph.append(go.Bar(name=f'none', x=["Disco"], y=[len(dataDisco) - totalDisco]))

        memoriaFig = go.Figure(data=memoGraph)
        memoriaFig.update_layout(barmode='stack')

        discoFig = go.Figure(data=discoGraph)
        discoFig.update_layout(barmode='stack')

        filteredDataGraph = []
        for data in dataGraph:
            if data['Finish'] <= hoje + timedelta(days=timeLimite):
                filteredDataGraph.append(data)

        processosFig = ff.create_gantt(filteredDataGraph, colors=colors, index_col='Resource', show_colorbar=True, group_tasks=True,
                    showgrid_x=True, showgrid_y=True)
        processosFig['layout'].update(legend={'x': 1, 'y': 1})

        memoriaDiscoFig = dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=memoriaFig), width=6),
                dbc.Col(dcc.Graph(figure=discoFig), width=6)
            ]
        )

        return (
                [dcc.Graph(id="plot_area", figure=processosFig)],
                memoriaDiscoFig,

                1,
                tempoTotalExecucao - 1,
                {i: str(i) for i in range(tempoTotalExecucao)},
                timeLimite,
                [dbc.Alert('Turnround: {:.2f}'.format(turnround), color="primary")]
            )
    raise PreventUpdate
    #return [html.Div(""), html.Div(""), 1, 1, {i: str(i) for i in range(tempoTotalExecucao)}, 1]


if __name__=='__main__':
    app.run_server()