import dash
from dash import html, dcc, Input, Output, callback, Dash, dash_table
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import re
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc
import plotly.tools as tls
import io
import base64


import plotly.graph_objects as go

def create_pitch():
    fig = go.Figure()

    # Add pitch boundaries
    fig.add_shape(type='rect', x0=0, y0=0, x1=130, y1=90, line=dict(color='black', width=2))

    # Add penalty areas
    fig.add_shape(type='rect', x0=0, y0=25, x1=16.5, y1=65, line=dict(color='black', width=2))
    fig.add_shape(type='rect', x0=113.5, y0=25, x1=130, y1=65, line=dict(color='black', width=2))

    # Add goal areas
    fig.add_shape(type='rect', x0=0, y0=36, x1=5.5, y1=54, line=dict(color='black', width=2))
    fig.add_shape(type='rect', x0=124.5, y0=36, x1=130, y1=54, line=dict(color='black', width=2))

    # Add centre circle
    fig.add_shape(type='circle', x0=65-9.15, y0=45-9.15, x1=65+9.15, y1=45+9.15, line=dict(color='black', width=2))

    # Add centre spot
    fig.add_trace(go.Scatter(x=[65], y=[45], mode='markers', marker=dict(color='black', size=5)))

    # Update layout
    fig.update_layout(
        xaxis=dict(range=[0, 130], visible=False),
        yaxis=dict(range=[0, 90], visible=False),
        plot_bgcolor='green',  # Change pitch color if needed
        showlegend=False
    )

    return fig


df_match_data = pd.read_csv('../Data/FIFA World Cup 2022 Match Data/data.csv', delimiter=',')
df_match_data_cleaned = df_match_data[['match', 'match_time', 'home_team', 'away_team', 'score', 'attendance', 'venue', 'referee', 'home_formation', 'away_formation']]
df_match_data_cleaned[['score_home', 'score_away']] = df_match_data_cleaned.score.str.split("–", expand=True,)
df_match_data_cleaned.loc[:48, 'Stage'] = 'Group stage'
df_match_data_cleaned.loc[48:56, 'Stage'] = 'Round of 8'
df_match_data_cleaned.loc[56:60, 'Stage'] = 'Quarter finals'
df_match_data_cleaned.loc[60:62, 'Stage'] = 'Semi finals'
df_match_data_cleaned.loc[62:, 'Stage'] = 'Finals'
column = ['match_time', 'home_team', 'away_team', 'score_home', 'score_away', 'attendance', 'venue', 'referee', 'home_formation', 'away_formation']


colors = {
    'background': '#0E1B2A',
    'text': '#FFFFFF',
    'dropdown' : '#000000'
}

filtered_data = df_match_data_cleaned[df_match_data_cleaned["Stage"] == 'Group stage'][column]
for index, row in filtered_data.iterrows():
    filtered_data.loc[index, 'score_home'] = int(re.sub("\(.*?\)","",str(filtered_data.loc[index, 'score_home'])))
    filtered_data.loc[index, 'score_away'] = int(re.sub("\(.*?\)","",str(filtered_data.loc[index, 'score_away'])))
avg_home = filtered_data['score_home'].mean()
avg_away = filtered_data['score_away'].mean()
fig = make_subplots(rows=1, cols=2, subplot_titles=('Average goals', "Average attendance"))
fig.add_trace(row=1, col=1,
        trace=go.Bar(x=['Home', 'Away'], y=[avg_home, avg_away], width=0.42)
        )
fig.add_trace(row=1, col=2,
        trace=go.Bar(x=filtered_data['venue'], y=filtered_data['attendance'], width=0.42)
        )
fig.update_yaxes(title_text="Goals", row=1, col=1)
fig.update_yaxes(title_text="Attendance", row=1, col=2)


dash.register_page(__name__,
                   path='/matchdata',
                    title='World cup matches',
                    name='World cup matches')

layout = html.Div([
    html.H1('Match data'),
    html.Div('Select World Cup stage:'),
    html.Div([
            dcc.Dropdown(df_match_data_cleaned["Stage"].unique(), "Group stage", id='demo-dropdown', searchable=True, style = {'color' : colors['dropdown']})
        ]),
    html.Div([
            dash_table.DataTable(
       id='match-table',
       columns=[{"name": i, "id": i} for i in df_match_data_cleaned[column].columns],
        data=df_match_data_cleaned[df_match_data_cleaned["Stage"] == "Group stage"][column].to_dict('records'),
        editable=True
   ),
   html.Div([
            dcc.Graph(
                id='sub-plots',
                figure=fig
            )
        ]),
    html.Div([
    html.H1('Formation'),
    dcc.Graph(figure=create_pitch())
        ])
    ]),
])


@callback(
    Output('match-table', 'data'),
    [Input('demo-dropdown', 'value')]
)
def update_table(value):
    filtered_data = df_match_data_cleaned[df_match_data_cleaned["Stage"] == value][column]
    return filtered_data.to_dict('records')

@callback(
    Output('sub-plots', 'figure'),
    Input('demo-dropdown', 'value'), prevent_initial_call=True, allow_duplicates=True
)
def update_graph(value):

    filtered_data = df_match_data_cleaned[df_match_data_cleaned["Stage"] == value][column]
    for index, row in filtered_data.iterrows():
        filtered_data.loc[index, 'score_home'] = int(re.sub("\(.*?\)","",str(filtered_data.loc[index, 'score_home'])))
        filtered_data.loc[index, 'score_away'] = int(re.sub("\(.*?\)","",str(filtered_data.loc[index, 'score_away'])))
    avg_home = filtered_data['score_home'].mean()
    avg_away = filtered_data['score_away'].mean()
    fig = make_subplots(rows=1, cols=2, subplot_titles=('Average goals', "Average attendance"))
    fig.add_trace(row=1, col=1,
        trace=go.Bar(x=['Home', 'Away'], y=[avg_home, avg_away], width=0.42)
        )
    fig.add_trace(row=1, col=2,
        trace=go.Bar(x=filtered_data['venue'], y=filtered_data['attendance'], width=0.42)
        )
    fig.update_yaxes(title_text="Goals", row=1, col=1)
    fig.update_yaxes(title_text="Attendance", row=1, col=2)


    return fig

