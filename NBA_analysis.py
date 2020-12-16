import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns],style={'textAlign': 'left'})),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ],style={'textAlign': 'left'}) for i in range(min(len(dataframe), max_rows))
        ])
    ])

all_datas = pd.read_csv('./all_players.csv',sep=',',encoding='gbk')
all_datas = all_datas.dropna(subset=["Player"])

all_types = list()
for item in all_datas.columns.tolist()[5:]:
    item_dict = {
        'label': item,
        'value': item
    }
    all_types.append(item_dict)

all_ages = [{'label': str(i), 'value': str(i)} for i in range(18,45)]
all_ages.insert(0,{'label': 'all', 'value': 'all'})

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
    html.H1('NBA Players Age Factor Analysis', style={'textAlign': 'center'}),
    html.Br(),

    html.Div(style={'width': '10%', 'display': 'inline-block'}),    # 改width可以改变Team的位置
    html.Div(["Team: ", dcc.Dropdown(options=all_teams,
                                    id='team',
                                    value=all_datas.loc[0,'Team']),
              ],
             style={'width': '20%', 'display': 'inline-block'}         # 改width可以改变长度
             ),

    html.Div(style={'width': '10%', 'display': 'inline-block'}),
    html.Div(["Attribute: ", dcc.Dropdown(options=all_types,
                                    id='attribute',
                                    value='Minutes played per game'),
              ],
             style={'width': '20%', 'display': 'inline-block'}
             ),

    html.Div(style={'width': '10%', 'display': 'inline-block'}),
    html.Div(["Age: ", dcc.Dropdown(options=all_ages,
                                    id='age',
                                    value='all'),
                   ],
                   style={'width': '20%', 'display': 'inline-block'}
                   ),

    html.Div([
        # html.Div(style={'width': '2%', 'display': 'inline-block'}),
        html.Br(),
        html.Br(),
        html.Div(id='logo', style={'width': '25%', 'display': 'inline-block'}),
        # html.H1('Logo', style={'width': '50%',}),
        # html.Hr(style={'width': '25%', 'display': 'inline-block'}),
        html.Div(id='teams_table',style={'width': '50%', 'display': 'inline-block'}),
        html.Br(),
        html.Br(),
        # html.Hr(style={'width': '25%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='teams_fig')],style={'width': '100%', 'height': '50%', 'display': 'inline-block', 'align':'center'})
    ])
])


@app.callback(
    Output(component_id='teams_fig', component_property='figure'),
    [Input(component_id='team', component_property='value'),
     Input(component_id='attribute', component_property='value')]
)
def update_output_div(team, attribute):
    df = all_datas[all_datas['Team']==team]
    df[attribute] = df[attribute].astype('float')
    df['Age'] = df['Age'].astype('int')
    all_age_dur = []
    all_attribute = []
    for every_age in all_ages[2:]:
        all_age_dur.append(int(every_age['value']))
        new_df = df[df['Age']==int(every_age['value'])]
        if new_df.shape[0]:
            all_attribute.append(new_df[attribute].sum() / new_df[attribute].count())
        else:
            all_attribute.append(0)
    fig = px.bar(x=all_age_dur, y=all_attribute, barmode="group")
    fig.update_layout(title="{} by Age".format(attribute),
                      xaxis_title="Age",
                      yaxis_title=attribute,
                      font=dict(
                          family="Courier New, monospace",
                          size=18,
                          color="RebeccaPurple")
                      )
    return fig

@app.callback(
    Output(component_id='teams_table', component_property='children'),
    [Input(component_id='team', component_property='value'),
     Input(component_id='attribute', component_property='value'),
     Input(component_id='age', component_property='value')]
)
def update_output_div1(team, attribute, age):
    if age != 'all':
        age = int(age)
    all_view_columns = all_datas.columns[0:5].tolist()
    all_view_columns.append(attribute)
    false_df = all_datas[all_view_columns]
    false_df = false_df.sort_values(by=attribute, ascending=False)
    false_df = false_df[all_datas['Team'] == team]
    if not age:
        return
        # return generate_table(false_df, max_rows=0)
    df = all_datas[all_datas['Team'] == team]
    view_columns = df.columns[0:5].tolist()
    view_columns.append(attribute)
    df = df[view_columns]
    df.drop(['Rk'],axis=1,inplace=True)
    if age == 'all':
        return generate_table(df, max_rows=df.shape[0])
    df['Age'] = df['Age'].astype('int')
    df = df[df['Age'] == age]
    if not df.shape[0]:
        return
    return  generate_table(df, max_rows=df.shape[0])

@app.callback(
    Output(component_id='logo', component_property='children'),
    [Input(component_id='team', component_property='value')]
)
def update_output_div2(team):
    img = html.Img(src="./team_logo/{}.png".format(team), style={'display': 'inline-block'})       
    #return img          # 队徽显示不出来

if __name__ == '__main__':
    app.run_server(debug=True)

