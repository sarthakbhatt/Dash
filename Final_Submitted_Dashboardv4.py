import dash

import dash_core_components as dcc

import dash_html_components as html

import dash_table_experiments as dt

import pandas as pd
#import base64
import numpy as np

from plotly import graph_objs as go

from plotly.graph_objs import *

from dash.dependencies import Input, Output, State
#, Event

from plotly.graph_objs import Scatter, Layout, Data, Figure, Bar,Margin
import copy
import base64

app = dash.Dash(__name__)

server = app.server

app.title = 'UP100'



# API keys and datasets

mapbox_access_token = 'pk.eyJ1IjoidXAxMDAiLCJhIjoiY2p0cG9hN3V2MDJmdjQ0bjUzbDZzZmo5bCJ9.5v_rGU1iRv8_VzLC_6GRWQ'

#map_data = pd.read_csv("nyc-wi-fi-hotspot-locations.csv")

map_data=pd.read_excel("21.xlsx")
dnew=pd.read_excel("final_MDTGPSdata.xlsx")
dff=pd.read_excel('final_gpsavail.xlsx')
data=pd.read_excel("fuelfindingnew4.xlsx")
fuel=data.groupby(["VehicleNo.","District","Model","Month"]).sum()
fuel.reset_index(inplace=True)
fuel["Mileage"]=fuel["Distancetravelled"]/fuel["Quantity"]
fuel.sort_values(by=['District','Model','Mileage'],inplace=True)
fuel_state=fuel.groupby(['Model']).mean()
fuel_state.reset_index(inplace=True)
Mileage_Bolero=fuel_state[fuel_state["Model"]=="Bolero"]["Mileage"]
Mileage_Innova=fuel_state[fuel_state["Model"]=="Innova"]["Mileage"]
Mileage_Innova=Mileage_Innova.tolist()
Mileage_Bolero=Mileage_Bolero.tolist()
Mileage_Bolero=Mileage_Bolero[0]
Mileage_Innova=Mileage_Innova[0]
# Selecting only required columns

map_data = map_data[['Event_Id','District','Policestation','Event_Lat','Event_Long','Type_Of_Event','Date']].drop_duplicates()

list1=map_data['Type_Of_Event'].nunique()
list2=map_data['Type_Of_Event'].unique()
list3=map_data['Type_Of_Event'].drop_duplicates().tolist()
# Boostrap CSS.

app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})

###############################
trace_1 = go.Scatter(x = dnew.END_TIME, y = dnew['PRV_AVAILABLE_ON_GPS_MDT'],
                    name = 'PRV_AVAILABLE_ON_GPS_MDT',
                    line = dict(width = 2,
                                color = 'rgb(229, 151, 50)'))
layout = go.Layout(title = 'Count of Events',
                   hovermode = 'closest')
fig = go.Figure(data = [trace_1], layout = layout)


#  Layouts
                     
# Creating layouts for datatable
layout_right = copy.deepcopy(layout)
layout_right['height'] = 350
#layout_right['margin-top'] = '20'
#layout_right['font-size'] = '12'



