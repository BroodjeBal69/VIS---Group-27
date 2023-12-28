import dash
from dash import html, dcc, Input, Output, callback, Dash, dash_table
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import re

df_player_stats = pd.read_csv('../Data/FIFA World Cup 2022 Player Data/player_stats.csv', delimiter=',')
df_scaled = pd.read_csv('df_scaled.csv')
df_scaled_filtered = df_scaled[df_scaled['name']== 'Denzel Dumfries']

colors = {
    'background': '#0E1B2A',
    'text': '#FFFFFF',
    'dropdown' : '#000000'
}

fig = make_subplots(rows=1, cols=1)
fig.add_trace(go.Scatter(y=df_scaled_filtered['rating']), row=1, col=1)
fig.update_xaxes(title_text="Match", row=1, col=1)
fig.update_yaxes(title_text="Rating", row=1, col=1)

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
    ]),
    html.Div([
        dcc.Graph(
                id='rating-graphs',
                figure=fig
            )])
])

@callback(
    Output('player-ratings', 'data'),
    [Input('demo-dropdown', 'value')]
)

def update_table(value):
    filtered_data = df_scaled[df_scaled["name"] == value][['name', 'rating', 'match']].to_dict('records')
    return filtered_data

@callback(
    Output('rating-graphs', 'figure'),
    Input('demo-dropdown', 'value'), prevent_initial_call=True, allow_duplicates=True, suppress_callback_exceptions=True
)

def update_graph(value):

    df_scaled_filtered = df_scaled[df_scaled['name']== value]
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Scatter(y=df_scaled_filtered['rating']), row=1, col=1)
    fig.update_xaxes(title_text="Match", row=1, col=1)
    fig.update_yaxes(title_text="Rating", row=1, col=1)


    return fig