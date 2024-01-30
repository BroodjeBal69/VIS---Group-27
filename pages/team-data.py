import dash
from dash import html, dcc, Input, Output, callback, Dash, dash_table
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os

df_team_data = pd.read_csv('../Data/FIFA World Cup 2022 Team Data/team_data.csv', delimiter=',')
df_player_stats = pd.read_csv('../Data/FIFA World Cup 2022 Player Data/player_stats.csv', delimiter=',')
df_team_group_stats = pd.read_csv('../Data/FIFA World Cup 2022 Team Data/group_stats.csv', delimiter=',')
df_players_team = df_player_stats[df_player_stats["team"]=='Argentina']
df_players = df_players_team[['player', 'position', 'games', 'goals', 'assists']]
df_team_rating = pd.read_csv('df_rating_team.csv')

df_team_rating_scaled = df_team_rating[df_team_rating['name'] == 'Argentina']
team_lst = list(df_team_data["team"].unique())
team_lst.insert(0, "~")

colors = {
    'background': '#0E1B2A',
    'text': '#FFFFFF',
    'dropdown' : '#000000'
}

filtered_data = df_player_stats[df_player_stats["team"] == 'Argentina'][['player', 'position', 'games', 'goals', 'assists']]
filtered_goals = filtered_data.sort_values('goals', ascending=False).head(5)
filtered_assists = filtered_data.sort_values('assists', ascending=False).head(5)
fig = make_subplots(rows=2, cols=2,  specs=[[{}, {}],
            [{"colspan": 2}, None]], subplot_titles=('Topscorers', "Most assists"))
fig.add_trace(row=1, col=1,
        trace=go.Bar(x=filtered_goals['player'], y=filtered_goals['goals'])
        )
fig.add_trace(row=1, col=2,
        trace=go.Bar(x=filtered_assists['player'], y=filtered_assists['assists'])
        )
fig.add_trace(row=2, col=1,
        trace=go.Scatter(y=df_team_rating_scaled['rating_team'])
        )
fig.update_yaxes(title_text="Goals", row=1, col=1)
fig.update_yaxes(title_text="Assists", row=1, col=2)
fig.update_xaxes(title_text="Match", row=1, col=1)
fig.update_yaxes(title_text="Rating", row=2, col=1)


dash.register_page(__name__,
                   path='/team-data',
                    title='Teams',
                    name='Teams')

layout = html.Div([
    html.H1('Team data'),
    html.Div('Select team:'),
    html.Div([
            dcc.Dropdown(df_team_data["team"].unique(), "Argentina", id='demo-dropdown', searchable=True, style = {'color' : colors['dropdown']})
        ]),
    html.Div([
            dash_table.DataTable(
       id='player-table',
       columns=[{"name": i, "id": i} for i in df_player_stats[['player', 'position', 'games', 'goals', 'assists']].columns],
        data=df_player_stats[df_player_stats["team"] == "Argentina"][['player', 'position', 'games', 'goals', 'assists']].to_dict('records'),
        editable=True
   ),
   html.Div('Select team to compare(purple line):'),
    html.Div([
        dcc.Dropdown(team_lst, value="~", id='team-data-new-dropdown', searchable=True, style = {'color' : colors['dropdown']})
    ]),
    ]),
    html.Div([
            dcc.Graph(
                id='sub-graphs',
                figure=fig
            )
        ])
])

@callback(
    Output('player-table', 'data'),
    [Input('demo-dropdown', 'value')]
)
def update_table(value):
    filtered_data = df_player_stats[df_player_stats["team"] == value][['player', 'position', 'games', 'goals', 'assists']]
    return filtered_data.to_dict('records')

@callback(
    Output('sub-graphs', 'figure'),
    Input('demo-dropdown', 'value'),
     Input('team-data-new-dropdown', 'value'), prevent_initial_call=True, allow_duplicates=True, suppress_callback_exceptions=True
)
def update_graph(first_team, second_team):

    filtered_data = df_player_stats[df_player_stats["team"] == first_team][['player', 'position', 'games', 'goals', 'assists']]
    filtered_goals = filtered_data.sort_values('goals', ascending=False).head(5)
    filtered_assists = filtered_data.sort_values('assists', ascending=False).head(5)
    df_team_rating_scaled = df_team_rating[df_team_rating['name'] == first_team]
    fig = make_subplots(rows=2, cols=2, specs=[[{}, {}],
            [{"colspan": 2}, None]], subplot_titles=('Topscorers', "Most assists"))
    fig.add_trace(row=1, col=1,
        trace=go.Bar(x=filtered_goals['player'], y=filtered_goals['goals'])
        )
    fig.add_trace(row=1, col=2,
        trace=go.Bar(x=filtered_assists['player'], y=filtered_assists['assists'])
        )
    fig.add_trace(row=2, col=1,
        trace=go.Scatter(y=df_team_rating_scaled['rating_team'])
        )
    if second_team != "~":
        df_team_rating_scaled2 = df_team_rating[df_team_rating['name'] == second_team]
        fig.add_trace(row=2, col=1, trace=go.Scatter(y=df_team_rating_scaled2['rating_team']))

    fig.update_yaxes(title_text="Goals", row=1, col=1)
    fig.update_yaxes(title_text="Assists", row=1, col=2)
    fig.update_xaxes(title_text="Match", row=1, col=1)
    fig.update_yaxes(title_text="Rating", row=2, col=1)


    return fig