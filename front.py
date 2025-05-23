import dash
from dash import dcc, html, dash_table, Input, Output, State
import requests
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

# URL base de la API
API_BASE_URL = "https://carsmoviesinventoryproject-production.up.railway.app/api/v1/carsmovies"

# Obtener los datos de la API (GET)
def fetch_data():
    response = requests.get(f"{API_BASE_URL}?page=0&size=100&sort=carMovieYear,desc")
    if response.status_code == 200:
        return response.json().get("Movies", [])
    return []

# Crear nueva película (POST)
def create_movie(movie):
    response = requests.post(API_BASE_URL, json=movie)
    return response.status_code == 201

# Actualizar película (PUT)
def update_movie(movie_id, updated_movie):
    response = requests.put(f"{API_BASE_URL}/{movie_id}", json=updated_movie)
    return response.status_code == 200

# Eliminar película (DELETE)
def delete_movie(movie_id):
    response = requests.delete(f"{API_BASE_URL}/{movie_id}")
    return response.status_code == 204

# Inicializar la app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
app.title = "Cars Movies Dashboard"

# Layout
app.layout = dbc.Container(
    fluid=True,
    style={"backgroundColor": "#f8f9fa", "maxWidth": "1200px", "margin": "0 auto", "paddingTop": "20px", "color": "black"},
    children=[
        dbc.Row(dbc.Col(html.Div([
            html.H1("Dashboard de Películas", className="display-3 text-center", style={'fontWeight': '300'}),
        ], style={'backgroundColor': '#343a40', 'padding': '30px', 'borderRadius': '15px', 'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)', 'marginBottom': '40px'}), width=12)),
        
        dbc.Row([
            dbc.Col(dbc.Button("Agregar Película", id="add-movie-btn", color="primary", size="lg", style={"width": "100%", 'fontWeight': '600'}), width=12, md=3),
            dbc.Col(dbc.Button("Actualizar", id="update-movie-btn", color="primary", size="lg", style={"width": "100%", 'fontWeight': '600'}), width=12, md=3),
            dbc.Col(dbc.Button("Eliminar", id="delete-movie-btn", color="primary", size="lg", style={"width": "100%", 'fontWeight': '600'}), width=12, md=3),
            dbc.Col(dbc.Button("Ver Listado", id="view-movie-btn", color="primary", size="lg", style={"width": "100%", 'fontWeight': '600'}), width=12, md=3),
        ], className="mb-4", style={'marginBottom': '40px'}),
        
        dbc.Row(dbc.Col(dcc.Input(id="search-input", type="text", placeholder="Buscar película por nombre...", style={"width": "100%", "padding": "10px", "fontSize": "18px", "borderRadius": "5px"}), width=12), style={"marginBottom": "30px"}),

        dbc.Row(dbc.Col(dbc.Card(dbc.CardBody([
            html.H4("Listado de Películas", className="card-title", style={'fontSize': '22px', 'fontWeight': 'bold'}),
            dash_table.DataTable(
                id='movies-table',
                columns=[
                    {"name": "ID", "id": "id"},
                    {"name": "Nombre", "id": "carMovieName"},
                    {"name": "Año", "id": "carMovieYear"},
                    {"name": "Duración (min)", "id": "duration"}
                ],
                data=fetch_data(),
                editable=True,
                row_deletable=True,
                style_table={'overflowX': 'auto', 'borderRadius': '10px', 'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.2)', 'backgroundColor': '#FFFFFF', 'marginTop': '20px'},
                style_cell={'textAlign': 'left', 'padding': '12px', 'fontSize': '16px', 'fontFamily': 'Arial, sans-serif', 'color': '#000000'},
                style_header={'backgroundColor': '#007bff', 'color': 'white', 'fontWeight': 'bold', 'textAlign': 'center', 'borderTopLeftRadius': '10px', 'borderTopRightRadius': '10px'},
                page_size=5,
                style_data_conditional=[
                    {'if': {'row_index': 'odd'}, 'backgroundColor': '#f1f1f1'},
                    {'if': {'state': 'selected'}, 'backgroundColor': '#4e73df'}
                ]
            )
        ])), width=12))
    ]
)

@app.callback(
    Output('movies-table', 'data'),
    Input('add-movie-btn', 'n_clicks'),
    Input('update-movie-btn', 'n_clicks'),
    Input('delete-movie-btn', 'n_clicks'),
    Input('view-movie-btn', 'n_clicks'),
    Input('search-input', 'value'),
    State('movies-table', 'data'),
    State('movies-table', 'selected_rows'),
    prevent_initial_call=True
)
def handle_crud(add_clicks, update_clicks, delete_clicks, view_clicks, search_value, current_data, selected_rows):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'add-movie-btn':
        new_movie = {
            "carMovieName": "Nueva Película",
            "carMovieYear": 2025,
            "duration": 100
        }
        create_movie(new_movie)

    elif trigger_id == 'update-movie-btn':
        if selected_rows:
            selected_index = selected_rows[0]
            selected_movie = current_data[selected_index]
            updated_movie = {
                "carMovieName": selected_movie["carMovieName"] + " (Actualizado)",
                "carMovieYear": selected_movie["carMovieYear"],
                "duration": selected_movie["duration"]
            }
            update_movie(selected_movie["id"], updated_movie)

    elif trigger_id == 'delete-movie-btn':
        if selected_rows:
            for i in selected_rows:
                delete_movie(current_data[i]["id"])

    elif trigger_id == 'search-input' and search_value:
        return [m for m in fetch_data() if search_value.lower() in m['carMovieName'].lower()]

    return fetch_data()

# Ejecutar servidor
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
