import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from datetime import datetime, timedelta



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)


server = app.server
# Ajustes da pagina 1 
# ajustes dos dados reais  

url1 = 'https://raw.githubusercontent.com/GUIPETAV/Base/main/base_media_30m.csv'

base = pd.read_csv(url1)
base['Datetime'] = pd.to_datetime(base['Datetime'])


# Lista de features disponíveis
features = base.columns[1:]

# Lista vazia para armazenar as features selecionadas
selected_features = []

fig_scatter = go.Figure()
fig_line = go.Figure()


# Definir o layout das páginas
page1_layout =html.Div(
    id="div1",
    children=[
        html.H1("Visualização dos dados reais ", id="h1", style={'text-align': 'center'}),

        # Caixas de seleção para as features
        dcc.Dropdown(
            id='feature-selector',
            options=[{'label': feature, 'value': feature} for feature in features],
            value=[features[1]],  # Defina a primeira feature como selecionada inicialmente
            multi=True  # Permitir seleção múltipla
        ),

        # Campos de seleção para o primeiro intervalo de data
        dcc.DatePickerSingle(
            id='start-date-selector',
            placeholder='Select a start date for the first interval',
            date=datetime.now().date() - timedelta(days=7)  # Defina a data de início do primeiro intervalo
        ),

        dcc.DatePickerSingle(
            id='end-date-selector',
            placeholder='Select an end date for the first interval',
            date=datetime.now().date()  # Defina a data de fim do primeiro intervalo
        ),

        # Campos de seleção para o segundo intervalo de data
        dcc.DatePickerSingle(
            id='start-date-selector-2',
            placeholder='Select a start date for the second interval',
            date=datetime.now().date() - timedelta(days=14)  # Defina a data de início do segundo intervalo
        ),

        dcc.DatePickerSingle(
            id='end-date-selector-2',
            placeholder='Select an end date for the second interval',
            date=datetime.now().date() - timedelta(days=7)  # Defina a data de fim do segundo intervalo
        ),

        dcc.Graph(id='scatter-plot'),
        dcc.Graph(id='line-plot'),
        dcc.Graph(id='box-plot')
    ]
)


@app.callback(
    dash.dependencies.Output('scatter-plot', 'figure'),
    [dash.dependencies.Input('feature-selector', 'value'),
     dash.dependencies.Input('start-date-selector', 'date'),
     dash.dependencies.Input('end-date-selector', 'date'),
     dash.dependencies.Input('start-date-selector-2', 'date'),
     dash.dependencies.Input('end-date-selector-2', 'date')]
)
def update_scatter_plot(selected_features, start_date, end_date, start_date_2, end_date_2):
    traces = []

    if start_date and end_date and start_date_2 and end_date_2:
        try:
            start_date = pd.to_datetime(start_date).date()
            end_date = pd.to_datetime(end_date).date()
            start_date_2 = pd.to_datetime(start_date_2).date()
            end_date_2 = pd.to_datetime(end_date_2).date()

            # Filter the data based on the selected intervals
            filtered_data_1 = base[
                (base['Datetime'].dt.date >= start_date) & (base['Datetime'].dt.date <= end_date)
            ]
            filtered_data_2 = base[
                (base['Datetime'].dt.date >= start_date_2) & (base['Datetime'].dt.date <= end_date_2)
            ]

            # Create scatter plot traces for each selected feature and interval
            for feature in selected_features:
                trace_1 = go.Scatter(x=filtered_data_1['Datetime'], y=filtered_data_1[feature],
                                     mode='markers', name=f"{feature} - Interval 1")
                trace_2 = go.Scatter(x=filtered_data_2['Datetime'], y=filtered_data_2[feature],
                                     mode='markers', name=f"{feature} - Interval 2")
                traces.append(trace_1)
                traces.append(trace_2)

        except Exception as e:
            print(f"Error: {e}")
            return go.Figure()

    fig_scatter = go.Figure(data=traces)
    fig_scatter.update_layout(
        title='Distribution of Selected Features (Scatter)',
        xaxis_title='Date',
        yaxis_title='Value'
    )

    return fig_scatter


