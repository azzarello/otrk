import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from datetime import datetime as dt


def resolve_entry_form(selections):
    for selection in selections:
        if selection is None:
            return
    return entry_layout


entry_layout = html.Div(children=[
    html.Div(
        html.Div(children=[
            html.P('Entry Date'),
            dcc.DatePickerSingle(
                id='entry-date-picker',
                min_date_allowed=dt(2015, 1, 1),
                max_date_allowed=dt.today(),
                initial_visible_month=dt(dt.today().year, dt.today().month, 1),
                display_format='M/D/YYYY'
            )
        ]),
        className='two columns offset-by-one column'),
    html.Div(
        html.Div(children=[
            html.P('Strike Price'),
            dcc.Input(
                id='entry-strike-price',
                type='number',
                placeholder='Enter strike price...'
            )
        ]),
        className='two columns'),
    html.Div(
        html.Div(children=[
            html.P('Ticker'),
            dcc.Input(
                id='entry-ticker',
                type='text',
                placeholder='Enter ticker...'
            )
        ]),
        className='two columns'),
    html.Div(
        html.Div(children=[
            html.P('Quantity'),
            dcc.Input(
                id='entry-quantity',
                type='number',
                placeholder='Enter quantity...'
            )
        ]),
        className='two columns'),

])
