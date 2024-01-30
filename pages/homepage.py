import dash
from dash import html, dcc, Input, Output, callback, Dash, dash_table
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import re

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

df_team_data        = pd.read_csv('../Data/FIFA World Cup 2022 Team Data/team_data.csv', delimiter=',')

df_match_data = pd.read_csv('../Data/FIFA World Cup 2022 Match Data/data.csv', delimiter=',')
df_match_data[['score_home', 'score_away']] = df_match_data.score.str.split("–", expand=True,)
for index, row in df_match_data.iterrows():
    df_match_data.loc[index, 'score_home'] = int(re.sub("\(.*?\)","",str(df_match_data.loc[index, 'score_home'])))
    df_match_data.loc[index, 'score_away'] = int(re.sub("\(.*?\)","",str(df_match_data.loc[index, 'score_away'])))
df_team_shots = df_match_data[["home_team", "home_saves", "away_sot"]]

fig = make_subplots(rows=5, cols=3, specs=[[{}, {}, {}], [{}, {}, {}], [{}, {}, {}],
           [{"colspan": 3}, None, None], [{"colspan": 3}, None, None]],
           subplot_titles=('Topscorers', 'Pens made', "Most assists", 'Most passes', 'Most minutes', 'Most saves', 'Most clean sheets',
                                                    'Most tackles', 'Most blocks', 'Shots saved v.s. Shots taken', 'Shots taken v.s. Goals'))
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

fig.add_trace(go.Scatter(x=df_team_data['gk_saves'], y=df_team_data['shots'], mode='markers', text=df_team_data['team']), row=4, col=1)

fig.add_trace(go.Scatter(x=df_team_data['goals'], y=df_team_data['shots'], mode='markers', text=df_team_data['team']), row=5, col=1)


fig.update_yaxes(title_text="Goals", row=1, col=1)
fig.update_yaxes(title_text="Penalties scored", row=1, col=2)
fig.update_yaxes(title_text="Assists", row=1, col=3)
fig.update_yaxes(title_text="Passes completed", row=2, col=1)
fig.update_yaxes(title_text="Minutes played", row=2, col=2)
fig.update_yaxes(title_text="Saves", row=2, col=3)
fig.update_yaxes(title_text="Clean sheets", row=3, col=1)
fig.update_yaxes(title_text="Tackles", row=3, col=2)
fig.update_yaxes(title_text="Blocks", row=3, col=3)
fig.update_xaxes(title_text='Shots saved', row=4, col=1)
fig.update_yaxes(title_text='Shots taken', row=4, col=1)
fig.update_xaxes(title_text='Goals', row=5, col=1)
fig.update_yaxes(title_text='Shots taken', row=5, col=1)

fig.update_layout(height=3500, width=2500)

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1('This is our Home page'),
    html.Div('Main statistics of the 2022 World Cup'),
    html.Div([dcc.Graph(figure=fig)])
])
    