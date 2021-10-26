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
import plotly.graph_objects as go

import matplotlib.pyplot as plt
import numpy as np

from io import BytesIO
import base64

def fig_to_uri(in_fig, close_all=True, **save_args):
    # type: (plt.Figure) -> str
    """
    Save a figure as a URI
    :param in_fig:
    :return:
    (from: https://github.com/4QuantOSS/DashIntro/blob/master/notebooks/Tutorial.ipynb)
    """
    out_img = BytesIO()
    in_fig.savefig(out_img, format='png', **save_args)
    if close_all:
        in_fig.clf()
        plt.close('all')
    out_img.seek(0)  # rewind file
    encoded = base64.b64encode(out_img.read()).decode("ascii").replace("\n", "")
    return "data:image/png;base64,{}".format(encoded)

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
# filtered_df_2 = dfs['Trial_2']

# df_1_ffp = filtered_df_1["predict"].to_frame().rename(columns={"predict": "dB_1"})
# df_2_ffp = filtered_df_2["predict"].to_frame().rename(columns={"predict": "dB_2"})
# df_1_angle = filtered_df_1["angle"].to_frame().rename(columns={"angle": "angle"})

# frames_ffp = [df_1_angle, df_1_ffp, df_2_ffp]
# df_total_ffp = pd.concat(frames_ffp, axis=1)

# print(df_total_ffp)

# fig_1, ax_1 = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(6,6))
# angle_deg = np.arange(-90,91,1)
# angle = [np.radians(a) for a in angle_deg]
# ax_1.set_xticks(np.pi/180. * np.linspace(-180, 180, 18, endpoint=False))
# ax_1.set_thetalim(-np.pi, np.pi)
# ax_1.plot(angle, df_total_ffp['dB_1'], label='dB1', ls="--")
# ax_1.plot(angle, df_total_ffp['dB_2'], label='dB2')
# angle_leg = np.deg2rad(67.5)
# ax_1.legend(loc="lower left",
#           bbox_to_anchor=(.5 + np.cos(angle_leg)/2, .5 + np.sin(angle_leg)/2))



# fig = go.Figure()

# fig.add_trace(go.Scatterpolar(r=df_total_ffp["dB_1"], theta=df_total_ffp["angle"], name='AF'))
# fig.add_trace(go.Scatterpolar(r=df_total_ffp["dB_2"], theta=df_total_ffp["angle"], name='Trial_2'))

# fig.show()

# fig = px.line_polar(df_total_ffp, r=["dB_1", "dB_2"], theta="angle", range_theta=[0,180])
# fig.show()

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
                
                html.Div(children=[html.Img(id='graph_ffp_polar', src='')], id='plot_div', style= {'height':'50%', 'width':'50%','textAlign':'center'}),
                html.Div(children=dcc.Graph(id='graph_1'), style={'width': '48%', 'display':'inline-block'}),
                html.Div(children=dcc.Graph(id='graph_2'),style={'width': '48%', 'float': 'right', 'display':'inline-block'})
                ], style={'textAlign':'center'})

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

@app.callback(
    Output('graph_ffp_polar', 'src'),
    [Input('item_1', 'value'),Input('item_2', 'value')]
    )
def update_ffp(select_1, select_2):
    
    filtered_df_1 = dfs[select_1]
    filtered_df_2 = dfs[select_2]

    df_1_ffp = filtered_df_1["predict"].to_frame().rename(columns={"predict": select_1})
    df_2_ffp = filtered_df_2["predict"].to_frame().rename(columns={"predict": select_2})
    df_1_angle = filtered_df_1["angle"].to_frame().rename(columns={"angle": "angle"})

    frames_ffp = [df_1_angle, df_1_ffp, df_2_ffp]
    df_total_ffp = pd.concat(frames_ffp, axis=1)

    fig_1, ax_1 = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(6,6))
    angle_deg = np.arange(-90,91,1)
    angle = [np.radians(a) for a in angle_deg]
    ax_1.set_xticks(np.pi/180. * np.linspace(-180, 180, 18, endpoint=False))
    ax_1.set_thetalim(-np.pi, np.pi)
    ax_1.plot(angle, df_total_ffp[select_1], label=select_1, ls="--")
    ax_1.plot(angle, df_total_ffp[select_2], label=select_2)
    angle_leg = np.deg2rad(67.5)
    ax_1.legend(loc="lower left",
          bbox_to_anchor=(.5 + np.cos(angle_leg)/2, .5 + np.sin(angle_leg)/2))
    
    out_url = fig_to_uri(fig_1)
    
    return out_url


if __name__ == '__main__':
    app.run_server(debug=False)

