##==================================
## External imports
##==================================
import os
import io
import flask
import urllib
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

##==================================
## Internal imports
##==================================
# Import app and cache
from app import app, cache

# Import all layouts
from layouts import loading, home, request_password, request_confirm, app_main
from layouts import help_documentation, filler, examples_page, lines, pca
from layouts import feedback, feedback_confirm

from layouts.global_layout import bubble_nav_logo, data_table
from layouts.examples import example_1, example_2, example_3, example_4, example_5

# Import callbacks for individual apps
from callbacks import home_call, request_password_call, app_main_call
from callbacks import example_1_call, example_2_call, example_3_call, example_4_call, example_5_call
from callbacks import lines_call, pca_call, feedback_call

# Import functions
from functions.global_functions import unpickleData

##==================================
## Initialize app layout
##==================================
def serve_layout():
    return html.Div([
            html.Div(
                loading.layout(),
                id = 'page-content'
            ),
            dcc.Location(id='url', refresh = False),
            dbc.Input(id = 'password-store', style = dict(display='none')),
            bubble_nav_logo.get(),
        ]
    )
app.layout = serve_layout()
##==========================================
## Callbacks to determine layout based on url
##===========================================
@app.callback(
    Output('page-content', 'children'),
    [
        Input('url', 'pathname'),
        Input('password-store','value')
    ],
)
def display_page(pathname, authenticate):

    # Direct user to correct layout (page)
    if pathname == '/':
        return app_main.layout()
    elif pathname == '/lines':
        return lines.layout()
    elif pathname == '/pca':
        return pca.layout()
    elif pathname == '/':
        return home.layout()
    elif pathname == '/lines':
        return home.layout()
    elif pathname == '/pca':
        return home.layout()
    elif pathname == '/request-password':
        return request_password.layout()
    elif pathname == '/request-confirm':
        return request_confirm.layout()
    elif pathname == '/contact-us':
        return feedback.layout()
    elif pathname == '/contact-us-confirm':
        return feedback_confirm.layout()
    elif pathname == '/help':
        return help_documentation.layout()
    elif pathname == '/examples':
        return examples_page.layout()
    elif pathname == '/example-1':
        return example_1.layout()
    elif pathname == '/example-2':
        return example_2.layout()
    elif pathname == '/example-3':
        return example_3.layout()
    elif pathname == '/example-4':
        return example_4.layout()
    elif pathname == '/example-5':
        return example_5.layout()
    elif pathname is not None and 'temp' in pathname:
        return loading.layout()
    else:
        return filler.layout()

##==========================================
## Callbacks for clearing data
##===========================================
@app.callback(
    Output('url', 'pathname'),
    [
        Input('clear-data-link', 'n_clicks'),
    ],
    [
        State('url','pathname')
    ],
    prevent_initial_call=True
)
def clean_refresh(n_clicks, temp_pathname):
    # Prevent updates
    if n_clicks is None:
        raise PreventUpdate

    if temp_pathname is None:
        raise PreventUpdate

    # Update the URL to clear the page
    return temp_pathname

##==========================================
## Callback for downloading data
##===========================================
@app.server.route('/._cache-directory/')
def download_csv():
    # Get the session ID when requested
    session_id = flask.request.args.get('value')

    # Unpickle the data based on the sessionID
    data = unpickleData(session_id)

    # Use string IO to make CSV for output
    str_io = io.StringIO()
    data.to_csv(str_io, index=False)
    mem = io.BytesIO()
    mem.write(str_io.getvalue().encode('utf-8'))
    mem.seek(0)
    str_io.close()

    return flask.send_file(mem,
                           mimetype = 'text/csv',
                           attachment_filename = 'data.csv',
                           as_attachment = True)

##==========================================
## Calling index.py
##===========================================

server = app.server
if __name__ == '__main__':
    # Get the port number
    if os.getenv("PORT") is None:
        port = 5000
    else:
        port = int(os.getenv("PORT"))
    
    # Serve app from specified port
    app.run_server(host='0.0.0.0', port = port)
