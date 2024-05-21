import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Cargar el conjunto de datos
df = pd.read_csv("ruta/a/tu/archivo.csv")

# Función para calcular la WCSS
def calculate_wcss(data):
    wcss_values = []
    for i in range(1, 11):  # Prueba desde 1 hasta 10 centros
        kmeans_result = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0).fit(data)
        wcss_values.append(kmeans_result.inertia_)
    return wcss_values

# Crear la UI de la aplicación Dash
app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Análisis de Clustering con KMeans")),
        ]),
        dbc.Row([
            dbc.Col(dcc.Upload(id='upload-data',
                                children=html.Div(['Arrastrar y soltar un archivo CSV aquí o ', html.A('Haz clic para seleccionar un archivo'), html.Br(), html.Br(),
                                                    html.A('Learn More')]),
                                style={'width': '100%', 'height': '60px', 'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
                                       'textAlign': 'center', 'margin': '10px'},
                                multiple=False)),
        ], justify="center"),
        dbc.Row([
            dbc.Col(dcc.Graph(id='cluster-graph')),
        ]),
        dbc.Row([
            dbc.Col(dbc.Table.from_dataframe(df.head(), striped=True, bordered=True, hover=True, dark=True)),
        ]),
    ])
], fluid=True)

@app.callback(Output('cluster-graph', 'figure'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename')])
def update_graph(contents, filename):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename:
                data = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            else:
                raise Exception('Archivo no soportado')
        except Exception as e:
            print(e)
            return html.Div([
                'Error cargando el archivo'
            ])

        # Preprocesamiento: Eliminar columnas no numéricas y/o manejar valores faltantes
        numeric_columns = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
        data_numeric = data[numeric_columns]

        # Calcular la WCSS para diferentes valores de k
        wcss_values = calculate_wcss(data_numeric)

        # Crear el gráfico
        fig = px.line(x=np.arange(1, len(wcss_values)+1), y=wcss_values,
                      labels={'x':'Cantidad de Centroides k', 'y':'WCSS'})
        fig.update_layout(title_text='Método del Codo')

        return fig

if __name__ == '__main__':
    app.run_server(debug=True)
