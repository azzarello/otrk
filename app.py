import pandas as pd
import flask
import dash
import dash_core_components as dash_core_components
import dash_html_components as html
import dash_table as dt
from pprint import pprint

from dash.dependencies import Input, Output, State

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

flask_server = flask.Flask(__name__)

app = dash.Dash(
    __name__,
    server=flask_server,
    url_base_pathname="/",
    external_stylesheets=external_stylesheets,
)

server = app.server

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(
                    children=[html.H1(children="otrk")], style={"text-align": "center"}
                ),
                html.Div(
                    children=[html.H4(children="Option Trading Record Keeper")],
                    style={"text-align": "center"},
                ),
            ],
        ),
        html.Div(dt.DataTable(id="table")),
    ]
)


if __name__ == "__main__":
    flask_server.run(debug=True)
