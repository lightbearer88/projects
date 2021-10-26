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

import matplotlib.pyplot as plt


excel_file = pd.ExcelFile(r"C:\Users\Ian's\Desktop\Postdoc\Micronet\51_deg_trials.xlsx")

dfs = {sheet_name: excel_file.parse(sheet_name, usecols=[0,1,2,3],
                         names=['R', 'C', 'angle', 'predict'])
       for sheet_name in excel_file.sheet_names}

sheet_keys = [keys for keys in dfs]

print(dfs['Trial_2'].head(2))

app = dash.Dash(__name__)

# app.layout = html.Div([
#     html.H6("Change the value in the text box to see callbacks in action!"),
#     html.Div([
#         "Input: ",
#         dcc.Input(id='my-input', value='initial value', type='text')
#     ]),
#     html.Br(),
#     html.Div(id='my-output'),

# ])

# @app.callback(
#     Output('graph-with-slider', 'figure'),
#     Input('year-slider', 'value'))

# def somefun():
    
#     return 0



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
                
                html.Div(children=dcc.Graph(id='graph_1'))
                
                ])

@app.callback(
    Output('graph_1', 'figure'),
    [Input('item_1', 'value'),Input('item_2', 'value')]
    )

def update_figure(select_1, select_2):
    filtered_df_1 = dfs[select_1]
    filtered_df_2 = dfs[select_2]
    
    fig = plt.plot(filtered_df_1)
    
    
    return 0


if __name__ == '__main__':
    app.run_server(debug=False)

