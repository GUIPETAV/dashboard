# -*- coding: utf-8 -*-
"""Dashboard.ipynb """

import dash
from dash import html,dcc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

url = 'https://raw.githubusercontent.com/GUIPETAV/Base/main/base.csv'

base = pd.read_csv(url)

fig = go.Figure(data=go.Scatter(x=base['Datetime'], y=base['ZA_TEMP'], mode='markers'))

# Personalizar o layout do gráfico
fig.update_layout(
    title='Distribuição da Temperatura',
    xaxis_title='Data',
    yaxis_title='Temperatura (°C)'
)
#Layout

app.layout = html.Div(id="div1",
    children=[
         html.H1("Visualização dos dados", id = "h1"),

    html.Div ("Dashboards"),
         
    dcc.Graph (figure = fig)
    ]
)

if __name__=='__main__':
  app.run_server (debug = True, port= 8051)