# Components style
def color_scale(md, rows=[]):
    color = []
    for row in md['Type_Of_Event']:
        if row == 'ACCIDENT':
            color.append("#FF0000")
        elif row == 'THEFT':
            color.append("#191970")
        elif row == 'DISPUTE':
            color.append("#E1CD44")
        elif row == 'DOMESTIC VIOLENCE':
            color.append("#228B22")
        elif row == 'ASSAULT/RIOT/COMMOTION':
            color.append("#B8D343")
        elif row == 'GAMBLING':
            color.append("#	#FFFF00")
        elif row == 'POLLUTION':
            color.append("#7FFFD4")
        elif row == 'ROBBERY':
            color.append("#8B4513")
        elif row == 'THREAT IN PERSON':
            color.append("#F3C644")
        elif row == 'DOMESTIC VIOLENCE':
            color.append("#F2BE41")
        elif row == 'ATTEMPTED MURDER':
            color.append("#F0AE3D")
        elif row == 'INFORMATION_AGAINST_POLICE':
            color.append("#EFA73B")
        elif row == 'FEMALE HARRASSMENT':
            color.append("#EE9F39")
        elif row == 'PROPERTY DISPUTES':
            color.append("#ED8934")
        elif row == 'MEDIUM_FIRE':
            color.append("#B22222")
        elif row == 'GRP':
            color.append("#808080")
        elif row == 'ANIMALS RELATED':
            color.append("#00FF7F")
        elif row == 'Election Offences -During Polling':
            color.append("#191970")
        elif row == 'PICK POCKET':
            color.append("#BC8F8F")
        elif row == 'COMMUNAL RIOTS-CRIME- ETHNIC-COMMUNAL CLASH':
            color.append("#B8860B")
        elif row == 'KUMBH MELA':
            color.append("#FFD700")
        elif row == 'COMMUNAL RIOTS':
            color.append("#FFA07A")
        elif row == 'SUSPICIOUS OBJECT INFORMATION':
            color.append("#006400")
        elif row == 'DACOITY':
            color.append("#2F4F4F")
        elif row == 'FEMALE SEXUAL HARRASSMENT':
            color.append("#FF1493")
        else:
            color.append("#FD0101")
    for i in rows:
        color[i] = '#1500FA'
    return color

def gen_map(map_data,h,j):
    # groupby returns a dictionary mapping the values of the first field
    # 'classification' onto a list of record dictionaries with that
    # classification value.
    return {
        "data": [
                {
                    "type": "scattermapbox",
                    "lat": list(map_data['Event_Lat']),
                    "lon": list(map_data['Event_Long']),
                    "hoverinfo": "text",

                    "hovertext": [["Event No: {} <br>Police Station: {} <br>Type: {}".format(i,j,k)]

                                for i,j,k in zip(map_data['Event_Id'], map_data['Policestation'],map_data['Type_Of_Event'])],

                    "mode": "markers",
                    "name": list(map_data['Policestation']),
                    'text':list(map_data['Type_Of_Event']),
                    'showlegend': False,
                    "marker": {
                        "size": 16,
                        "opacity": 1.0,
                        "color": color_scale(map_data)
                    }
                }
            ],
        "layout": dict(
    autosize=True,
    height=600,
    uirevision =True,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=15), orientation='h'),
    title='Each Dot is a UP100 Event',
    mapbox=dict(
             uirevision =True,
        accesstoken=mapbox_access_token,
        style="mapbox://sprites/mapbox/streets-v10",
        center=dict(
            lon=h,
            lat=j
        ),
        zoom=13,
        bearing=0,
        pitch=30,
    )
)
    }
        
image_filename = 'UP100.jpg' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())   
#image_filename = 'EY.png' # replace with your own image
#encoded_image = base64.b64encode(open(image_filename, 'rb').read())   
image_filename1 = 'EY.png' # replace with your own image
encoded_image1 = base64.b64encode(open(image_filename1, 'rb').read())   
        
