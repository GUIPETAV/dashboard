# -*- coding: utf-8 -*-
"""Dashboard.ipynb """

import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

url = 'https://raw.githubusercontent.com/GUIPETAV/Base/main/base.csv'

base = pd.read_csv(url)

#

# Lista de features disponíveis
features = base.columns[1:]

# Lista vazia para armazenar as features selecionadas
selected_features = []

fig = go.Figure()

# Personalizar o layout do gráfico
# Layout
app.layout = html.Div(
    id="div1",
    children=[
        html.H1("Visualização dos dados", id="h1",style={'text-align': 'center'}),
    
                # Caixas de seleção para as features

        dcc.Dropdown(
            id='feature-selector',
            options=[{'label': feature, 'value': feature} for feature in features],
            value=[features[0]],  # Defina a primeira feature como selecionada inicialmente
            multi=True  # Permitir seleção múltipla
        ),
        
        dcc.Graph(id='scatter-plot')
    ]
)

@app.callback(
    dash.dependencies.Output('scatter-plot', 'figure'),
    [dash.dependencies.Input('feature-selector', 'value')]
)
def update_scatter_plot(selected_features):
    traces = []
    
    # Criar uma trace para cada feature selecionada
    for feature in selected_features:
        trace = go.Scatter(x=base['Datetime'], y=base[feature], mode='markers', name=feature)
        traces.append(trace)
    
    fig = go.Figure(data=traces)
    fig.update_layout(
        title='Distribuição das Features Selecionadas',
        xaxis_title='Data',
        yaxis_title='Valor'
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)