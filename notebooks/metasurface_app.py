# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 16:09:00 2021

@author: Ian's
"""

import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px
import plotly.io as pio

pio.renderers.default="browser"

excel_file = pd.ExcelFile(r"C:\Users\Ian's\Desktop\Postdoc\Micronet\51_deg_trials.xlsx")

dfs = {sheet_name: excel_file.parse(sheet_name, usecols=[0,1,2,3],
                         names=['R', 'C', 'angle', 'predict'])
       for sheet_name in excel_file.sheet_names}

sheet_keys = [keys for keys in dfs]

cells = list(range(1,31))

df_cells = pd.DataFrame({"cells" : cells})

#print(df_cells)

#print(dfs['Trial_2'].head(2))


# filtered_df_1 = dfs['AF']
# df_1_R = (filtered_df_1["R"].dropna()).to_frame().rename(columns={"R": "R1"})
# df_1_C = filtered_df_1["C"].dropna().to_frame().rename(columns={"C": "C1"})

# filtered_df_2 = dfs['Trial_2']
# df_2_R = (filtered_df_2["R"].dropna()).to_frame().rename(columns={"R": "R2"})
# df_2_C = filtered_df_2["C"].dropna().to_frame().rename(columns={"C": "C2"})

# frames_R = [df_cells, df_1_R, df_2_R]

# df_total_R = pd.concat(frames_R, axis=1)

# #print(df_total_R)

# fig = px.line(df_total_R, x="cells", y=["R1","R2"])
# fig.show()



# block this out to test regular plotting
app = dash.Dash(__name__)


app.layout = html.Div(
    children = [html.Div(children=[dcc.Dropdown(id = 'item_1', 
                                                options=[{"label": trial_list, "value": trial_list}
                                                          for trial_list in sheet_keys],
                                                value = 'AF')],
                          style={'width': '48%', 'display':'inline-block'}),
                
                html.Div(children=[dcc.Dropdown(id = 'item_2', 
                                                options=[{"label": trial_list, "value": trial_list}
                                                          for trial_list in sheet_keys],
                                                value = 'Trial_2')],
                          style={'width': '48%', 'float': 'right', 'display':'inline-block'}),
                
                html.Div(children=dcc.Graph(id='graph_1')),
                html.Div(children=dcc.Graph(id='graph_2'))
                
                ])

@app.callback(
    Output('graph_1', 'figure'),
    Output('graph_2', 'figure'),
    [Input('item_1', 'value'),Input('item_2', 'value')]
    )

def update_figure(select_1, select_2):
    
    nameR_1 = "R_{}".format(select_1)
    nameR_2 = "R_{}".format(select_2)
    nameC_1 = "C_{}".format(select_1)
    nameC_2 = "C_{}".format(select_2)
    
    filtered_df_1 = dfs[select_1]
    df_1_R = (filtered_df_1["R"].dropna()).to_frame().rename(columns={"R": nameR_1})
    df_1_C = filtered_df_1["C"].dropna().to_frame().rename(columns={"C": nameC_1})

    filtered_df_2 = dfs[select_2]
    df_2_R = (filtered_df_2["R"].dropna()).to_frame().rename(columns={"R": nameR_2})
    df_2_C = filtered_df_2["C"].dropna().to_frame().rename(columns={"C": nameC_2})

    frames_R = [df_cells, df_1_R, df_2_R]
    frames_C = [df_cells, df_1_C, df_2_C]

    df_total_R = pd.concat(frames_R, axis=1)
    df_total_C = pd.concat(frames_C, axis=1)

    figR = px.line(df_total_R, x="cells", y=[nameR_1,nameR_2], labels={"value": "Resistance"})
    figC = px.line(df_total_C, x="cells", y=[nameC_1,nameC_2], labels={"value": "Capacitance"})
    
    
    return figR,figC


if __name__ == '__main__':
    app.run_server(debug=False)