@app.callback(
    dash.dependencies.Output('line-plot', 'figure'),
    [dash.dependencies.Input('feature-selector', 'value'),
     dash.dependencies.Input('start-date-selector', 'date'),
     dash.dependencies.Input('end-date-selector', 'date'),
     dash.dependencies.Input('start-date-selector-2', 'date'),
     dash.dependencies.Input('end-date-selector-2', 'date')]
)
def update_line_plot(selected_features, start_date, end_date, start_date_2, end_date_2):
    traces = []

    if start_date and end_date and start_date_2 and end_date_2:

        try:
            start_date = pd.to_datetime(start_date).date()
            end_date = pd.to_datetime(end_date).date()
            start_date_2 = pd.to_datetime(start_date_2).date()
            end_date_2 = pd.to_datetime(end_date_2).date()

            # Filter the data based on the selected intervals
            filtered_data_1 = base[
                (base['Datetime'].dt.date >= start_date) & (base['Datetime'].dt.date <= end_date)
            ]
            filtered_data_2 = base[
                (base['Datetime'].dt.date >= start_date_2) & (base['Datetime'].dt.date <= end_date_2)
            ]

            # Create line plot traces for each selected feature and interval
            for feature in selected_features:
                trace_1 = go.Scatter(x=filtered_data_1['Datetime'], y=filtered_data_1[feature],
                                     mode='lines', name=f"{feature} - Interval 1")
                trace_2 = go.Scatter(x=filtered_data_2['Datetime'], y=filtered_data_2[feature],
                                     mode='lines', name=f"{feature} - Interval 2")
                traces.append(trace_1)
                traces.append(trace_2)

        except Exception as e:
            print(f"Error: {e}")
            return go.Figure()

    fig_line = go.Figure(data=traces)
    fig_line.update_layout(
        title='Distribution of Selected Features (Line)',
        xaxis_title='Date',
        yaxis_title='Value'
    )

    return fig_line


@app.callback(
     dash.dependencies.Output('box-plot', 'figure'),
    [dash.dependencies.Input('feature-selector', 'value'),
     dash.dependencies.Input('start-date-selector', 'date'),
     dash.dependencies.Input('end-date-selector', 'date'),
     dash.dependencies.Input('start-date-selector-2', 'date'),
     dash.dependencies.Input('end-date-selector-2', 'date')]
)
def update_box_plot(selected_features, start_date, end_date, start_date_2, end_date_2):
    traces = []

    if start_date and end_date and start_date_2 and end_date_2:
        try:
            start_date = pd.to_datetime(start_date).date()
            end_date = pd.to_datetime(end_date).date()
            start_date_2 = pd.to_datetime(start_date_2).date()
            end_date_2 = pd.to_datetime(end_date_2).date()

            # Filter the data based on the selected intervals
            filtered_data_1 = base[
                (base['Datetime'].dt.date >= start_date) & (base['Datetime'].dt.date <= end_date)
            ]
            filtered_data_2 = base[
                (base['Datetime'].dt.date >= start_date_2) & (base['Datetime'].dt.date <= end_date_2)
            ]

            # Create box plot traces for each selected feature and interval
            for feature in selected_features:
                trace_1 = go.Box(y=filtered_data_1[feature], name=f"{feature} - Interval 1")
                trace_2 = go.Box(y=filtered_data_2[feature], name=f"{feature} - Interval 2")
                traces.append(trace_1)
                traces.append(trace_2)

        except Exception as e:
            print(f"Error: {e}")
            return go.Figure()

    fig_box = go.Figure(data=traces)
    fig_box.update_layout(
        title='Distribution of Selected Features (Boxplot)',
        yaxis_title='Value'
    )

    return fig_box



page2_layout = html.Div([
    html.H1("Visualização dos dados simulados", id="h1", style={'text-align': 'center'}),
    # Conteúdo da página 2...
])

page3_layout = html.Div([
    html.H1("Classificadores reais/reais", id="h1", style={'text-align': 'center'}),
    # Conteúdo da página 3...
])

page4_layout = html.Div([
    html.H1("Classificadores simulado/simulado", id="h1", style={'text-align': 'center'}),
    # Conteúdo da página 4...
])

page5_layout = html.Div([
    html.H1("Classificadores simulado/reais", id="h1", style={'text-align': 'center'}),
    # Conteúdo da página 5...
])

# Layout principal com guias
app.layout = html.Div([
    dcc.Tabs(id='tabs', value='page1', children=[
        dcc.Tab(label='Visualização dos dados reais', value='page1'),
        dcc.Tab(label='Visualização dos dados simulados', value='page2'),
        dcc.Tab(label='Classificadores reais/reais ', value='page3'),
        dcc.Tab(label='Classificadores simulado/simulado ', value='page4'),
        dcc.Tab(label='Classificadores simulado/reais ', value='page5'),
    ]),
    html.Div(id='page-content')
])

# Callback para alternar o conteúdo com base na guia selecionada
@app.callback(Output('page-content', 'children'), [Input('tabs', 'value')])
def render_page_content(tab):
    if tab == 'page1':
        return page1_layout
    elif tab == 'page2':
        return page2_layout
    elif tab == 'page3':
        return page3_layout
    elif tab == 'page4':
        return page4_layout
    elif tab == 'page5':
        return page5_layout
    else:
        return html.Div('Página não encontrada')

if __name__ == '__main__':
    app.run_server(debug=True)
