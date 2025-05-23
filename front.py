import dash
from dash import dcc, html, dash_table, Input, Output, State
import requests
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

# URL de la API
API_URL = "https://carsmoviesinventoryproject-production.up.railway.app/api/v1/carsmovies?page=0&size=5&sort=carMovieYear,desc"

# Obtener los datos de la API
def fetch_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json().get("Movies", [])
    return []

# Inicializar la app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
app.title = "Cars Movies Dashboard"

# Variable global para almacenar los datos de las películas
movie_data = fetch_data()

# Layout
app.layout = dbc.Container(
    fluid=True,
    style={
        "backgroundColor": "#f8f9fa",  # Fondo blanco claro
        "maxWidth": "1200px",
        "margin": "0 auto",
        "paddingTop": "20px",
        "color": "black"  # Color de texto negro
    },
    children=[
        # Título
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H1("Dashboard de Películas", className="display-3 text-center", style={'fontWeight': '300'}),
                    ],
                    style={
                        'backgroundColor': '#343a40',  # Fondo gris oscuro
                        'padding': '30px',
                        'borderRadius': '15px',
                        'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)',  # Sombra suave
                        'marginBottom': '40px'  # Separación del título con otros elementos
                    }
                ),
                width=12
            )
        ),

        # Fila de botones de acción con todos los botones en azul
        dbc.Row([
            dbc.Col(
                dbc.Button(
                    children="Agregar Película", 
                    id="add-movie-btn", 
                    color="primary", 
                    size="lg", 
                    style={"width": "100%", 'fontWeight': '600'}
                ),
                width=12, md=3
            ),
            dbc.Col(
                dbc.Button(
                    children="Actualizar", 
                    id="update-movie-btn", 
                    color="primary", 
                    size="lg", 
                    style={"width": "100%", 'fontWeight': '600'}
                ),
                width=12, md=3
            ),
            dbc.Col(
                dbc.Button(
                    children="Eliminar", 
                    id="delete-movie-btn", 
                    color="primary", 
                    size="lg", 
                    style={"width": "100%", 'fontWeight': '600'}
                ),
                width=12, md=3
            ),
            dbc.Col(
                dbc.Button(
                    children="Ver Listado", 
                    id="view-movie-btn", 
                    color="primary", 
                    size="lg", 
                    style={"width": "100%", 'fontWeight': '600'}
                ),
                width=12, md=3
            ),
        ], className="mb-4", style={'marginBottom': '40px'}),  # Mayor separación entre los botones y la tabla

        # Fila del buscador
        dbc.Row(
            dbc.Col(
                dcc.Input(
                    id="search-input", 
                    type="text", 
                    placeholder="Buscar película por nombre...", 
                    style={"width": "100%", "padding": "10px", "fontSize": "18px", "borderRadius": "5px"}
                ),
                width=12
            ),
            style={"marginBottom": "30px"}  # Separación del buscador de la tabla
        ),

        # Card para contener la tabla de películas
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H4("Listado de Películas", className="card-title", style={'fontSize': '22px', 'fontWeight': 'bold'}),
                        dash_table.DataTable(
                            id='movies-table',
                            columns=[
                                {"name": "ID", "id": "id"},
                                {"name": "Nombre", "id": "carMovieName"},
                                {"name": "Año", "id": "carMovieYear"},
                                {"name": "Duración (min)", "id": "duration"}
                            ],
                            data=movie_data,
                            editable=True,
                            row_deletable=True,
                            style_table={
                                'overflowX': 'auto',
                                'borderRadius': '10px',
                                'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.2)',  # Sombra suave
                                'backgroundColor': '#FFFFFF',  # Fondo blanco para la tabla
                                'marginTop': '20px',  # Separación superior de la tabla
                            },
                            style_cell={
                                'textAlign': 'left',
                                'padding': '12px',
                                'fontSize': '16px',
                                'fontFamily': 'Arial, sans-serif',
                                'color': '#000000'  # Texto negro para la tabla
                            },
                            style_header={
                                'backgroundColor': '#007bff',  # Azul para los encabezados
                                'color': 'white',
                                'fontWeight': 'bold',
                                'textAlign': 'center',
                                'borderTopLeftRadius': '10px',
                                'borderTopRightRadius': '10px'
                            },
                            page_size=5,
                            style_data_conditional=[
                                {'if': {'row_index': 'odd'}, 'backgroundColor': '#f1f1f1'},  # Fondo gris claro para filas impares
                                {'if': {'state': 'selected'}, 'backgroundColor': '#4e73df'}  # Resaltado al seleccionar
                            ]
                        )
                    ])
                ),
                width=12
            )
        )
    ]
)

# Callback para manejar todas las interacciones con los botones
@app.callback(
    Output('movies-table', 'data'),
    Input('add-movie-btn', 'n_clicks'),
    Input('update-movie-btn', 'n_clicks'),
    Input('delete-movie-btn', 'n_clicks'),
    Input('search-input', 'value'),
    State('movies-table', 'data'),
    State('movies-table', 'selected_rows'),
    prevent_initial_call=True
)
def update_table(add_clicks, update_clicks, delete_clicks, search_value, current_data, selected_rows):
    # Agregar película
    if add_clicks:
        new_movie = {
            'id': len(current_data) + 1,
            'carMovieName': "Nueva Película",
            'carMovieYear': 2025,
            'duration': 120
        }
        current_data.append(new_movie)

    # Actualizar película
    if update_clicks:
        current_data = fetch_data()

    # Eliminar película
    if delete_clicks and selected_rows:
        selected_ids = [current_data[i]['id'] for i in selected_rows]
        current_data = [movie for movie in current_data if movie['id'] not in selected_ids]

    # Buscar película
    if search_value:
        current_data = [movie for movie in current_data if search_value.lower() in movie['carMovieName'].lower()]

    return current_data

# Ejecutar el servidor
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
