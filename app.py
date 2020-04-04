import pandas as pd
import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from pprint import pprint

from funcs import resolve_entry_form

from dash.dependencies import Input, Output, State

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

flask_server = flask.Flask(__name__)

app = dash.Dash(
    __name__,
    server=flask_server,
    url_base_pathname="/",
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True
)

server = app.server

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(
                    children=[html.H1(children="otrk")],
                    style={"text-align": "center"}
                ),
                html.Div(
                    children=[
                        html.H4(children="Option Trading Record Keeper")],
                    style={"text-align": "center"},
                ),
            ],
            className="row"),
        html.Br(),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.P(children='Entry Mode:'),
                        dcc.Dropdown(id='mode-dropdown',
                                     options=[
                                         {'label': 'Full Trade',
                                          'value': 'full'},
                                         {'label': 'Entry Trade',
                                          'value': 'entry'},
                                         {'label': 'Exit Trade',
                                          'value': 'exit'},
                                     ],
                                     placeholder='Select mode...')
                    ],
                    className='two columns offset-by-one column'),
                html.Div(
                    children=[
                        html.P(children='Timeframe:'),
                        dcc.Dropdown(id='timeframe-dropdown',
                                     options=[
                                         {'label': 'Dime',
                                          'value': 'dime'},
                                         {'label': 'Day',
                                          'value': 'day'},
                                         {'label': 'Swing',
                                          'value': 'swing'},
                                         {'label': 'Trend',
                                          'value': 'trend'},
                                         {'label': 'Investment',
                                          'value': 'investment'},
                                     ],
                                     placeholder='Select timeframe...')
                    ],
                    className='two columns'),
                html.Div(
                    children=[
                        html.P(children='Strategy:'),
                        dcc.Dropdown(id='strategy-dropdown',
                                     placeholder='Select strategy...')
                    ],
                    className='two columns'),
                html.Div(
                    children=[
                        html.P(children='Sub-Strategy:'),
                        dcc.Dropdown(id='sub-strategy-dropdown',
                                     placeholder='Select sub-strategy...',
                                     disabled=True)
                    ],
                    className='two columns'),
                html.Div(
                    children=[
                        html.P(children='Variation:'),
                        dcc.Dropdown(id='variation-dropdown',
                                     placeholder='Select variation...',
                                     disabled=True)
                    ],
                    className='two columns')],
            className="row"),
        html.Br(),
        html.Div(
            id='form',
            children=None,
            className='row'
        ),
        html.Div(
            id='output'
        )
    ]
)


@app.callback(Output('strategy-dropdown', 'options'),
              [Input('timeframe-dropdown', 'value')])
def generate_strategy_options(timeframe):
    if timeframe is not None:
        return [{'label': i, 'value': i.lower()}
                for i in strategy_options.get(timeframe)]
    else:
        return []


@app.callback([Output('sub-strategy-dropdown', 'options'),
               Output('sub-strategy-dropdown', 'disabled'),
               Output('variation-dropdown', 'options'),
               Output('variation-dropdown', 'disabled')],
              [Input('strategy-dropdown', 'value')],
              [State('timeframe-dropdown', 'value')])
def generate_ss_variation_options(strategy, timeframe):
    # print(strategy.split())
    print(strategy)
    tf_strat = timeframe + '-' + strategy.split()[0]
    # print(tf_strat)
    if tf_strat is not None and tf_strat in sub_strategy_options:
        sub_strategy = [{'label': i, 'value': i.lower()}
                        for i in sub_strategy_options.get(tf_strat)]
        sub_strategy_disabled = False
    else:
        sub_strategy = []
        sub_strategy_disabled = True
    if strategy is not None and strategy in variation_options:
        variation = [{'label': i, 'value': i.lower()}
                     for i in variation_options.get(strategy)]
        variation_disabled = False
    else:
        variation = []
        variation_disabled = True

    return sub_strategy, sub_strategy_disabled, variation, variation_disabled


@app.callback(Output('form', 'children'),
              [Input('mode-dropdown', 'value'),
               Input('timeframe-dropdown', 'value'),
               Input('strategy-dropdown', 'value')])
def generate_entry_form(mode, timeframe, strategy):
    selections = [mode, timeframe, strategy]
    return resolve_entry_form(selections)

# @app.callback(Output('output', 'children'),
#               [Input('entry-date-picker', 'date')])
# def print_date(date):
#     print(date)
#     return str(date)


strategy_options = {
    'dime': ['Dime Trend', 'FBB', 'Opening Candle',
             'Blowoff', 'Bollinger Band Channel', 'Sweet Spot',
             'Sentiment Shift'],
    'day': ['Fade', 'Channel', 'Gap Fill', 'Gap to MA', '3:30 Reversal',
            'Bounce', 'Scalp', 'Gap Against Trend', 'Retrace to Inside Band',
            'Hedge'],
    'swing': ['Earnings', 'Long', 'Short', 'Two-Day Rebound',
              'Put Credit Spread', 'Put Debit Spread', 'Call Credit Spread',
              'Call Debit Spread', 'Iron Butterfly', 'Iron Condor',
              'Straddle', 'Strangle', '15-Minute', 'Naked Puts'],
    'trend': ['Long', 'Covered Call', 'Naked Puts', 'Earnings'],
    'investment': ['Stock Purchase', 'Covered Calls']
}

sub_strategy_options = {
    'dime-fbb': ['Bullish', 'Bearish'],
    'dime-opening': ['Bullish', 'Bearish'],
    'swing-15': ['SIS', 'SS'],
    'trend-long': ['Bullish', 'Bearish'],
    'trend-earnings': ['Naked Puts', 'Covered Calls']
}

variation_options = {
    'dime trend': ['80/20', 'Add to'],
    'fbb': ['Add to'],
    'opening candle': ['Add to'],
    'blowoff': ['Add to'],
    'bollinger band channel': ['Add to'],
    'sweet spot': ['Add to'],
    'sentiment shift': ['Add to'],
}


if __name__ == "__main__":
    flask_server.run(debug=True)
