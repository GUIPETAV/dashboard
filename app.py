import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

url = 'https://raw.githubusercontent.com/GUIPETAV/Base/main/base_media_30m.csv'

base = pd.read_csv(url)

# Lista de features disponíveis
features = base.columns[1:]

# Lista vazia para armazenar as features selecionadas
selected_features = []

fig_scatter = go.Figure()
fig_line = go.Figure()

# Personalizar o layout do gráfico
# Layout
app.layout = html.Div(
    id="div1",
    children=[
        html.H1("Visualização dos dados", id="h1", style={'text-align': 'center'}),

        # Caixas de seleção para as features
        dcc.Dropdown(
            id='feature-selector',
            options=[{'label': feature, 'value': feature} for feature in features],
            value=[features[0]],  # Defina a primeira feature como selecionada inicialmente
            multi=True  # Permitir seleção múltipla
        ),

        dcc.Graph(id='scatter-plot'),
        dcc.Graph(id='line-plot')
    ]
)


@app.callback(
    dash.dependencies.Output('scatter-plot', 'figure'),
    [dash.dependencies.Input('feature-selector', 'value')]
)
def update_scatter_plot(selected_features):
    traces = []

    # Criar uma trace de dispersão para cada feature selecionada
    for feature in selected_features:
        trace = go.Scatter(x=base['Datetime'], y=base[feature], mode='markers', name=feature)
        traces.append(trace)

    fig_scatter = go.Figure(data=traces)
    fig_scatter.update_layout(
        title='Distribuição das Features Selecionadas (Dispersão)',
        xaxis_title='Data',
        yaxis_title='Valor'
    )

    return fig_scatter


@app.callback(
    dash.dependencies.Output('line-plot', 'figure'),
    [dash.dependencies.Input('feature-selector', 'value')]
)
def update_line_plot(selected_features):
    traces = []

    # Criar uma trace de linha para cada feature selecionada
    for feature in selected_features:
        trace = go.Scatter(x=base['Datetime'], y=base[feature], mode='lines', name=feature)
        traces.append(trace)

    fig_line = go.Figure(data=traces)
    fig_line.update_layout(
        title='Distribuição das Features Selecionadas (Linha)',
        xaxis_title='Data',
        yaxis_title='Valor'
    )

    return fig_line


if __name__ == '__main__':
    app.run_server(debug=True, port=8052)