# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 04:58:12 2022

@author: TEVIN
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 10:34:32 2022
@author: TEVIN
"""
#Import Dependancies
import dash_bootstrap_components as dbc
import dash
#Sfrom dash.dependencies import Input,Output
#import dash_daq as daq
from dash import dcc,html,dash_table
import plotly.express as px
#import redis
import pymongo
import pandas as pd
#import time
from datetime import timedelta
from dash.dependencies import Input, Output
#import plotly.graph_objects as go


################

client  = pymongo.MongoClient("mongodb+srv://toloo:Godocholoo@cluster0.idj1r.mongodb.net/test")
db = client["iotdatadb"]
col = db["iotwaterapi"]

data = col.find()
df = pd.DataFrame(data)

   ####################
   
#app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}]
)
server = app.server
########################
   
# Eliminating test records


########################

# Transformations
# 1FA1185
df1 = df.loc[(df['device'] == '1FA1185')] #  1FA1A01
df1['time'] = pd.to_datetime(df1['time'])
df1['time'] += timedelta(hours=3)

# df1['actual_level'] = 7000 - df1['Level']
df1['Level'] = round(df1['Level']* 1.4286 ,2)
df1['Event_type'] = df1['Messagetype'].apply(lambda x: 'Level Increase' if x == 47 else 'Level Decrease')
df1 = df1.sort_values(by = 'time',ascending = False)
df1['ΔVolume (Lts)'] = round(abs(df1['Level'] - df1['Level'].shift(-1)),2)
df1['sysdate'] =pd.to_datetime('today',format = "%Y-%m-%d %H:%M:%S",utc='true') ####################################################
df1['timediff'] = (df1['sysdate'] - df1['time']).astype('timedelta64[s]') ####################################################
df1 = df1[df1['timediff'] <= 259200] #3days###################################################
df1 = df1.rename(columns = {'_id':'Event_id','time':'Event_time (UTC+3)','Battery':'Battery_level (%)'
                          ,'Level':'Volume (Lts)'})
df1 = df1[[ 'Event_time (UTC+3)','Event_type','Volume (Lts)','ΔVolume (Lts)',]]


#getting aggrgates
maxlevinc = df1["ΔVolume (Lts)"].where(df1['Event_type'] == 'Level Increase').max()
maxinctime = df1["Event_time (UTC+3)"].where(df1['ΔVolume (Lts)'] == maxlevinc).max()
# maxinctime = maxinctime.strftime("%d-%b-%Y %H:%M:%S")
maxlevdec = df1["ΔVolume (Lts)"].where(df1['Event_type'] == 'Level Decrease').max()
maxdectime = df1["Event_time (UTC+3)"].where(df1['ΔVolume (Lts)'] == maxlevdec).max()
maxdectime = maxdectime.strftime("%d-%b-%Y %H:%M:%S")
# Currentvolume = df1.iloc[0,4]
# Currenttime = df1.iloc[0,2]
# Currenttime = Currenttime.strftime("%d-%b-%Y %H:%M:%S")

# 1FA1A01
df2 = df.loc[(df['device'] == '1FA1A01')] #  
df2['time'] = pd.to_datetime(df2['time'])
df2['time'] += timedelta(hours=3)
# df['actual_level'] = 7000 - df['Level']
df2['Level'] = round(df2['Level']* 1.4286 ,2)
df2['Event_type'] = df2['Messagetype'].apply(lambda x: 'Level Increase' if x == 47 else 'Level Decrease')
df2 = df2.sort_values(by = 'time',ascending = False)
df2['ΔVolume (Lts)'] = round(abs(df2['Level'] - df2['Level'].shift(-1)),2)
df2['sysdate'] =pd.to_datetime('today',format = "%Y-%m-%d %H:%M:%S",utc='true') ####################################################
df2['timediff'] = (df2['sysdate'] - df2['time']).astype('timedelta64[s]') ####################################################
df2 = df2[df2['timediff'] <= 259200] #3days###################################################
df2 = df2.rename(columns = {'_id':'Event_id','time':'Event_time (UTC+3)','Battery':'Battery_level (%)'
                          ,'Level':'Volume (Lts)'})
df2 = df2[[ 'Event_time (UTC+3)','Event_type','Volume (Lts)','ΔVolume (Lts)',]]

#getting aggrgates
maxlevincdf2 = df2["ΔVolume (Lts)"].where(df2['Event_type'] == 'Level Increase').max()
maxinctimedf2 = df2["Event_time (UTC+3)"].where(df2['ΔVolume (Lts)'] == maxlevincdf2).max()
maxinctimedf2 = maxinctimedf2.strftime("%d-%b-%Y %H:%M:%S")
maxlevdecdf2 = df2["ΔVolume (Lts)"].where(df2['Event_type'] == 'Level Decrease').max()
maxdectimedf2 = df2["Event_time (UTC+3)"].where(df2['ΔVolume (Lts)'] == maxlevdecdf2).max()
maxdectimedf2 = maxdectimedf2.strftime("%d-%b-%Y %H:%M:%S")
# Currentvolumedf2 = df2.iloc[0,4]
# Currenttimedf2 = df2.iloc[0,2]
# Currenttimedf2 = Currenttimedf2.strftime("%d-%b-%Y %H:%M:%S")

# visualizations

#plotting the trend graphs
#1FA1185 trend graph
fig1FA1185 = px.area(df1, x="Event_time (UTC+3)", y="Volume (Lts)",line_shape='spline',
                  title='Volume Trend',
                  labels={
                     "Event_time (UTC+3)": "Event_time (UTC+3)",
                     "Volume (Lts)": "Volume (Lts)"
                 }
                  , color_discrete_sequence=["#04AEC4"],height=325
                  )
fig1FA1185.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
'margin':{'l': 10, 'r': 10},
'font_color':"#ffffff",
'title_font_color':"#ffffff",
"title_font":{'size': 20},
})
fig1FA1185.update_xaxes(showgrid=True)
fig1FA1185.update_yaxes(showgrid=True)
fig1FA1185.layout.xaxis.fixedrange = True
fig1FA1185.layout.yaxis.fixedrange = True

#1FA1A01 trend graph
fig1FA1A01 = px.area(df2, x="Event_time (UTC+3)", y="Volume (Lts)",line_shape='spline',title='Volume Trend',
                 labels={
                    "Event_time (UTC+3)": "Event_time (UTC+3)",
                    "Volume (Lts)": "Volume (Lts)"
                }
                 , color_discrete_sequence=["#04AEC4"],height=325
                 )
fig1FA1A01.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
'margin':{'l': 10, 'r': 10},
'font_color':"#ffffff",
'title_font_color':"#ffffff",
"title_font":{'size': 20},
})
fig1FA1A01.update_xaxes(showgrid=True)
fig1FA1A01.update_yaxes(showgrid=True)
fig1FA1A01.layout.xaxis.fixedrange = True
fig1FA1A01.layout.yaxis.fixedrange = True

app.title = "Ultrasonic Water Level Sensor Analytics"
app.layout = dbc.Container(fluid=True,
                            children=[
    html.Div(
    [

     
     
      dbc.Card(
         dbc.Row(
             [
                html.P(),
                html.P(),  
      html.H4("Ultrasonic Water Level Sensor Analytics"
              ,style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)","text-align":"center","color":"#04AEC4",}
              ),
      ]
             ),style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)"},),
     
      dbc.Card(
         dbc.Row(
             [
                # html.P(),
                # html.P(),  
      html.H6("Sensor end-point provided by Silafrica SIMTANKH20 Solution"
              ,style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)","text-align":"center","color":"#04AEC4",}
              ),
      html.H6("Contact tevin9316@gmail.com for more information"
              ,style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)","text-align":"center","color":"#04AEC4",}
              ),
      html.P(),
      html.P(),
      ]
             ),style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)"},),
     
      #  html.H6("Contact tevin9316@gmail.com for more information"
               # ,style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)","text-align":"center","color":"#04AEC4",}
               # ),
     
     
     html.P(),
     #html.P(),

     dbc.Card(
        dbc.Row(
            [
##########
html.Hr(style={'borderWidth': "1.9vh", "width": "100%", "color": "#04AEC4"}),
#### Device-1FA1185
     html.P(),
    # html.P(),
html.H5("Device ID: 1FA1185 ;  Location ID: A009158"
        ,style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)","text-align":"center","color":"#04AEC4",}
        ),
####Current readings
dbc.Col(dbc.Card([
        dbc.CardHeader("Current Volume (liters)",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                            "text-align":"center","color":"#ffffff","font-weight":"bold",}),
        dbc.CardBody(
            [
                html.H4(id="load_currentvolume",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                                    "text-align":"center","color":"#04AEC4"}, className="card-title"),
                dcc.Interval(id='interval-currentvolume',interval=60*1000,n_intervals=0,)
               # html.P("This is some card text", className="card-text"),
            ]
        ),
        dbc.CardFooter(
            [
                html.H4("Latest Update: ",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                                    "text-align":"center","color":"#ffffff",'font-size': '16px',}, className="card-title"),
                html.H4(id="load_currenttime",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                                    "text-align":"center","color":"#ffffff",'font-size': '16px',}, className="card-title"),
                dcc.Interval(id='interval-currenttime',interval=60*1000,n_intervals=0,)
               # html.P("This is some card text", className="card-text"),
            ]  
        ),
    ],style = {"background-color":"rgba(0,0,0,0.0)","border-color":"#04AEC4",'height':'170px',},
   
    ),xs=12,sm=6,md=4,lg=4,xl=4,
    style = {"margin-top":"1%",}),

#### Highest volume increase readings

dbc.Col(dbc.Card([
        dbc.CardHeader("Highest Volume Increase (liters)",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                            "text-align":"center","color":"#ffffff","font-weight":"bold",}),
        dbc.CardBody(
            [
                html.H4(id="load_highestinc",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                                    "text-align":"center","color":"#04AEC4"}, className="card-title"),
                dcc.Interval(id='interval-highestinc',interval=60*1000,n_intervals=0,)
               # html.P("This is some card text", className="card-text"),
            ]
        ),
        dbc.CardFooter(
            [
                html.H4("Occurred at: ",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                                    "text-align":"center","color":"#ffffff",'font-size': '16px',}, className="card-title"),
                html.H4(id="load_highestinctime",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                                    "text-align":"center","color":"#ffffff",'font-size': '16px',}, className="card-title"),
                dcc.Interval(id='interval-highestinctime',interval=60*1000,n_intervals=0,)
               # html.P("This is some card text", className="card-text"),
            ]  
        ),
    ],style = {"background-color":"rgba(0,0,0,0.0)","border-color":"#04AEC4",'height':'170px',},
   
    ),xs=12,sm=6,md=4,lg=4,xl=4,
    style = {"margin-top":"1%",}),
     
#### Highest volume decrease readings    
dbc.Col(dbc.Card([
        dbc.CardHeader("Highest Volume Decrease (liters)",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                            "text-align":"center","color":"#ffffff","font-weight":"bold",}),
        dbc.CardBody(
            [
                html.H4(id="load_highestdec",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                                    "text-align":"center","color":"#04AEC4"}, className="card-title"),
                dcc.Interval(id='interval-highestdec',interval=60*1000,n_intervals=0,)
               # html.P("This is some card text", className="card-text"),
            ]
        ),
        dbc.CardFooter(
            [
                html.H4("Occurred at: ",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                                    "text-align":"center","color":"#ffffff",'font-size': '16px',}, className="card-title"),
                html.H4(id="load_highestdectime",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                                    "text-align":"center","color":"#ffffff",'font-size': '16px',}, className="card-title"),
                dcc.Interval(id='interval-highestdectime',interval=60*1000,n_intervals=0,)
               # html.P("This is some card text", className="card-text"),
            ]  
        ),
    ],style = {"background-color":"rgba(0,0,0,0.0)","border-color":"#04AEC4",'height':'170px',},
   
    ),xs=12,sm=6,md=4,lg=4,xl=4,
    style = {"margin-top":"1%",}),
       
 
            ],
            className="mb-4",
        ),
       
        style = {"background-color":"rgb(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)"}),
###############################################################rav ahuja    
     dbc.Card(
       
         dbc.Row(
            [
               
#########
html.P(),

       
dbc.Col(dbc.Card([dcc.Graph(id='load-1FA1185-graph',figure=fig1FA1185),dcc.Interval(id='interval-1FA1185-graph',interval=60*1000,n_intervals=0,) ],style = {"background-color":"rgba(0,0,0,0)","border-color":"rgba(0,0,0,0)",},
               
), xs=12,sm=12,md=12,lg=12,xl=12,
style = {"margin-top":"1%",}),
       
            ],
            className="mb-4"
        ),
         style = {"background-color":"rgb(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)"}),
     
     
         ######################################################
   dbc.Card(      
         dbc.Row(
            [
# #######
#html.P(),
dbc.Col(dbc.Card([
dash_table.DataTable(
                id='load-1FA1185-table',
                data=df1.to_dict('records'),
                #id="load_omni_trxns_dist_pie",
                style_cell={
                    'backgroundColor': 'rgba(0,0,0,0)',
                    'color': '#fff',
                    'border': '0.01px solid #04AEC4',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'width': 'auto',
                    'textOverflow': 'ellipsis',
                    'font-family': 'Verdana, Tahoma, sans-serif',
                    'font-size': '9px',
                    'text-align': 'center',
                    'overflow-y': 'auto',
                    'padding-left': '2%',
                    'pointer-events':'none',
                },
                style_table={
                    'overflowX': 'auto', 'margin-top': '2%', 'overflow-y': 'auto'},
                style_as_list_view=False,
                style_data_conditional=[ {

                                    "if": {"state": "selected"},

                                    "backgroundColor": "inherit !important",
                                    
                                    # "backgroundColor": "rgba(0,0,0,0.3)",

                                    "border": "0.01px solid #04AEC4",

                                        }

                                    ],
                style_header={
                    'backgroundColor': 'rgba(0,0,0,0)', 'font-size': '10px', 'color': '#04AEC4',
                    'text-align': 'center',
                    'border': '0.01px solid #04AEC4',
                    #'width': 'auto',
                    'font-weight':'bold',},
                sort_action='native',
                page_action='native',   # all data is passed to the table up-front
                page_size=6,
            ),dcc.Interval(id='interval-1FA1185-table',interval=60*1000,n_intervals=0,)],style = {"background-color":"rgba(0,0,0,0)","border-color":"rgba(0,0,0,0)",}
    ), xs=12,sm=12,md=12,lg=12,xl=12),

# dbc.Col(dcc.Graph(figure=figtemp), width=3)

           ],
            className="mb-4",
         ),
         
         style = {"background-color":"rgb(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)"}),
       
html.Hr(style={'borderWidth': "1.9vh", "width": "100%", "color": "#04AEC4"}),
        html.P(),
        html.P(),
        html.P(),
        html.P(),
     html.P(),
     html.P(),
# html.P('Device ID: 1FA1A01 ;  Location ID: A009263'),
html.H5("Device ID: 1FA1A01 ;  Location ID: A009263"
        ,style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)","text-align":"center","color":"#04AEC4",}
        ),
#### Device-1FA1A01

####Current readings
dbc.Card(
   dbc.Row(
       [

dbc.Col(dbc.Card([
        dbc.CardHeader("Current Volume (liters)",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                            "text-align":"center","color":"#ffffff","font-weight":"bold",}),
        dbc.CardBody(
            [
                html.H4(id="load_currentvolumedf2",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                                    "text-align":"center","color":"#04AEC4"}, className="card-title"),
                dcc.Interval(id='interval-currentvolumedf2',interval=60*1000,n_intervals=0,)
               # html.P("This is some card text", className="card-text"),
            ]
        ),
        dbc.CardFooter(
            [
                html.H4("Latest Update: ",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                                    "text-align":"center","color":"#ffffff",'font-size': '16px',}, className="card-title"),
                html.H4(id="load_currenttimedf2",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                                    "text-align":"center","color":"#ffffff",'font-size': '16px',}, className="card-title"),
                dcc.Interval(id='interval-currenttimedf2',interval=60*1000,n_intervals=0,)
               # html.P("This is some card text", className="card-text"),
            ]  
        ),
    ],style = {"background-color":"rgba(0,0,0,0.0)","border-color":"#04AEC4",'height':'170px',},
   
    ),xs=12,sm=6,md=4,lg=4,xl=4,
    style = {"margin-top":"1%",}),

#### Highest volume increase readings

dbc.Col(dbc.Card([
        dbc.CardHeader("Highest Volume Increase (liters)",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                            "text-align":"center","color":"#ffffff","font-weight":"bold",}),
        dbc.CardBody(
            [
                html.H4(id="load_highestincdf2",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                                    "text-align":"center","color":"#04AEC4"}, className="card-title"),
                dcc.Interval(id='interval-highestincdf2',interval=60*1000,n_intervals=0,)
               # html.P("This is some card text", className="card-text"),
            ]
        ),
        dbc.CardFooter(
            [
                html.H4("Occurred at: ",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                                    "text-align":"center","color":"#ffffff",'font-size': '16px',}, className="card-title"),
                html.H4(id="load_highestinctimedf2",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                                    "text-align":"center","color":"#ffffff",'font-size': '16px',}, className="card-title"),
                dcc.Interval(id='interval-highestinctimedf2',interval=60*1000,n_intervals=0,)
               # html.P("This is some card text", className="card-text"),
            ]  
        ),
    ],style = {"background-color":"rgba(0,0,0,0.0)","border-color":"#04AEC4",'height':'170px',},
   
    ),xs=12,sm=6,md=4,lg=4,xl=4,
    style = {"margin-top":"1%",}),
     
#### Highest volume decrease readings    
dbc.Col(dbc.Card([
        dbc.CardHeader("Highest Volume Decrease (liters)",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                            "text-align":"center","color":"#ffffff","font-weight":"bold",}),
        dbc.CardBody(
            [
                html.H4(id="load_highestdecdf2",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                                    "text-align":"center","color":"#04AEC4"}, className="card-title"),
                dcc.Interval(id='interval-highestdecdf2',interval=60*1000,n_intervals=0,)
               # html.P("This is some card text", className="card-text"),
            ]
        ),
        dbc.CardFooter(
            [
                html.H4("Occurred at: ",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                                    "text-align":"center","color":"#ffffff",'font-size': '16px',}, className="card-title"),
                html.H4(id="load_highestdectimedf2",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                                    "text-align":"center","color":"#ffffff",'font-size': '16px',}, className="card-title"),
                dcc.Interval(id='interval-highestdectimedf2',interval=60*1000,n_intervals=0,)
               # html.P("This is some card text", className="card-text"),
            ]  
        ),
    ],style = {"background-color":"rgba(0,0,0,0.0)","border-color":"#04AEC4",'height':'170px',},
   
    ),xs=12,sm=6,md=4,lg=4,xl=4,
    style = {"margin-top":"1%",}),
       
       


       
            ],
            className="mb-4",
        ),
 
       style = {"background-color":"rgb(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)"}),      
        ########################################################
       
       
        dbc.Row(
            [
#######
html.P(),
       
           
           
dbc.Col(dbc.Card([dcc.Graph(id='load-1FA1A01-graph',figure=fig1FA1A01),dcc.Interval(id='interval-1FA1A01-graph',interval=60*1000,n_intervals=0,) ],style = {"background-color":"rgba(0,0,0,0)","border-color":"rgba(0,0,0,0)",}
), xs=12,sm=12,md=12,lg=12,xl=12,
style = {"margin-top":"1%",}),
            ],
            className="mb-4",
        ),      
       
        ########################################################
       
         dbc.Row(
            [
# #######
#html.P(),
dbc.Col(dbc.Card([
dash_table.DataTable(
                id='load-1FA1A01-table',
                data=df2.to_dict('records'),
                #id="load_omni_trxns_dist_pie",
                style_cell={
                    'backgroundColor': 'rgba(0,0,0,0)',
                    'color': '#fff',
                    'border': '0.01px solid #04AEC4',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'width': 'auto',
                    'textOverflow': 'ellipsis',
                    'font-family': 'Verdana, Tahoma, sans-serif',
                    'font-size': '9px',
                    'text-align': 'center',
                    'overflow-y': 'auto',
                    'padding-left': '2%',
                    'pointer-events':'none',
                },
                style_table={
                    'overflowX': 'auto', 'margin-top': '2%', 'overflow-y': 'auto'},
                style_as_list_view=False,
                style_data_conditional=[ {

                                    "if": {"state": "selected"},

                                    "backgroundColor": "inherit !important",

                                    "border": "inherit !important",

                                        }

                                    ],
                style_header={
                    'backgroundColor': 'rgba(0,0,0,0)',
                    'font-size': '10px',
                    'color': '#04AEC4',
                    'text-align': 'center',
                    'border': '0.01px solid #04AEC4',
                    #'width': 'auto',
                    'font-color':'#04AEC4',
                    'font-weight':'bold',},
                sort_action='native',
                page_action='native',   # all data is passed to the table up-front
                page_size=6,
            ),dcc.Interval(id='interval-1FA1A01-table',interval=60*1000,n_intervals=0,)],style = {"background-color":"rgba(0,0,0,0)","border-color":"rgba(0,0,0,0)",}
    ), xs=12,sm=12,md=12,lg=12,xl=12),

# dbc.Col(dcc.Graph(figure=figtemp), width=3)

           ],
            className="mb-4",
         ),
  html.Hr(style={'borderWidth': "1.9vh", "width": "100%", "color": "#04AEC4"}),      
       #html.P(),
       
      # html.P(["℗ Powered by Drocon Infographics"], className = 'flicker2'),
        #########################################################
       
        html.H6("℗ Powered by Hidbuilt Analytics"
                ,style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)","text-align":"center","color":"#04AEC4",}
                ),
        html.P(),
        html.P(),
     
     
       
    ]
)
   
    ]
    , style = {"background-color":"#0a2351","border-color":"#04AEC4",})  ##0a2351,#002D62 #04AEC4


@app.callback(
    Output('load_currentvolume', 'children'),
    [Input('interval-currentvolume', 'n_intervals'), ])
def fn_currentvol(n_intervals):
    data = col.find()
    df = pd.DataFrame(data)
    df1 = df.loc[(df['device'] == '1FA1185')]
    df1['time'] = pd.to_datetime(df1['time'])
    df1['time'] += timedelta(hours=3)
    df1['sysdate'] =pd.to_datetime('today',format = "%Y-%m-%d %H:%M:%S",utc='true') ####################################################
    df1['timediff'] = (df1['sysdate'] - df1['time']).astype('timedelta64[s]') ####################################################
    df1 = df1[df1['timediff'] <= 259200] #3days###################################################
    df1['Level'] = round(df1['Level']* 1.4286 ,2)
    df1 = df1.sort_values(by = 'time',ascending = False)
    # df1['ΔVolume (Lts)'] = round(abs(df1['Level'] - df1['Level'].shift(-1)),2)
    # df1 = df1.rename(columns = {'_id':'Event_id','time':'Event_time (UTC+3)','Battery':'Battery_level (%)'
    #                           ,'Level':'Volume (Lts)'})
    # df1 = df1[['Event_id', 'Event_time (UTC+3)','Event_type','Volume (Lts)','ΔVolume (Lts)','Battery_level (%)']]
    Currentvolume = df1.iloc[0,4]
    return (Currentvolume)  
########################################
@app.callback(
    Output('load_currenttime', 'children'),
    [Input('interval-currenttime', 'n_intervals'), ])
def fn_currentime(n_intervals):
    data = col.find()
    df = pd.DataFrame(data)
    df1 = df.loc[(df['device'] == '1FA1185')]
    df1['time'] = pd.to_datetime(df1['time'])
    df1['time'] += timedelta(hours=3)
    df1 = df1.sort_values(by = 'time',ascending = False)
    df1['sysdate'] =pd.to_datetime('today',format = "%Y-%m-%d %H:%M:%S",utc='true') ####################################################
    df1['timediff'] = (df1['sysdate'] - df1['time']).astype('timedelta64[s]') ####################################################
    df1 = df1[df1['timediff'] <= 259200] #3days###################################################
    # df1['ΔVolume (Lts)'] = round(abs(df1['Level'] - df1['Level'].shift(-1)),2)
    # df1 = df1.rename(columns = {'_id':'Event_id','time':'Event_time (UTC+3)','Battery':'Battery_level (%)'
    #                           ,'Level':'Volume (Lts)'})
    # df1 = df1[['Event_id', 'Event_time (UTC+3)','Event_type','Volume (Lts)','ΔVolume (Lts)','Battery_level (%)']]
    Currenttime = df1.iloc[0,2]
    Currenttime = Currenttime.strftime("%d-%b-%Y %H:%M:%S")
    return (Currenttime)
########################################
@app.callback(
    Output('load_highestinc', 'children'),
    [Input('interval-highestinc', 'n_intervals'), ])
def fn_highestinc(n_intervals):
    data = col.find()
    df = pd.DataFrame(data)
    df1 = df.loc[(df['device'] == '1FA1185')]
    df1['time'] = pd.to_datetime(df1['time'])
    df1['time'] += timedelta(hours=3)
    df1['Level'] = round(df1['Level']* 1.4286 ,2)
    df1['Event_type'] = df1['Messagetype'].apply(lambda x: 'Level Increase' if x == 47 else 'Level Increase')
    df1 = df1.sort_values(by = 'time',ascending = False)
    df1['ΔVolume (Lts)'] = round(abs(df1['Level'] - df1['Level'].shift(-1)),2)
    df1['sysdate'] =pd.to_datetime('today',format = "%Y-%m-%d %H:%M:%S",utc='true') ####################################################
    df1['timediff'] = (df1['sysdate'] - df1['time']).astype('timedelta64[s]') ####################################################
    df1 = df1[df1['timediff'] <= 259200] #3days###################################################
    maxlevinc = df1["ΔVolume (Lts)"].where(df1['Event_type'] == 'Level Increase').max()
    return (maxlevinc)
########################################
@app.callback(
    Output('load_highestinctime', 'children'),
    [Input('interval-highestinctime', 'n_intervals'), ])
def fn_highestinctime(n_intervals):
    data = col.find()
    df = pd.DataFrame(data)
    df1 = df.loc[(df['device'] == '1FA1185')]
    df1['time'] = pd.to_datetime(df1['time'])
    df1['time'] += timedelta(hours=3)
    df1['Level'] = round(df1['Level']* 1.4286 ,2)
    df1['Event_type'] = df1['Messagetype'].apply(lambda x: 'Level Increase' if x == 47 else 'Level Decrease')
    df1 = df1.sort_values(by = 'time',ascending = False)
    df1['ΔVolume (Lts)'] = round(abs(df1['Level'] - df1['Level'].shift(-1)),2)
    df1['sysdate'] =pd.to_datetime('today',format = "%Y-%m-%d %H:%M:%S",utc='true') ####################################################
    df1['timediff'] = (df1['sysdate'] - df1['time']).astype('timedelta64[s]') ####################################################
    df1 = df1[df1['timediff'] <= 259200] #3days###################################################
    maxlevinc = df1["ΔVolume (Lts)"].where(df1['Event_type'] == 'Level Increase').max()
    maxinctime = df1["time"].where(df1['ΔVolume (Lts)'] == maxlevinc).max()
    maxinctime = maxinctime.strftime("%d-%b-%Y %H:%M:%S")
    return (maxinctime)  
########################################    

@app.callback(
    Output('load_highestdec', 'children'),
    [Input('interval-highestdec', 'n_intervals'), ])
def fn_highestdec(n_intervals):
    data = col.find()
    df = pd.DataFrame(data)
    df1 = df.loc[(df['device'] == '1FA1185')]
    df1['time'] = pd.to_datetime(df1['time'])
    df1['time'] += timedelta(hours=3)
    df1['Level'] = round(df1['Level']* 1.4286 ,2)
    df1['Event_type'] = df1['Messagetype'].apply(lambda x: 'Level Increase' if x == 47 else 'Level Decrease')
    df1 = df1.sort_values(by = 'time',ascending = False)
    df1['ΔVolume (Lts)'] = round(abs(df1['Level'] - df1['Level'].shift(-1)),2)
    df1['sysdate'] =pd.to_datetime('today',format = "%Y-%m-%d %H:%M:%S",utc='true') ####################################################
    df1['timediff'] = (df1['sysdate'] - df1['time']).astype('timedelta64[s]') ####################################################
    df1 = df1[df1['timediff'] <= 259200] #3days###################################################
    maxlevdec = df1["ΔVolume (Lts)"].where(df1['Event_type'] == 'Level Decrease').max()
    # maxlevdec = df1["ΔVolume (Lts)"].where(df1['Event_type'] == 'Level Decrease').max()
    return (maxlevdec)    
########################################

@app.callback(
    Output('load_highestdectime', 'children'),
    [Input('interval-highestdectime', 'n_intervals'), ])
def fn_highestdectime(n_intervals):
    data = col.find()
    df = pd.DataFrame(data)
    df1 = df.loc[(df['device'] == '1FA1185')]
    df1['time'] = pd.to_datetime(df1['time'])
    df1['time'] += timedelta(hours=3)
    df1['Level'] = round(df1['Level']* 1.4286 ,2)
    df1['Event_type'] = df1['Messagetype'].apply(lambda x: 'Level Increase' if x == 47 else 'Level Decrease')
    df1 = df1.sort_values(by = 'time',ascending = False)
    df1['ΔVolume (Lts)'] = round(abs(df1['Level'] - df1['Level'].shift(-1)),2)
    df1['sysdate'] =pd.to_datetime('today',format = "%Y-%m-%d %H:%M:%S",utc='true') ####################################################
    df1['timediff'] = (df1['sysdate'] - df1['time']).astype('timedelta64[s]') ####################################################
    df1 = df1[df1['timediff'] <= 259200] #3days###################################################
    maxlevdec = df1["ΔVolume (Lts)"].where(df1['Event_type'] == 'Level Decrease').max()
    maxdectime = df1["time"].where(df1['ΔVolume (Lts)'] == maxlevdec).max()
    maxdectime = maxdectime.strftime("%d-%b-%Y %H:%M:%S")
    return (maxdectime)    
########################################

@app.callback(
    Output('load_currentvolumedf2', 'children'),
    [Input('interval-currentvolumedf2', 'n_intervals'), ])
def fn_currentvoldf2(n_intervals):
    data = col.find()
    df = pd.DataFrame(data)
    df2 = df.loc[(df['device'] == '1FA1A01')]
    df2['time'] = pd.to_datetime(df2['time'])
    df2['time'] += timedelta(hours=3)
    df2['Level'] = round(df2['Level']* 1.4286 ,2)
    df2 = df2.sort_values(by = 'time',ascending = False)
    df2['ΔVolume (Lts)'] = round(abs(df2['Level'] - df2['Level'].shift(-1)),2)
    df2['sysdate'] =pd.to_datetime('today',format = "%Y-%m-%d %H:%M:%S",utc='true') ####################################################
    df2['timediff'] = (df2['sysdate'] - df2['time']).astype('timedelta64[s]') ####################################################
    df2 = df2[df2['timediff'] <= 259200] #3days###################################################
    # df2 = df2.rename(columns = {'_id':'Event_id','time':'Event_time (UTC+3)','Battery':'Battery_level (%)'
    #                           ,'Level':'Volume (Lts)'})
    # df2 = df2[['Event_id', 'Event_time (UTC+3)','Event_type','Volume (Lts)','ΔVolume (Lts)','Battery_level (%)']]
    Currentvolumedf2 = df2.iloc[0,4]
    return (Currentvolumedf2)  
########################################
@app.callback(
    Output('load_currenttimedf2', 'children'),
    [Input('interval-currenttimedf2', 'n_intervals'), ])
def fn_currentimedf2(n_intervals):
    data = col.find()
    df = pd.DataFrame(data)
    df2 = df.loc[(df['device'] == '1FA1A01')]
    df2['time'] = pd.to_datetime(df2['time'])
    df2['time'] += timedelta(hours=3)
    df2 = df2.sort_values(by = 'time',ascending = False)
    df2['ΔVolume (Lts)'] = round(abs(df2['Level'] - df2['Level'].shift(-1)),2)
    df2['sysdate'] =pd.to_datetime('today',format = "%Y-%m-%d %H:%M:%S",utc='true') ####################################################
    df2['timediff'] = (df2['sysdate'] - df2['time']).astype('timedelta64[s]') ####################################################
    df2 = df2[df2['timediff'] <= 259200] #3days###################################################
    # df2 = df2.rename(columns = {'_id':'Event_id','time':'Event_time (UTC+3)','Battery':'Battery_level (%)'
    #                           ,'Level':'Volume (Lts)'})
    # df2 = df2[['Event_id', 'Event_time (UTC+3)','Event_type','Volume (Lts)','ΔVolume (Lts)','Battery_level (%)']]
    Currenttimedf2 = df2.iloc[0,2]
    Currenttimedf2 = Currenttimedf2.strftime("%d-%b-%Y %H:%M:%S")
    return (Currenttimedf2)
########################################
@app.callback(
    Output('load_highestincdf2', 'children'),
    [Input('interval-highestincdf2', 'n_intervals'), ])
def fn_highestincdf2(n_intervals):
    data = col.find()
    df = pd.DataFrame(data)
    df2 = df.loc[(df['device'] == '1FA1A01')]
    df2['time'] = pd.to_datetime(df2['time'])
    df2['time'] += timedelta(hours=3)
    df2['Level'] = round(df2['Level']* 1.4286 ,2)
    df2['Event_type'] = df2['Messagetype'].apply(lambda x: 'Level Increase' if x == 47 else 'Level Decrease')
    df2 = df2.sort_values(by = 'time',ascending = False)
    df2['ΔVolume (Lts)'] = round(abs(df2['Level'] - df2['Level'].shift(-1)),2)
    df2['sysdate'] =pd.to_datetime('today',format = "%Y-%m-%d %H:%M:%S",utc='true') ####################################################
    df2['timediff'] = (df2['sysdate'] - df2['time']).astype('timedelta64[s]') ####################################################
    df2 = df2[df2['timediff'] <= 259200] #3days###################################################
    maxlevincdf2 = df2["ΔVolume (Lts)"].where(df2['Event_type'] == 'Level Increase').max()
    return (maxlevincdf2)
########################################
@app.callback(
    Output('load_highestinctimedf2', 'children'),
    [Input('interval-highestinctimedf2', 'n_intervals'), ])
def fn_highestinctimedf2(n_intervals):
    data = col.find()
    df = pd.DataFrame(data)
    df2 = df.loc[(df['device'] == '1FA1A01')]
    df2['time'] = pd.to_datetime(df2['time'])
    df2['time'] += timedelta(hours=3)
    df2['Level'] = round(df2['Level']* 1.4286 ,2)
    df2['Event_type'] = df2['Messagetype'].apply(lambda x: 'Level Increase' if x == 47 else 'Level Decrease')
    df2 = df2.sort_values(by = 'time',ascending = False)
    df2['ΔVolume (Lts)'] = round(abs(df2['Level'] - df2['Level'].shift(-1)),2)
    df2['sysdate'] =pd.to_datetime('today',format = "%Y-%m-%d %H:%M:%S",utc='true') ####################################################
    df2['timediff'] = (df2['sysdate'] - df2['time']).astype('timedelta64[s]') ####################################################
    df2 = df2[df2['timediff'] <= 259200] #3days###################################################
    maxlevincdf2 = df2["ΔVolume (Lts)"].where(df2['Event_type'] == 'Level Increase').max()
    maxinctimedf2 = df2["time"].where(df2['ΔVolume (Lts)'] == maxlevincdf2).max()
    maxinctimedf2 = maxinctimedf2.strftime("%d-%b-%Y %H:%M:%S")
    return (maxinctimedf2)  
########################################    

@app.callback(
    Output('load_highestdecdf2', 'children'),
    [Input('interval-highestdecdf2', 'n_intervals'), ])
def fn_highestdecdf2(n_intervals):
    data = col.find()
    df = pd.DataFrame(data)
    df2 = df.loc[(df['device'] == '1FA1A01')]
    df2['time'] = pd.to_datetime(df2['time'])
    df2['time'] += timedelta(hours=3)
    df2['Level'] = round(df2['Level']* 1.4286 ,2)
    df2['Event_type'] = df2['Messagetype'].apply(lambda x: 'Level Increase' if x == 47 else 'Level Decrease')
    df2 = df2.sort_values(by = 'time',ascending = False)
    df2['ΔVolume (Lts)'] = round(abs(df2['Level'] - df2['Level'].shift(-1)),2)
    df2['sysdate'] =pd.to_datetime('today',format = "%Y-%m-%d %H:%M:%S",utc='true') ####################################################
    df2['timediff'] = (df2['sysdate'] - df2['time']).astype('timedelta64[s]') ####################################################
    df2 = df2[df2['timediff'] <= 259200] #3days###################################################
    maxlevdecdf2 = df2["ΔVolume (Lts)"].where(df2['Event_type'] == 'Level Decrease').max()
    return (maxlevdecdf2)    
########################################

@app.callback(
    Output('load_highestdectimedf2', 'children'),
    [Input('interval-highestdectimedf2', 'n_intervals'), ])
def fn_highestdectimedf2(n_intervals):
    data = col.find()
    df = pd.DataFrame(data)
    df2 = df.loc[(df['device'] == '1FA1A01')]
    df2['time'] = pd.to_datetime(df2['time'])
    df2['time'] += timedelta(hours=3)
    df2['Level'] = round(df2['Level']* 1.4286 ,2)
    df2['Event_type'] = df2['Messagetype'].apply(lambda x: 'Level Increase' if x == 47 else 'Level Decrease')
    df2 = df2.sort_values(by = 'time',ascending = False)
    df2['ΔVolume (Lts)'] = round(abs(df2['Level'] - df2['Level'].shift(-1)),2)
    df2['sysdate'] =pd.to_datetime('today',format = "%Y-%m-%d %H:%M:%S",utc='true') ####################################################
    df2['timediff'] = (df2['sysdate'] - df2['time']).astype('timedelta64[s]') ####################################################
    df2 = df2[df2['timediff'] <= 259200] #3days###################################################
    maxlevdecdf2 = df2["ΔVolume (Lts)"].where(df2['Event_type'] == 'Level Decrease').max()
    maxdectimedf2 = df2["time"].where(df2['ΔVolume (Lts)'] == maxlevdecdf2).max()
    maxdectimedf2 = maxdectimedf2.strftime("%d-%b-%Y %H:%M:%S")
    return (maxdectimedf2)    
########################################


########################################
# @app.callback(Output('1FA1185-tank', 'value'),
#               Input('interval-1FA1185-tank', 'n_intervals'))
# def update_output(n_intervals):
#     data = col.find()
#     df = pd.DataFrame(data)
#     df1 = df.loc[(df['device'] == '1FA1185')]
#     df1['Level'] = round(df1['Level']* 1.4286 ,2)
#     df1 = df1.sort_values(by = 'time',ascending = False)
   
#     value = df1.iloc[0,4]
#     return value

########################################
   
# @app.callback(Output('1FA1A01-tank', 'value'),
#               Input('interval-1FA1A01-tank', 'n_intervals'))
# def update_output2(n_intervals):
#     data = col.find()
#     df = pd.DataFrame(data)
#     df2 = df.loc[(df['device'] == '1FA1A01')]
#     df2['Level'] = round(df2['Level']* 1.4286 ,2)
#     df2 = df2.sort_values(by = 'time',ascending = False)
#     value = df2.iloc[0,4]
#     return value

########################################
   
@app.callback(Output('load-1FA1185-graph', 'figure'),
              Input('interval-1FA1185-graph', 'n_intervals'))
def update_1FA1185_graph(n_intervals):
    data = col.find()
    df = pd.DataFrame(data)
    df1 = df.loc[(df['device'] == '1FA1185')] #  1FA1A01
    df1['time'] = pd.to_datetime(df1['time'])
    df1['time'] += timedelta(hours=3)
    # df1['actual_level'] = 7000 - df1['Level']
    df1['Level'] = round(df1['Level']* 1.4286 ,2)
    df1['Event_type'] = df1['Messagetype'].apply(lambda x: 'Level Increase' if x == 47 else 'Level Decrease')
    df1 = df1.sort_values(by = 'time',ascending = False)
    df1['ΔVolume (Lts)'] = round(abs(df1['Level'] - df1['Level'].shift(-1)),2)
    df1['sysdate'] =pd.to_datetime('today',format = "%Y-%m-%d %H:%M:%S",utc='true') ####################################################
    df1['timediff'] = (df1['sysdate'] - df1['time']).astype('timedelta64[s]') ####################################################
    df1 = df1[df1['timediff'] <= 259200] #3days###################################################
    df1 = df1.rename(columns = {'_id':'Event_id','time':'Event_time (UTC+3)','Battery':'Battery_level (%)'
                              ,'Level':'Volume (Lts)'})
    df1 = df1[['Event_id', 'Event_time (UTC+3)','Event_type','Volume (Lts)','ΔVolume (Lts)','Battery_level (%)']]
    fig1FA1185 = px.area(df1, x="Event_time (UTC+3)", y="Volume (Lts)",line_shape='spline',
                      title='Volume Trend',
                      labels={
                         "Event_time (UTC+3)": "Event_time (UTC+3)",
                         "Volume (Lts)": "Volume (Lts)"
                     }
                      , color_discrete_sequence=["#04AEC4"],height=325,
                      
                      )
    fig1FA1185.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    'margin':{'l': 10, 'r': 10},
    'font_color':"#ffffff",
    'title_font_color':"#ffffff",
    "title_font":{'size': 15},
    })
    fig1FA1185.update_xaxes(showgrid=True)
    fig1FA1185.update_yaxes(showgrid=True)
    fig1FA1185.layout.xaxis.fixedrange = True
    fig1FA1185.layout.yaxis.fixedrange = True
    
    return fig1FA1185

########################################
   
@app.callback(Output('load-1FA1A01-graph', 'figure'),
              Input('interval-1FA1A01-graph', 'n_intervals'))
def update_1FA1A01_graph(n_intervals):
    data = col.find()
    df = pd.DataFrame(data)
    df2 = df.loc[(df['device'] == '1FA1A01')] #  
    df2['time'] = pd.to_datetime(df2['time'])
    df2['time'] += timedelta(hours=3)
    # df['actual_level'] = 7000 - df['Level']
    df2['Level'] = round(df2['Level']* 1.4286 ,2)
    df2['Event_type'] = df2['Messagetype'].apply(lambda x: 'Level Increase' if x == 47 else 'Level Decrease')
    df2 = df2.sort_values(by = 'time',ascending = False)
    df2['ΔVolume (Lts)'] = round(abs(df2['Level'] - df2['Level'].shift(-1)),2)
    df2['sysdate'] =pd.to_datetime('today',format = "%Y-%m-%d %H:%M:%S",utc='true') ####################################################
    df2['timediff'] = (df2['sysdate'] - df2['time']).astype('timedelta64[s]') ####################################################
    df2 = df2[df2['timediff'] <= 259200] #3days###################################################
    df2 = df2.rename(columns = {'_id':'Event_id','time':'Event_time (UTC+3)','Battery':'Battery_level (%)'
                              ,'Level':'Volume (Lts)'})
    df2 = df2[['Event_id', 'Event_time (UTC+3)','Event_type','Volume (Lts)','ΔVolume (Lts)','Battery_level (%)']]
    fig1FA1A01 = px.area(df2, x="Event_time (UTC+3)", y="Volume (Lts)",line_shape='spline',title='Volume Trend',
                     labels={
                        "Event_time (UTC+3)": "Event_time (UTC+3)",
                        "Volume (Lts)": "Volume (Lts)"
                    }
                     , color_discrete_sequence=["#04AEC4"],height=325
                     )
    fig1FA1A01.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    'margin':{'l': 10, 'r': 10},
    'font_color':"#ffffff",
    'title_font_color':"#ffffff",
    "title_font":{'size': 15},
    })
    fig1FA1A01.update_xaxes(showgrid=True)
    fig1FA1A01.update_yaxes(showgrid=True)
    fig1FA1A01.layout.xaxis.fixedrange = True
    fig1FA1A01.layout.yaxis.fixedrange = True
    return fig1FA1A01

########################################
   
@app.callback(Output('load-1FA1185-table', 'data'),
              Input('interval-1FA1185-table', 'n_intervals'))
def update_1FA1185_table(n_intervals):
    data = col.find()
    df = pd.DataFrame(data)
    df1 = df.loc[(df['device'] == '1FA1185')] #  1FA1A01
    df1['time'] = pd.to_datetime(df1['time'])
    df1['time'] += timedelta(hours=3)
    # df1['actual_level'] = 7000 - df1['Level']
    df1['Level'] = round(df1['Level']* 1.4286 ,2)
    df1['Event_type'] = df1['Messagetype'].apply(lambda x: 'Level Increase' if x == 47 else 'Level Decrease')
    df1 = df1.sort_values(by = 'time',ascending = False)
    df1['ΔVolume (Lts)'] = round(abs(df1['Level'] - df1['Level'].shift(-1)),2)
    df1 = df1.rename(columns = {'_id':'Event_id','time':'Event_time (UTC+3)','Battery':'Battery_level (%)'
                              ,'Level':'Volume (Lts)'})
    df1 = df1[['Event_time (UTC+3)','Event_type','Volume (Lts)','ΔVolume (Lts)',]]
    newdf2 = df1.to_dict('records')
    return (newdf2)

########################################
   
@app.callback(Output('load-1FA1A01-table', 'data'),
              Input('interval-1FA1A01-table', 'n_intervals'))
def update_1FA1A01_table(n_intervals):
    data = col.find()
    df = pd.DataFrame(data)
    df2 = df.loc[(df['device'] == '1FA1A01')] #  
    df2['time'] = pd.to_datetime(df2['time'])
    df2['time'] += timedelta(hours=3)
    # df['actual_level'] = 7000 - df['Level']
    df2['Level'] = round(df2['Level']* 1.4286 ,2)
    df2['Event_type'] = df2['Messagetype'].apply(lambda x: 'Level Increase' if x == 47 else 'Level Decrease')
    df2 = df2.sort_values(by = 'time',ascending = False)
    df2['ΔVolume (Lts)'] = round(abs(df2['Level'] - df2['Level'].shift(-1)),2)
    df2 = df2.rename(columns = {'_id':'Event_id','time':'Event_time (UTC+3)','Battery':'Battery_level (%)'
                              ,'Level':'Volume (Lts)'})
    df2 = df2[['Event_time (UTC+3)','Event_type','Volume (Lts)','ΔVolume (Lts)',]]
    newdf3 = df2.to_dict('records')
    return (newdf3)

if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server(debug=True, host="0.0.0.0", port=8080)