app.layout = html.Div([
    # Title - Row
    html.Div(
        [
            
            html.Img(
                src='data:image/png;base64,{}'.format(encoded_image.decode()),
                className='two columns',
                style={
                    'height': '25%',
                    'width': '25%',
                    'float': 'right',
                    'position': 'relative',
                    'padding-top': 19,
                    'padding-right': 0
                },
            ),
                    
            html.Img(
                src='data:image/png;base64,{}'.format(encoded_image1.decode()),
                className='four columns',
                style={
                    'height': '25%',
                    'width': '16%',
                    'float': 'left',
                    'position': 'relative',
                    'padding-top': 10,
                    'padding-right': 0
                },
            ),
                    html.H1(
                '               District Wise UP100 Events Analysis',
                style={'font-family': 'Helvetica',
                       "margin-top": "25",
                       "textAlign":"center",
                       "margin-bottom": "0",
                       'padding-left': 20,
                       'font-size': '45'},
                className='six columns',
            ),
        ],
        className='row'
    ),

      
    # Selectors
    dcc.Tabs(id="tabs", children=[
    dcc.Tab(label='Event Analysis', children=[   
            html.Div([
    html.Div(
        [
            html.Div(

                    [

                        html.H5('Choose Date:'),

                         dcc.Dropdown(

                          id = 'date',


                            options= [{'label': str(item),

                                                  'value': str(item)}

                                                 for item in set(map_data['Date'])],

                            multi=True,

                            value=' ' 

                        )],
                className='six columns',
                style={'margin-top': '20'}
            ),
                         
            html.Div(
                [

                        html.H5('Choose District:'),

                         dcc.Dropdown(

                           id = 'district',
                           options= [{'label': str(item),
                                    'value': str(item)}
                         for item in set(map_data['District'])],

                            multi=True,
                            value=' ' 

                        )

                    ],
                className='two columns',
                style={'margin-top': '20'}
            ),
            html.Div(
                [

                        html.H5('Choose Type:'),
                        dcc.Dropdown(
                        id = 'typeofevent',
                        options= [{'label': str(item),
                                   'value': str(item)}
                         for item in set(map_data['Type_Of_Event'])],
                            multi=True,
                            value= ['ACCIDENT','DISPUTE','THEFT','DOMESTIC VIOLENCE']
                        )

                    ],

                className='four columns',
                style={'margin-top': '20'}
            )
        ],
        className='row'
    ),

    # Map + table + Histogram
    html.Div(
        [
            html.Div(
                [
                    dcc.Graph(id='map-graph',
                              animate=True, 
                              style={'margin-top': '20'})
                ], className = "six columns"
            ),
            html.Div(
                [
                    dt.DataTable(
                        rows=map_data.to_dict('records'),
                        columns=map_data.columns,
                        row_selectable=True,
                        filterable=True,
                        sortable=True,
                        selected_row_indices=[],
                        id='datatable'),
                ],
                style=layout_right,
                className="six columns"
            ),
            html.Div(
                [
                    dcc.Graph(id="bar-graph")
                ],className="twelve columns")
        ], className="row"
    )
])
            ])
        ,  
            
#GPS Availability 10 min interval wise   
        dcc.Tab(label='GPS Analysis', children=[
                html.Div([
        html.Div([
        
        html.Div(

                    [

                        html.H5('Select District for PRV Status for every 10 min interval :'),

                        dcc.Dropdown(

                            id='type1',

                            options= [{'label': str(item),

                                                  'value': str(item)}

                                                 for item in set(dnew['District'])],



                            value=' '

                        )

                    ],
                className='six columns',
                style={'margin-top': '20'}
            ),
                        
                        html.Div(

                    [

                        html.H5('Select Date for PRV Status for every 10 min interval :'),

                        dcc.Dropdown(

                            id='date1',

                            options= [{'label': str(item),

                                                  'value': str(item)}

                                                 for item in set(dnew['Date'])],



                            value=' '

                        )

                    ],
                        className='six columns',
                style={'margin-top': '20'}
                )
                        ], className="row"
                        ),
                        
# bar-graph
          html.Div([
            html.Div([
                        dcc.Graph(
                            id='linegraph',figure=fig
                        )
                    ], className= 'twelve columns',
                         style={'margin-top': '20'}

                    )  
                ],className="row"),
        
        
                        
                        
#GPS unaviailibility

        # Selectors
        

html.Div(
                    [
                            html.Div([

                        html.H5('Select District for Unavailable PRVs on GPS in past 24 hours:'),

                        dcc.Dropdown(

                            id='type3',

                            options= [{'label': str(item),

                                                  'value': str(item)}

                                                 for item in set(dff['District'])],



                            value=' '

                        )

                    ],

                    className='six columns',

                    style={'margin-top': '20'}

                ),
        
                    html.Div(

                    [

                        html.H5('Select Date for Unavailable PRV on GPS in past 24 hours:'),

                        dcc.Dropdown(

                            id='date2',

                            options= [{'label': str(item),

                                                  'value': str(item)}

                                                 for item in set(dff['Date'])],

                            value=' '

                        )

                    ],

                    className='six columns',

                    style={'margin-top': '20'}

                ),                        
        
        ],className='row'
                        ),
                        
#bar-graph
html.Div([
        html.Div([

                        dcc.Graph(

                            id='line3-graph',figure=fig

                        )

                    ], className= 'twelve columns',
                       style={'margin-top': '20'}
                    )       
        ],className='row')
                        ])
        ]),

##fuel
                        
     
        # Selectors
        # Selectors
        
        dcc.Tab(label='Fuel Analysis', children=[
                html.Div([
                        
                        html.Div([
                                
                                 html.Div(

                    [

                        html.H5('Select District :'),

                        dcc.Dropdown(

                            id='type4',

                            options= [{'label': str(item),

                                                  'value': str(item)}

                                                 for item in set(fuel['District'])],



                            value=' '

                        )

                    ],

                    className='four columns',

                    style={'margin-top': '20'}

                ),
                        
                    html.Div(

                    [

                        html.H5('Select Month:'),

                        dcc.Dropdown(

                            id='date3',

                            options= [{'label': str(item),

                                                  'value': str(item)}

                                                 for item in set(fuel['Month'])],



                            value=' '

                        )

                    ],

                    className='four columns',

                    style={'margin-top': '20'}

                ),
                        
                            html.Div(

                    [

                        html.H5('Select Model:'),

                        dcc.Dropdown(

                            id='model',

                            options= [{'label': str(item),

                                                  'value': str(item)}

                                                 for item in set(fuel['Model'])],



                            value=' '

                        )

                    ],

                    className='four columns',

                    style={'margin-top': '20'}

                ), 
                        
                        
                        
                        
                        
                        
                        #plot fuel
                        html.Div([
                        html.Div([

                        dcc.Graph(

                            id='line4-graph',figure=fig

                        )

                    ], className= 'twelve columns'

                    )  
            ],className='row')
                        ])
                        
                        ])
                        ])
                        ],style={
            'height': '55px','fontWeight': 'bold', 'font-size': '22'})
                                                         
               ], className='ten columns offset-by-one')
                        
 



