import dash
from dash import html, dcc, Input, Output, callback, Dash, dash_table
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

df_player_defense       = pd.read_csv('../Data/FIFA World Cup 2022 Player Data/player_defense.csv', delimiter=',')
df_player_keepers       = pd.read_csv('../Data/FIFA World Cup 2022 Player Data/player_keepers.csv', delimiter=',')
df_player_passing       = pd.read_csv('../Data/FIFA World Cup 2022 Player Data/player_passing.csv', delimiter=',')
df_player_shooting      = pd.read_csv('../Data/FIFA World Cup 2022 Player Data/player_shooting.csv', delimiter=',')
df_player_stats         = pd.read_csv('../Data/FIFA World Cup 2022 Player Data/player_stats.csv', delimiter=',')

topscorers = df_player_stats.sort_values('goals', ascending=False).head(5)
pens_made = df_player_shooting.sort_values('pens_made', ascending=False).head(5)
topassists = df_player_stats.sort_values('assists', ascending=False).head(5)

most_passes = df_player_passing.sort_values('passes_completed', ascending=False).head(5)
most_minutes = df_player_stats.sort_values('minutes', ascending=False).head(5)
most_saves = df_player_keepers.sort_values('gk_saves', ascending=False).head(5)

most_clean_sheets = df_player_keepers.sort_values('gk_clean_sheets', ascending=False).head(5)
most_tackles = df_player_defense.sort_values('tackles', ascending=False).head(5)
most_blocks = df_player_defense.sort_values('blocks', ascending=False).head(5)

fig = make_subplots(rows=3, cols=3, subplot_titles=('Topscorers', 'Pens made', "Most assists", 'Most passes', 'Most minutes', 'Most saves', 'Most clean sheets',
                                                    'Most tackles', 'Most blocks'))
fig.add_trace(row=1, col=1,
    trace=go.Bar(x=topscorers['player'], y=topscorers['goals'], width=0.42)
    )
fig.add_trace(row=1, col=2,
    trace=go.Bar(x=pens_made['player'], y=pens_made['pens_made'], width=0.42)
    )
fig.add_trace(row=1, col=3,
    trace=go.Bar(x=topassists['player'], y=topassists['assists'], width=0.42)
    )

fig.add_trace(row=2, col=1,
    trace=go.Bar(x=most_passes['player'], y=most_passes['passes_completed'], width=0.42)
    )
fig.add_trace(row=2, col=2,
    trace=go.Bar(x=most_minutes['player'], y=most_minutes['minutes'], width=0.42)
    )
fig.add_trace(row=2, col=3,
    trace=go.Bar(x=most_saves['player'], y=most_saves['gk_saves'], width=0.42)
    )

fig.add_trace(row=3, col=1,
    trace=go.Bar(x=most_clean_sheets['player'], y=most_clean_sheets['gk_clean_sheets'], width=0.42)
    )
fig.add_trace(row=3, col=2,
    trace=go.Bar(x=most_tackles['player'], y=most_tackles['tackles'], width=0.42)
    )
fig.add_trace(row=3, col=3,
    trace=go.Bar(x=most_blocks['player'], y=most_blocks['blocks'], width=0.42)
    )

fig.update_yaxes(title_text="Goals", row=1, col=1)
fig.update_yaxes(title_text="Penalties scored", row=1, col=2)
fig.update_yaxes(title_text="Assists", row=1, col=3)
fig.update_yaxes(title_text="Passes completed", row=2, col=1)
fig.update_yaxes(title_text="Minutes played", row=2, col=2)
fig.update_yaxes(title_text="Saves", row=2, col=3)
fig.update_yaxes(title_text="Clean sheets", row=3, col=1)
fig.update_yaxes(title_text="Tackles", row=3, col=2)
fig.update_yaxes(title_text="Blocks", row=3, col=3)

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1('This is our Home page'),
    html.Div('Main statistics of the 2022 World Cup'),
    html.Div([dcc.Graph(figure=fig)])
])
    