import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

all_datas = pd.read_csv('./players.csv',sep=',',encoding='gbk')
all_datas = all_datas.dropna(subset=["Name"])

all_types = list()
for item in all_datas.drop_duplicates(subset=['Position'], keep='first', inplace=False)['Position']:
    item_dict = {
        'label': item,
        'value': item
    }
    all_types.append(item_dict)

all_ages = [
    {'label': '15-20', 'value': '15-20'},
    {'label': '20-25', 'value': '20-25'},
    {'label': '25-30', 'value': '25-30'},
    {'label': '30-35', 'value': '30-35'},
    {'label': '35-40', 'value': '35-40'}
]

all_teams = list()
for item in all_datas.drop_duplicates(subset=['Team'], keep='first', inplace=False)['Team']:
    item_dict = {
        'label': item,
        'value': item
    }
    all_teams.append(item_dict)

app = dash.Dash(__name__, external_stylesheets=stylesheet)
server = app.server

app.layout = html.Div([
    html.H1('NBA Salary Analyse', style={'textAlign': 'center'}),
    html.Br(),
    html.Div([
        html.Div(style={'width': '20%','display': 'inline-block'}),
        html.Div(["Position: ", dcc.Dropdown(options=all_types,
                                        id='position',
                                        value='SG'),
                  ],
                 style={'width': '40%', 'display': 'inline-block'}
                 ),
        html.Br(),
        html.Div([dcc.Graph(id='salary_fig')]),
    ],style={'width': '49%', 'display': 'inline-block', 'float': 'right',}),

    html.Div([
        html.Div(["Age: ", dcc.Dropdown(options=all_ages,
                                        id='age',
                                        value='15-20'),
                       ],
                       style={'width': '40%', 'display': 'inline-block'}
                       ),
        html.Div(style={'width': '20%', 'display':'inline-block'}),
        html.Div(["Team: ", dcc.Dropdown(options=all_teams,
                                        id='team',
                                        value=all_datas.loc[0,'Team']),
                  ],
                 style={'width': '40%', 'display': 'inline-block'}
                 ),
        html.Div([dcc.Graph(id='teams_fig')]),
    ],style={'width': '49%', 'display': 'inline-block', 'float': 'right',}),
])


@app.callback(
    Output(component_id='salary_fig', component_property='figure'),
    [Input(component_id='team', component_property='value'),
     Input(component_id='position', component_property='value')]
)
def update_output_div(team, position):
    df = all_datas[all_datas['Team']==team]
    df = df[df['Position']==position]
    df.replace('--','0',inplace=True)
    df.loc[:, 'Salary'] = df.loc[:, 'Salary'].str.replace('$', '')
    df.loc[:, 'Salary'] = df.loc[:, 'Salary'].str.replace(',', '')
    df['Salary'] = df['Salary'].astype('int')
    all_age_dur = list()
    all_salary = list()
    for item in all_ages:
        age_dur = item['value'].split('-')
        new_df = df[(df['Age']>=age_dur[0]) & (df['Age']<age_dur[1])]
        if new_df.shape[0]:
            all_age_dur.append(item['value'])
            all_salary.append(new_df['Salary'].sum() / new_df['Salary'].count())
        else:
            all_age_dur.append(item['value'])
            all_salary.append(0)
    fig = px.bar(x=all_age_dur, y=all_salary, barmode="group")
    fig.update_layout(title="Salary of age",
                      xaxis_title="Age",
                      yaxis_title="Salary",
                      font=dict(
                          family="Courier New, monospace",
                          size=18,
                          color="RebeccaPurple")
                      )
    return fig

@app.callback(
    Output(component_id='teams_fig', component_property='figure'),
    [Input(component_id='team', component_property='value'),
     Input(component_id='age', component_property='value')]
)
def update_output_div1(team, age):
    df = all_datas[all_datas['Team']==team]
    age_dur = age.split('-')
    df = df[(df['Age'] >= age_dur[0]) & (df['Age'] < age_dur[1])]
    df.replace('--','0',inplace=True)
    df.loc[:, 'Salary'] = df.loc[:, 'Salary'].str.replace('$', '')
    df.loc[:, 'Salary'] = df.loc[:, 'Salary'].str.replace(',', '')
    df['Salary'] = df['Salary'].astype('int')
    all_pos = list()
    all_value = list()
    for pos in all_types:
        new_df = df[df['Position']==pos['value']]
        if new_df.shape[0]:
            all_pos.append(pos['value'])
            all_value.append(new_df['Salary'].sum() / new_df['Salary'].count())
        else:
            all_pos.append(pos['value'])
            all_value.append(0)
    fig = px.bar(x=all_pos,
                 y=all_value, barmode="group")
    fig.update_layout(title="Salary of position",
                      xaxis_title="Position",
                      yaxis_title="Salary",
                      font=dict(
                          family="Courier New, monospace",
                          size=18,
                          color="RebeccaPurple")
                      )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
