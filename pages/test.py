# import dash
# from dash import html, dcc, Input, Output, callback, Dash, dash_table
# import pandas as pd
# from plotly.subplots import make_subplots
# import plotly.graph_objects as go
# import re
# import matplotlib.pyplot as plt
# import numpy as np
# from matplotlib.patches import Arc
# import plotly.tools as tls
# import io
# import base64
# import dash_bootstrap_components as dbc


# fig2 = go.Figure()

# # Add pitch boundaries
# fig2.add_shape(type='rect', x0=0, y0=0, x1=130, y1=90, line=dict(color='black', width=2))

# # Add penalty areas
# fig2.add_shape(type='rect', x0=0, y0=25, x1=16.5, y1=65, line=dict(color='black', width=2))
# fig2.add_shape(type='rect', x0=113.5, y0=25, x1=130, y1=65, line=dict(color='black', width=2))

# # Add goal areas
# fig2.add_shape(type='rect', x0=0, y0=36, x1=5.5, y1=54, line=dict(color='black', width=2))
# fig2.add_shape(type='rect', x0=124.5, y0=36, x1=130, y1=54, line=dict(color='black', width=2))

# # Add centre circle
# fig2.add_shape(type='circle', x0=65-9.15, y0=45-9.15, x1=65+9.15, y1=45+9.15, line=dict(color='black', width=2))

# # Add centre spot
# fig2.add_trace(go.Scatter(x=[65], y=[45], mode='markers', marker=dict(color='black', size=5)))

# # # Player positions for 5-3-2 formation (home team)
# # home_positions = [(7, 45), (25, 45), (25, 25), (25, 5), (25, 65), (25, 85),
# #                       (43, 45), (43, 15), (43, 75), (61, 20), (61, 70)]

# # # Player positions for 4-3-3 formation (away team)
# # away_positions = away_positions = [(130 - x, y) for x, y in [(7, 45), (25, 30), (25, 5), (25, 60), (25, 85), (43, 45), (43, 15), (43, 75), (61, 45), (61, 75), (61, 15)]]


# # # Add players for the home team
# # for position in home_positions:
# #     fig2.add_trace(go.Scatter(x=[position[0]], y=[position[1]], mode='markers', marker=dict(color='red', size=10)))

# # # Add players for the away team
# # for position in away_positions:
# #     fig2.add_trace(go.Scatter(x=[position[0]], y=[position[1]], mode='markers', marker=dict(color='blue', size=10)))

# # Update layout
# fig2.update_layout(
#     xaxis=dict(range=[0, 130], visible=False),
#     yaxis=dict(range=[0, 90], visible=False),
#     plot_bgcolor='green',  # Change pitch color if needed
#     showlegend=False
# )

# df_match_data = pd.read_csv('../Data/FIFA World Cup 2022 Match Data/data.csv', delimiter=',')
# df_match_data_cleaned = df_match_data[['match', 'match_time', 'home_team', 'away_team', 'score', 'attendance', 'venue', 'referee', 'home_formation', 'away_formation', 'home_sot', 'away_sot', 'home_clearances', 'away_clearances']]
# df_match_data_cleaned[['score_home', 'score_away']] = df_match_data_cleaned.score.str.split("–", expand=True,)
# df_match_data_cleaned.loc[:48, 'Stage'] = 'Group stage'
# df_match_data_cleaned.loc[48:56, 'Stage'] = 'Round of 8'
# df_match_data_cleaned.loc[56:60, 'Stage'] = 'Quarter finals'
# df_match_data_cleaned.loc[60:62, 'Stage'] = 'Semi finals'
# df_match_data_cleaned.loc[62:, 'Stage'] = 'Finals'
# column = ['match_time', 'home_team', 'away_team', 'score_home', 'score_away', 'attendance', 'venue', 'referee', 'home_formation', 'away_formation', 'home_sot', 'away_sot', 'home_clearances', 'away_clearances']

# colors = {
#     'background': '#0E1B2A',
#     'text': '#FFFFFF',
#     'dropdown' : '#000000'
# }