@app.callback(

    Output('datatable', 'rows'),
    [Input('date','value'),
     Input('district','value'),
     Input('typeofevent','value')])

def update_rows1(Date,District,Type_Of_Event):

    map_aux = map_data.copy()


    # Type_Of_Event filter

    #date filter
    map_aux = map_aux[map_aux['Date'].isin(Date)]
    # District filter
    map_aux = map_aux[map_aux['District'].isin(District)]
    #typeofevent
    map_aux = map_aux[map_aux['Type_Of_Event'].isin(Type_Of_Event)]

    rows = map_aux.to_dict('records')

    return rows

@app.callback(
    Output('datatable', 'selected_row_indices'),
    [Input('bar-graph', 'selectedData')],
    [State('datatable','selected_row_indices')])
def update_rows2(selectedData, rows):
    if selectedData:
        rows = []
        for point in selectedData['points']:
            rows.append(point['pointNumber'])
    return rows



@app.callback(
    Output('map-graph', 'figure'),
    [Input('datatable', 'rows'),
     Input('datatable', 'selected_row_indices')])
def map_selection(rows, selected_row_indices):
    aux = pd.DataFrame(rows)
    temp_df = aux.ix[selected_row_indices, :]
    h=temp_df['Event_Long'][0]
    j=temp_df['Event_Lat'][0]
    if len(selected_row_indices) == 0:
        return gen_map(aux)
    return gen_map(temp_df, h,j)




