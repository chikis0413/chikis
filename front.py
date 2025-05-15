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
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Cars Movies Dashboard"

# Variable global para almacenar los datos de las películas
movie_data = fetch_data()

# Layout
app.layout = dbc.Container(
    fluid=True,
    style={"width": "70%", "margin": "0 auto"},  # Página ocupa el 70% de la pantalla
    children=[
        # Título
        dbc.Row(
            dbc.Col(
                html.Div(
                    html.H1("Dashboard de Películas", className="display-3 text-center text-light"),
                    style={'backgroundColor': '#343a40', 'padding': '40px', 'borderRadius': '10px'}
                )
            )
        ),

        # Fila de botones de acción
        dbc.Row([
            dbc.Col(
                dbc.Button("Agregar Película", id="add-movie-btn", color="primary", style={"width": "100%"}),
                width=12, md=3
            ),
            dbc.Col(
                dbc.Button("Actualizar Películas", id="update-movie-btn", color="secondary", style={"width": "100%"}),
                width=12, md=3
            ),
            dbc.Col(
                dbc.Button("Eliminar Película", id="delete-movie-btn", color="danger", style={"width": "100%"}),
                width=12, md=3
            ),
            dbc.Col(
                dbc.Button("Ver Listado", id="view-movie-btn", color="info", style={"width": "100%"}),
                width=12, md=3
            ),
        ], className="mb-4"),

        # Tabla de películas
        dbc.Row(
            dbc.Col(
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
                    style_table={'overflowX': 'auto', 'borderRadius': '10px', 'boxShadow': '0px 4px 6px rgba(0,0,0,0.1)'},
                    style_cell={'textAlign': 'left', 'padding': '8px', 'fontSize': '16px', 'fontFamily': 'Arial, sans-serif'},
                    style_header={'backgroundColor': '#007bff', 'color': 'white', 'fontWeight': 'bold'},
                    page_size=5,
                    style_data_conditional=[
                        {'if': {'row_index': 'odd'}, 'backgroundColor': '#f8f9fa'}
                    ]
                )
            )
        )
    ]
)

# Callback para agregar una película
@app.callback(
    Output('movies-table', 'data'),
    Input('add-movie-btn', 'n_clicks'),
    State('movies-table', 'data'),
    prevent_initial_call=True
)
def add_movie(n_clicks, current_data):
    if not n_clicks:
        raise PreventUpdate
    # Agregar una película al listado (con datos de ejemplo)
    new_movie = {
        'id': len(current_data) + 1,
        'carMovieName': "Nueva Película",
        'carMovieYear': 2025,
        'duration': 120
    }
    current_data.append(new_movie)
    return current_data

# Callback para actualizar la tabla con los datos más recientes
@app.callback(
    Output('movies-table', 'data'),
    Input('update-movie-btn', 'n_clicks'),
    prevent_initial_call=True
)
def update_movie_list(n_clicks):
    global movie_data
    if not n_clicks:
        raise PreventUpdate
    movie_data = fetch_data()  # Actualiza con los datos de la API
    return movie_data

# Callback para eliminar una película
@app.callback(
    Output('movies-table', 'data'),
    Input('delete-movie-btn', 'n_clicks'),
    State('movies-table', 'selected_rows'),
    State('movies-table', 'data'),
    prevent_initial_call=True
)
def delete_movie(n_clicks, selected_rows, current_data):
    if not n_clicks or not selected_rows:
        raise PreventUpdate
    selected_ids = [current_data[i]['id'] for i in selected_rows]
    updated_data = [movie for movie in current_data if movie['id'] not in selected_ids]
    return updated_data


# Ejecutar el servidor
if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)