# dash.register_page(__name__,
#                    path='/test',
#                     title='Test',
#                     name='Test')

# layout = html.Div([
#     html.H1('Match data'),
#     html.Div('Select World Cup stage:'),
#     html.Div([
#             dcc.Dropdown(df_match_data_cleaned["Stage"].unique(), "Group stage", id='demo-dropdown', searchable=True, style = {'color' : colors['dropdown']})
#         ]),
#     html.Div([dash_table.DataTable(
#        id='match-table',
#        columns=[{"name": i, "id": i} for i in df_match_data_cleaned[column].columns],
#         data=df_match_data_cleaned[df_match_data_cleaned["Stage"] == "Group stage"][column].to_dict('records'),
#         editable=True      
#    )
#    ,]),
#     html.Div([
#     html.H1('Formation'),
#     dcc.Graph(figure=fig2, id='test-field-graph')
#         ])
#     ])

# # @callback(Output('tbl_out', 'children'), Input('match-table', 'active_cell'))
# # def update_graphs(active_cell):
# #     return str(active_cell) if active_cell else "Click the table"

# @callback(Output('test-field-graph', 'figure'), Input('match-table', 'active_cell'), prevent_initial_call=True, allow_duplicates=True, suppress_callback_exceptions=True)


# def create_pitch(active_cell):
#     fig2 = go.Figure()

#     # Add pitch boundaries
#     fig2.add_shape(type='rect', x0=0, y0=0, x1=130, y1=90, line=dict(color='black', width=2))

#     # Add penalty areas
#     fig2.add_shape(type='rect', x0=0, y0=25, x1=16.5, y1=65, line=dict(color='black', width=2))
#     fig2.add_shape(type='rect', x0=113.5, y0=25, x1=130, y1=65, line=dict(color='black', width=2))

#     # Add goal areas
#     fig2.add_shape(type='rect', x0=0, y0=36, x1=5.5, y1=54, line=dict(color='black', width=2))
#     fig2.add_shape(type='rect', x0=124.5, y0=36, x1=130, y1=54, line=dict(color='black', width=2))

#     # Add centre circle
#     fig2.add_shape(type='circle', x0=65-9.15, y0=45-9.15, x1=65+9.15, y1=45+9.15, line=dict(color='black', width=2))

#     # Add centre spot
#     fig2.add_trace(go.Scatter(x=[65], y=[45], mode='markers', marker=dict(color='black', size=5)))

#     home_form = df_match_data.loc[active_cell['row'],'home_formation']
#     away_form = df_match_data.loc[active_cell['row'],'away_formation']

#     # Player positions for 5-3-2 formation (home team)
#     five_three_two = [(7, 45), (25, 45), (25, 25), (25, 5), (25, 65), (25, 85),
#                       (43, 45), (43, 15), (43, 75), (61, 20), (61, 70)]

#     # Player positions for 4-3-3 formation (away team)
#     four_three_three = [(130 - x, y) for x, y in [(7, 45), (25, 30), (25, 5), (25, 60), (25, 85), (43, 45), (43, 15), (43, 75), (61, 45), (61, 75), (61, 15)]]

#     if home_form == '4-3-3':
#         home_posistions = four_three_three
#     else: 
#         away_positions = 0

#     if away_form == '4-3-3':
#         away_positions = four_three_three
#     else:
#         away_positions = 0
    

#     # Add players for the home team
#     for position in home_posistions:
#         fig2.add_trace(go.Scatter(x=[position[0]], y=[position[1]], mode='markers', marker=dict(color='red', size=10)))

#     # Add players for the away team
#     for position in away_positions:
#         fig2.add_trace(go.Scatter(x=[position[0]], y=[position[1]], mode='markers', marker=dict(color='blue', size=10)))

#     # Update layout
#     fig2.update_layout(
#         xaxis=dict(range=[0, 130], visible=False),
#         yaxis=dict(range=[0, 90], visible=False),
#         plot_bgcolor='green',  # Change pitch color if needed
#         showlegend=False
#     )

#     return fig2