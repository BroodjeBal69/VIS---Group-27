import dash
from dash import html, dcc, Input, Output, callback, Dash, dash_table
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import re

df_match_data = pd.read_csv('../Data/FIFA World Cup 2022 Match Data/data.csv', delimiter=',')
df_match_data_cleaned = df_match_data[['match', 'match_time', 'home_team', 'away_team', 'score', 'attendance', 'venue', 'referee', 'home_formation', 'away_formation']]
df_match_data_cleaned[['score_home', 'score_away']] = df_match_data_cleaned.score.str.split("–", expand=True,)
df_match_data_cleaned.loc[:48, 'Stage'] = 'Group stage'
df_match_data_cleaned.loc[48:56, 'Stage'] = 'Round of 8'
df_match_data_cleaned.loc[56:60, 'Stage'] = 'Quarter finals'
df_match_data_cleaned.loc[60:62, 'Stage'] = 'Semi finals'
df_match_data_cleaned.loc[62:, 'Stage'] = 'Finals'
column = ['match_time', 'home_team', 'away_team', 'score_home', 'score_away', 'attendance', 'venue', 'referee', 'home_formation', 'away_formation']

import matplotlib.pyplot as plt
from matplotlib.patches import Arc

def createPitch():
       
    #Create figure
    fig=plt.figure()
    ax=fig.add_subplot(1,1,1)

    #Pitch Outline & Centre Line
    plt.plot([0,0],[0,90], color="black")
    plt.plot([0,130],[90,90], color="black")
    plt.plot([130,130],[90,0], color="black")
    plt.plot([130,0],[0,0], color="black")
    plt.plot([65,65],[0,90], color="black")
    
    #Left Penalty Area
    plt.plot([16.5,16.5],[65,25],color="black")
    plt.plot([0,16.5],[65,65],color="black")
    plt.plot([16.5,0],[25,25],color="black")
    
    #Right Penalty Area
    plt.plot([130,113.5],[65,65],color="black")
    plt.plot([113.5,113.5],[65,25],color="black")
    plt.plot([113.5,130],[25,25],color="black")
    
    #Left 6-yard Box
    plt.plot([0,5.5],[54,54],color="black")
    plt.plot([5.5,5.5],[54,36],color="black")
    plt.plot([5.5,0.5],[36,36],color="black")
    
    #Right 6-yard Box
    plt.plot([130,124.5],[54,54],color="black")
    plt.plot([124.5,124.5],[54,36],color="black")
    plt.plot([124.5,130],[36,36],color="black")
    #FourFourTwo()
    
    #Prepare Circles
    centreCircle = plt.Circle((65,45),9.15,color="black",fill=False)
    centreSpot = plt.Circle((65,45),0.8,color="black")
    leftPenSpot = plt.Circle((11,45),0.8,color="black")
    rightPenSpot = plt.Circle((119,45),0.8,color="black")
    
    #Draw Circles
    ax.add_patch(centreCircle)
    ax.add_patch(centreSpot)
    ax.add_patch(leftPenSpot)
    ax.add_patch(rightPenSpot)
    
    #Prepare Arcs
    leftArc = Arc((11,45),height=18.3,width=18.3,angle=0,theta1=310,theta2=50,color="black")
    rightArc = Arc((119,45),height=18.3,width=18.3,angle=0,theta1=130,theta2=230,color="black")

    #Draw Arcs
    ax.add_patch(leftArc)
    ax.add_patch(rightArc)
    
    #Tidy Axes
    plt.axis('off')
    
    #Display Pitch
    plt.show()

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

# (Your existing code)

# Modify your layout to include an empty Div for the pitch image
layout = html.Div([
    html.H1('Match data'),
    html.Div('Select World Cup stage:'),
    html.Div([
        dcc.Dropdown(
            options=[{'label': stage, 'value': stage} for stage in df_match_data_cleaned["Stage"].unique()],
            value='Group stage',
            id='demo-dropdown',
            searchable=True,
            style={'color': colors['dropdown']}
        )
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
        # Empty Div to hold the generated pitch image
        html.Div(id='pitch-image')
    ]),
])

# Add a callback to update the pitch image
@callback(
    [Output('match-table', 'data'), Output('sub-plots', 'figure'), Output('pitch-image', 'children')],
    [Input('demo-dropdown', 'value')]
)
def update_data_and_plots(value):
    filtered_data = df_match_data_cleaned[df_match_data_cleaned["Stage"] == value][column]

    # Update the data in the match table
    updated_table_data = filtered_data.to_dict('records')

    # Update the sub-plots figure
    for index, row in filtered_data.iterrows():
        filtered_data.loc[index, 'score_home'] = int(re.sub("\(.*?\)", "", str(filtered_data.loc[index, 'score_home'])))
        filtered_data.loc[index, 'score_away'] = int(re.sub("\(.*?\)", "", str(filtered_data.loc[index, 'score_away'])))
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

    # Generate the pitch image using createPitch function
    pitch_image = createPitch()
    pitch = dcc.Graph(
        id='pitch',
        figure=go.Figure(pitch_image)
    )

    return updated_table_data, fig, pitch



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
