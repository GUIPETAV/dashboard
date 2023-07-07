import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

url = 'https://raw.githubusercontent.com/GUIPETAV/Base/main/base_media_30m.csv'

base = pd.read_csv(url)
base['Datetime'] = pd.to_datetime(base['Datetime'])

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
        html.H1("Visualização dos dados reais ", id="h1", style={'text-align': 'center'}),

        # Caixas de seleção para as features
        dcc.Dropdown(
            id='feature-selector',
            options=[{'label': feature, 'value': feature} for feature in features],
            value=[features[1]],  # Defina a primeira feature como selecionada inicialmente
            multi=True  # Permitir seleção múltipla
        ),

        # Campos de seleção para a data de início e fim
        dcc.DatePickerSingle(
            id='start-date-selector',
            placeholder='Select a start date',
            date=datetime.now().date()  # Defina a data de início como a data atual
        ),

        dcc.DatePickerSingle(
            id='end-date-selector',
            placeholder='Select an end date',
            date=datetime.now().date()  # Defina a data de fim como a data atual
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
     dash.dependencies.Input('end-date-selector', 'date')]
)
def update_scatter_plot(selected_features, start_date, end_date):
    traces = []

    if start_date and end_date:
        try:
            start_date = pd.to_datetime(start_date).date()
            end_date = pd.to_datetime(end_date).date()

            # Filter the data based on the selected start and end dates
            filtered_data = base[
                (base['Datetime'].dt.date >= start_date) & (base['Datetime'].dt.date <= end_date)
            ]

            # Create a scatter plot trace for each selected feature
            for feature in selected_features:
                trace = go.Scatter(x=filtered_data['Datetime'], y=filtered_data[feature], mode='markers', name=feature)
                traces.append(trace)

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
     dash.dependencies.Input('end-date-selector', 'date')]
)
def update_line_plot(selected_features, start_date, end_date):
    traces = []

    if start_date and end_date:
        try:
            start_date = pd.to_datetime(start_date).date()
            end_date = pd.to_datetime(end_date).date()

            # Filter the data based on the selected start and end dates
            filtered_data = base[
                (base['Datetime'].dt.date >= start_date) & (base['Datetime'].dt.date <= end_date)
            ]

            # Create a line plot trace for each selected feature
            for feature in selected_features:
                trace = go.Scatter(x=filtered_data['Datetime'], y=filtered_data[feature], mode='lines', name=feature)
                traces.append(trace)

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
     dash.dependencies.Input('end-date-selector', 'date')]
)
def update_box_plot(selected_features, start_date, end_date):
    traces = []

    if start_date and end_date:
        try:
            start_date = pd.to_datetime(start_date).date()
            end_date = pd.to_datetime(end_date).date()

            # Filter the data based on the selected start and end dates
            filtered_data = base[
                (base['Datetime'].dt.date >= start_date) & (base['Datetime'].dt.date <= end_date)
            ]

            # Create a box plot trace for each selected feature
            for feature in selected_features:
                trace = go.Box(y=filtered_data[feature], name=feature)
                traces.append(trace)

        except Exception as e:
            print(f"Error: {e}")
            return go.Figure()

    fig_box = go.Figure(data=traces)
    fig_box.update_layout(
        title='Distribution of Selected Features (Boxplot)',
        yaxis_title='Value'
    )

    return fig_box


if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
