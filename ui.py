import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

from plotly import tools
import plotly.graph_objs as go

from model import get_total_by_instrument, get_total_by_sector


SECTOR_CHART_HEIGHT = 330

df_instrument = get_total_by_instrument()
df_sector = get_total_by_sector()

x_range = min(df_instrument.index), max(df_instrument.index)


def _figure_from_df(df, select_enabled=False, title='', height=None):
    return {
        'data': [
            go.Bar(
                x = df.index,
                y = df[name],
                name = name,
                marker = {
                    'line': {
                        'width': 0,
                    },
                },
            ) for name in df.columns
            ],
        'layout': {
            'title': title,
            'xaxis': {
                'range': x_range,
            },
            'yaxis': {
                'autorange': True,
            },            
            'barmode': 'stack',
            'clickmode': 'event+select' if select_enabled else '',
            'legend': {
                'x': 0,
                'y': 1,
            },
            'cursor': 'pointer',
            'bargap': 0,
            'height': height,
        },
    }

external_stylesheets = []#['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Banxico Total Outstanding Debt', style=dict(textAlign='center')),
    html.Div([
        dcc.Graph(
            id='instrument-bars',
            figure=_figure_from_df(
                df_instrument,
                select_enabled=True,
                title='Outstanding Debt by Instrument Type')
        ),
        dcc.Graph(
            id='sector-bars',        
            figure=_figure_from_df(
                df_sector,
                title='Sector Breakdown',
                height=SECTOR_CHART_HEIGHT,
            )
        ),
    ]),        

    html.Div(children='''
        Source: https://www.banxico.org.mx/SieAPIRest/service/v1/doc/catalogoSeries
    '''),
])


@app.callback(
    Output('sector-bars', 'figure'),
    [Input('instrument-bars', 'selectedData')],
)
def drilldown_instrument(evt):
    if evt is not None:
        series = set([p['curveNumber'] for p in evt['points']])
        instrument_types = [df_instrument.columns[i] for i in series]
        df = get_total_by_sector(frozenset(instrument_types))
        return _figure_from_df(
            df,
            title='Sector Breakdown for %s Bonds' % ', '.join(instrument_types),
            height=SECTOR_CHART_HEIGHT,
        )
    global df_sector
    return _figure_from_df(
        df_sector,
        title='Sector Breakdown',
        height=SECTOR_CHART_HEIGHT,        
    )


if __name__ == '__main__':
    app.run_server(debug=True)