@app.callback(
    Output('bar-graph', 'figure'),
    [Input('datatable', 'rows'),
     Input('datatable', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    
    dff = pd.DataFrame(rows)


    data = Data([

         go.Bar(

             x=dff.groupby('Type_Of_Event', as_index = False).count()['Type_Of_Event'],

             y=dff.groupby('Type_Of_Event', as_index = False).count()['District'],
             text=dff.groupby('Type_Of_Event', as_index = False).count()['District'],
             textposition='auto',
             marker=dict(color='rgb(255,165,0)')
             

         )

     ])
    return go.Figure(data=data, layout=layout)


#Other graphs
    

@app.callback(

    Output('linegraph', 'figure'),

    [Input('type1', 'value'),Input('date1', 'value')])

def update_linefigure(District,Date):

    d = dnew[dnew['District']==District]
    d=d[d['Date']==Date]
    trace_2 = go.Scatter(x=d.END_TIME,y=d['PRV_AVAILABLE_ON_GPS_MDT'], mode = 'lines+markers',name = 'GPS Signal & MDT Status Available' )
    trace_3 = go.Scatter(x=d.END_TIME,y=d['PRV_AVAILABLE_ON_MDT'],name='Last Status Available On MDT',mode='lines+markers')
    fig=go.Figure(data=[trace_2,trace_3],layout=layout)
    return fig



@app.callback(

    Output('line4-graph', 'figure'),

    [Input('type4', 'value'),Input('date3', 'value'),Input('model', 'value')])

def update_linefuelfigure(District,Date,mod):

    dfuel = fuel[fuel['District']==District]
    d2=dfuel[dfuel['Month']==Date]
    d3=d2[d2['Model']==mod]
    
    d3.reset_index(inplace=True)
    
    if(mod=="Innova"):
        
        x1=d3["VehicleNo."]
        y1=[Mileage_Innova]*len(d3)
        trace_6 =go.Scatter(x=x1,y=y1,mode = 'lines+markers',name = 'State Average' )
    else:
        x1=d3["VehicleNo."]
        y1=[Mileage_Bolero]*len(d3)
        trace_6 =go.Scatter(x=x1,y=y1,mode = 'lines+markers',name = 'State Average' )   
 
    trace_5 = go.Scatter(x=d3["VehicleNo."],y=d3['Mileage'], mode = 'lines+markers',name = 'PRV wise mileage' )
    
    fig=go.Figure(data=[trace_5,trace_6],layout=layout)
    return fig



@app.callback(

    Output('line3-graph', 'figure'),

    [Input('type3', 'value'),Input('date2', 'value')])

def update_gpsfigure(District,Date):

    dff2 = dff[dff['District']==District]
    dff2=dff2[dff2['Date']==Date]
    '''trace_3 = go.Scatter(x=dff.END_TIME,y=dff['PRV_AVAILABLE'],name=val, line=dict(width=2,color='rgb(106,181,135)'))
    fig=go.Figure(data=[trace_3],layout=layout)
    return fig'''
    y1=dff2.groupby('PRV_NO', as_index = False).sum()['TIME_DIFFERENCE(Min)']
    x1 = dff2.groupby('PRV_NO', as_index = False).count()['PRV_NO']
    sortx = [x1 for _,x1 in sorted(zip(y1,x1))]
    sorty = sorted(y1)
    
    data = Data([

            go.Bar(

             x=sortx,

             y=sorty,
             text=sorty,
             textposition='auto',
             marker=dict(color='rgb(255,165,0)')

         )

     ])

    return {
           'data': data,
            'layout': go.Layout(
            title='MDT Off Duration for the Day',
            hovermode='closest',
            
        barmode='group',

        showlegend=False,

        dragmode="select"
            
        )
    }
    



                        
                        
if __name__ == '__main__':
    app.run_server(debug=True)        
        