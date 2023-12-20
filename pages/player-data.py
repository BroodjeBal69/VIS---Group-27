import dash
from dash import html, dcc, Input, Output, callback, Dash, dash_table
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import re

df_player_stats = pd.read_csv('../Data/FIFA World Cup 2022 Player Data/player_stats.csv', delimiter=',')
df_scaled = pd.read_csv('df_scaled.csv')

colors = {
    'background': '#0E1B2A',
    'text': '#FFFFFF',
    'dropdown' : '#000000'
}


dash.register_page(__name__,
                   path='/player-data',
                    title='World cup players',
                    name='World cup players')

layout = html.Div([
    html.H1('Player data'),
    html.Div('Select World Cup player:'),
    html.Div([
            dcc.Dropdown(df_player_stats["player"].unique(), "Denzel Dumfries", id='demo-dropdown', searchable=True, style = {'color' : colors['dropdown']})
        ]),
        html.Div([
            dash_table.DataTable(
       id='player-ratings',
       columns=[{"name": i, "id": i} for i in df_scaled[['name', 'rating', 'match']].columns],
        data=df_scaled[df_scaled["name"] == "Denzel Dumfries"][['name', 'rating', 'match']].to_dict('records'),
        editable=True,
    #     style_header={
    #     'backgroundColor': 'rgb(30, 30, 30)',
    #     'color': 'white'
    # },
    #     style_data={
    #     'backgroundColor': 'rgb(50, 50, 50)',
    #     'color': 'white'
    # },
   ),
    ])
])

@callback(
    Output('player-ratings', 'data'),
    [Input('demo-dropdown', 'value')]
)

def update_table(value):
    filtered_data = df_scaled[df_scaled["name"] == value][['name', 'rating', 'match']].to_dict('records')
    return filtered_data
