import numpy as np
from flask import Flask, request, jsonify, render_template
import json
import pickle
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons
from geopy.geocoders import Nominatim
from pygeocoder import Geocoder
from helper import create_app, create_server,create_df,get_model, get_json, get_recommender
import dash
import dash_core_components as dcc
import dash_html_components as html
from sklearn.metrics import mean_squared_error
from math import sqrt  
from sklearn.metrics import r2_score
from dash.dependencies import Input, Output
from keras.models import load_model

import tensorflow as tf
global graph,model
graph = tf.get_default_graph()

#flask and dash initilization
app = create_app()
server = create_server(app)
df = create_df()

#create dataframes
area = df['area']
prices = df['prices']
schools = df['schools']
model_data = df['model_data']
c_property = df['c_property']
rew = df['rew']
rew_clean = df['rew_clean']
 
rew_latlong = df['latlong']

# Load the model
model = get_model()
gbr = model['gbr']
f1 = model['f1n']  
f2 = model['f2n']  
f3 = model['f3n']  
f4 = model['f4n']  
stackedmodel= model['stackedmodel']  

geo_json = get_json()
recommender = get_recommender()

#variables
neighbourhoods = list(np.array(area['Neighbourhood_Name']))
n_values = list(np.array(area['N_Value']))
options=[{'label':name, 'value':value} for name,value in zip(neighbourhoods,n_values)]
mapbox_access_token =  "pk.eyJ1IjoiamFja3AiLCJhIjoidGpzN0lXVSJ9.7YK6eRwUNFwd3ODZff6JvA"
year = 2020
GoogleMaps(
    app,
    key="AIzaSyAvzm0x2kmJoeqX6VY83lMa8pPRDDjH4sY"
)
cols = list(rew.columns)
type_list = cols[cols.index('House'):cols.index('Multifamily')+1]
 
    
def create_map(json_file):
    data = go.Data([
    go.Scattermapbox(
        lat=['49.246292'],
        lon=['-123.116226']
        )
    ])
    layout = go.Layout(
        height=600,
        clickmode="event+select",
        autosize=True,
        hovermode='closest',
        yaxis=dict(title='Mean Price'),
        mapbox=dict(
            layers=[
                dict(
                    sourcetype = 'geojson',
                    source = json_file,
                    type = 'fill',
                    color = 'rgba(163,22,19,0.8)',
                    opacity = 0.3
                )
            ],
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=49.246292,
                lon=-123.116226
            ),
            pitch=0,
            zoom=11,
            style='basic'
        ),
    )

    fig = dict(data=data, layout=layout)
    return fig

server.layout = html.Div(children=[
    html.Div([
       html.Div([
          dcc.Dropdown(
        options = options,
        value = 'CBD',
        id='area-dropdown',
        placeholder="Select an area"
        ),
           dcc.Graph(
            id="scatter-map",
            figure=create_map(geo_json) 
            ),
        html.Div([
        html.Div('Median House Price',id='median-house',className="col-sm-4"),
        html.Div('% of properties with price decrease',id='price-decrease',className="col-sm-3"),
        html.Div('Median House Age',id='median-age',className="col-sm-4")
    ],className="row")
],className="col-md-6"),
        
    html.Div([
        html.Div([
        html.Div([html.H6(children='Distribution of major property types'),
        dcc.Graph(id='pie')],className="col-md-6"),
        html.Div([html.H6(children='Average school ratings'),
        dcc.Graph(id='bar')],className="col-md-6")
        ],className="row"),
        html.H6(children='Median Price from 2006 - 2019'),
        dcc.Graph(id='plot')     
    ],className="col-md-6")   
    ],className="row")
],className="container-fluid")


@server.callback(
    [Output('pie', 'figure'),
     Output('plot', 'figure'),
     Output('bar','figure'),
     Output('scatter-map', 'figure'),
     Output('median-house', 'children'),
     Output('price-decrease', 'children'),
     Output('median-age', 'children')],
    [Input('area-dropdown', 'value')])
def set_display_children(selected_area):
    medians = area[area['N_Value'] == selected_area].values.tolist()[0][5:]
    x_axis = prices.columns[2:].tolist()
    y_axis=prices[prices['N_Value'] == selected_area].values.tolist()[0][2:]
    file_name= area[area['N_Value'] == selected_area].values.tolist()[0][0]
    with open('../data/geo-json/'+file_name+'.json') as f:
        json_file = json.load(f)
    a="Median House Price: "+"{0:.2f}".format(round(medians[0],2))+"million"
    b="% of properties with price decrease : "+"{0:.2f}".format(round(medians[1],2))
    c="Median House Age: "+str(round(medians[2],0))+" years"
    x_bar=schools[schools['N_Value']==selected_area]['School Name'].tolist()
    y_bar=schools[schools['N_Value']==selected_area]['2017-18 rating'].tolist()
    trace_bar = go.Bar(x=x_bar,y=y_bar)
    trace = go.Pie(labels=['Land', 'Strata'], values=area[area['N_Value'] == selected_area].values.tolist()[0][3:5])
    return {
        'data':[trace],
        'layout':go.Layout(
                     hovermode='closest',
                     height = 300,
             margin=go.layout.Margin(
                l=0,
                r=0,
                b=50,
                t=50,
                pad=2
            )
        )
     
    },{
           'data': [{
            'x': x_axis,
            'y': y_axis,
            'line': {
                'width': 3,
                'shape': 'spline'
            }
        }],
        'layout': go.Layout(
                     hovermode='closest',
                     height = 300,
                    xaxis= dict(
                    title= 'Year',
                    ticklen= 5,
                    zeroline= False,
                    gridwidth= 2,
                    automargin=True
                ),
                yaxis=dict(
                    title= 'Property price in million',
                    ticklen= 5,
                    gridwidth= 2,
                    automargin=True
                ) ,
            margin=go.layout.Margin(
        l=10,
        r=1,
        b=60,
        t=50,
        pad=2
    )
                    )
    },{
        'data':[trace_bar],
        'layout':go.Layout(
                     hovermode='closest',
                     height = 300,
                     xaxis=dict(title='School',automargin=True),
                     yaxis=dict(title='Rating',automargin=True),
                 margin=go.layout.Margin(
                l=0,
                r=0,
                b=40,
                t=40,
                pad=2
            )
        )
     },create_map(json_file),a,b,c

@app.route('/peek')
def peek():
    return 'Hello';

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rental')
def rental():
    return render_template('rental.html')

@app.route('/property')
def property():
    map=Map("simple-map", 49.23806279999999,-123.1556386)
    return render_template('property.html')

def create_user_chart(multiplier,pid):
    y_axis = c_property[c_property['PID']==pid]['CURRENT_HOUSE_PRICE'].tolist()
    x_axis = c_property[c_property['PID']==pid]['TAX_ASSESSMENT_YEAR'].tolist()
    
    if not y_axis:
        return False;
    price_2020 = multiplier * float(y_axis[-1:][0])
 
    trace_1 = go.Scatter(
    x = list(x_axis),
    y = y_axis,
    name = 'Ground Truth',
    mode = 'lines',
    marker = dict(
    line = dict(
            color = ('rgb(205, 12, 24)'),
            width = 4
    )
    )    
    )
    
    n_x = [x_axis[len(x_axis)-1],'2020']
    n_y = [y_axis[len(y_axis)-1],price_2020]
    
    trace_2 = go.Scatter(
    x = list(n_x),
    y = n_y,
    name = 'Estimated',
    mode = 'lines',
    connectgaps=True,
    marker = dict(
    line = dict(
            color = ('rgb(22, 96, 167)'),
            width = 4
    )
    )    
    )

    data = [trace_1,trace_2]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
    
def create_line_chart(predicted_price,selected_area):
    x_axis = prices.columns[2:].tolist()
    y_axis=prices[prices['Neighbourhood_Name'] == selected_area].values.tolist()[0][2:]

    trace_1 = go.Scatter(
    x = list(x_axis),
    y = y_axis,
    name = 'Ground Truth',
    mode = 'lines',
    marker = dict(
    line = dict(
            color = ('rgb(205, 12, 24)'),
            width = 4
    )
    )    
    )
    n_x = [x_axis[len(x_axis)-1],'2020']
    n_y = [y_axis[len(y_axis)-1],predicted_price]
    
    trace_2 = go.Scatter(
    x = list(n_x),
    y = n_y,
    name = 'Estimated',
    mode = 'lines',
    connectgaps=True,
    marker = dict(
    line = dict(
            color = ('rgb(22, 96, 167)'),
            width = 4
    )
    )    
    )

    data = [trace_1,trace_2]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


@app.route('/property_predict', methods=['GET', 'POST'])
def property_predict():
    if request.method == "POST":
        
        user_agent_received = request.get_json()
        interest_rate_2020=float(user_agent_received['interest'])
        Area = user_agent_received['area']
        pid = user_agent_received['pid']
        nbrhd = model_data[(model_data["NEIGHBOURHOOD_NAME"]==Area)]
        prev_price = nbrhd[nbrhd['TAX_ASSESSMENT_YEAR']==year-1]['CURRENT_MEDIAN_PRICE']
        sample_data = pd.DataFrame({"NEIGHBOURHOOD_NAME":Area,"TAX_ASSESSMENT_YEAR":year,"PREVIOUS_MEDIAN_PRICE":\
                           prev_price,"INTEREST_RATE":interest_rate_2020})

        indexed = pd.get_dummies(sample_data)

        req_cols = set(model_data['NEIGHBOURHOOD_NAME'].unique())-(set({Area}))

        for col in req_cols:
            indexed["NEIGHBOURHOOD_NAME_"+col]=0
        predicted_price = gbr.predict(indexed)[0] 
        response = {}
        response['price'] = round(predicted_price,2)
        response['graph_1'] = create_line_chart(predicted_price,Area)
        multiplier = predicted_price/(prev_price.tolist()[0])
        user_chart = create_user_chart(multiplier,pid)
        if user_chart != False:
            response['graph_2'] = user_chart
        else:
            response['graph_2'] = 'error'
        return jsonify(response)
    
    return jsonify({'error':'Missing Data!'})

def encode_data(htype,parea):
    
    encoded = []
    
    # Add Crime percentage
    
    crimep = {'V6E':9.652823,'V6H':8.577192,'V5T':8.09922,'V5M':6.480475,'V5L':6.361571,'V6J':6.026049,'V5N':5.794912,
              'V6A':5.666982,'V5K':4.266424,'V6M':3.76216,'V5W':3.643648,'V6L':3.232389,'V5V':3.110738,'V6P':2.989087,
              'V5P':2.39692,'V6S':2.266636,'V6R':1.380544,'V5Z':1.316187,'V6G':0.784061,'V6N':0.096536}
    
    if parea in crimep.keys():
        encoded.append(crimep[parea])
    else:
        encoded.append(0.0)
    
    # Encoding House type
    
    if htype in ['Apt/Condo','Mfd/Mobile Home','Townhouse']:
        encoded.append(0)
        encoded.append(1)
    else:
        encoded.append(1)
        encoded.append(0)
        
    
    # Encoding School type
    
    srs = {'V4A':[0,1,0],'V4N':[0,1,0],'V4P':[0,1,0],'V5K':[0,1,0],'V5M':[0,1,0],'V5N':[0,1,0],'V5P':[0,1,0],'V5R':[0,1,0],
           'V5S':[0,1,0],'V5T':[0,1,0],'V5X':[0,1,0],'V5Z':[0,1,0],'V6B':[0,1,0],'V6H':[0,1,0],'V6J':[1,0,0],'V6K':[0,1,0],
           'V6L':[0,1,0],'V6M':[0,1,0],'V6N':[0,1,0],'V6P':[0,1,0],'V6R':[0,1,0],'V6S':[1,0,0],'V6T':[0,1,0],'V6Z':[0,1,0]}
    
    if parea not in srs.keys():
        encoded = encoded + [0,0,1]
    else:
        encoded = encoded + srs[parea]
        
    # Encoding Area
            
    areas = ['V3S', 'V7C', 'V3W', 'V4N', 'V6Y', 'V6X', 'V4A', 'V2X', 'V7E', 'V3B','V3T', 'V4B', 'V3R', 'V3A', 'V6B',
         'V5R', 'V3M', 'V5H','V3E', 'V2Y', 'V3Z', 'V7S', 'V6P', 'V6Z', 'V7A', 'V3K', 'V3J', 'V3N', 'V7L', 'V3H',
         'V3C', 'V4C', 'V3X', 'V5J', 'V1M', 'V3V', 'V5N', 'V6E', 'V5E', 'V7V', 'V4P', 'V5C', 'V4K', 'V4R', 'V5X',
         'V5Z', 'V2W', 'V6S','V2Z', 'V6M', 'V3L', 'V7M', 'V6G', 'V5M', 'V7W', 'V5A', 'V4M', 'V6N', 'V5Y', 'V5S',
         'V7R', 'V7J', 'V5P', 'V6R', 'V7T', 'V5B', 'V7P', 'V3Y', 'V4W', 'V6J', 'V4L', 'V7G', 'V6K', 'V6A', 'V5G',
         'V5T', 'V7N','V4E', 'V6H', 'V6V', 'V5K', 'V6T', 'V6C', 'V5L', 'V6L', 'V5V', 'V5W', 'V7H', 'V7K', 'V6W',
         'V0N', 'V0V', 'V7B', 'V3G', 'V0X', 'V2S', 'V2T', 'V4S', 'V4X', 'V1V', 'V2E', 'V0T', 'V9L', 'V8K', 'V0H',
         'V0Y','V0M', 'V8V', 'V2J', 'V2A', 'V1L', 'V2H', 'V0B', 'V0L', 'V4G']
    
    for i in areas:
        if i == parea:
            encoded.append(1)
        else:
            encoded.append(0)
            
    return encoded

def predict_price(bed,bath,area_sqft,age,fireplaces,housetype,area):
    
    inputs = [bed,bath,area_sqft,age,fireplaces]
    inputs = inputs + encode_data(housetype,area)
    sample = []
    sample.append(tuple(inputs))
    
    inp_sample = pd.DataFrame(sample)
    inp_sample = np.array(inp_sample).reshape(1,-1)
    
    p1 = f1.predict(inp_sample)[0]
    p2 = f2.predict(inp_sample)[0]
    p3 = f3.predict(inp_sample)[0]
    with graph.as_default():
        p4 = f4.predict(inp_sample)[0][0]
    
    newInp = pd.DataFrame([(p1,p2,p3,p4)])
    newInp = np.array(newInp).reshape(1,-1)
    predicted_price = stackedmodel.predict(newInp)[0]
    
    return predicted_price

def map_feature(value):
    diction = {'House':0,'Apt/Condo':0,'Townhouse':0,'Land/Lot':0,'Duplex':0,'Mfd/Mobile Home':0,'Multifamily':0}
    for i in diction:
        if(i == value):
            diction[i]=1
    return diction

def rew_dataset(sample_df,rew,rew_latlong,rew_clean,area):
    req_cols = ['price','listing_id','bed','bath','area_sqft','fireplaces']+type_list
    rew = rew[req_cols]
    sim_data = rew[['price','listing_id','bed','bath','area_sqft','fireplaces']+type_list]
    sim_data.set_index('listing_id',inplace=True)
    #Add this row on top of all re
    sim_numeric = pd.concat([sample_df, sim_data], axis=0)
    #Normalize
    sim_normal = (sim_numeric - sim_numeric.min()) / (sim_numeric.max() - sim_numeric.min())

    #Normalized sample
    normal_sample = sim_normal.iloc[0,:]

    #normalized sim_data
    sim_normal = sim_normal.iloc[1:,:]
    
    vals = recommender.kneighbors([normal_sample])
    # get indices
    indices = list(vals[1][0])
    result_df = sim_data.iloc[indices,:]
    result_df = pd.merge(result_df,rew_clean,on="listing_id",how='inner')
    result_df =  result_df[result_df['area'] == area]
    result = pd.merge(rew_latlong,result_df,on="listing_id")
    latlon = result[['listing_id','lat','lon','price','bed','bath','area_sqft','fireplaces']]
    return result_df,latlon

def create_table(df):
    df = df[['listing_id','price', 'bed', 'bath', 'area_sqft', 'fireplaces', 'House', 'Apt/Condo',
               'Townhouse', 'Land/Lot', 'Duplex', 'Mfd/Mobile Home', 'Multifamily']]
    df = df.applymap(str)
    df.loc[df['House'] == '1', 'House'] = 'House'
    df.loc[df['Apt/Condo'] == '1', 'Apt/Condo'] = 'Apt/Condo'
    df.loc[df['Townhouse'] == '1', 'Townhouse'] = 'Townhouse'
    df.loc[df['Land/Lot'] == '1', 'Land/Lot'] = 'Land/Lot'
    df.loc[df['Duplex'] == '1', 'Duplex'] = 'Duplex'
    df.loc[df['Mfd/Mobile Home'] == '1', 'Mfd/Mobile Home'] = 'Mfd/Mobile Home'
    df.loc[df['Multifamily'] == '1', 'Multifamily'] = 'Multifamily'
    df = df.loc[:, ~(df == '0').all()]
    df = df.rename(columns={ df.columns[6]: "Type" })
    
    trace = go.Table(
    header=dict(values=list(df.columns),
                fill = dict(color='#C2D4FF'),
                align = ['left'] * 5),
    cells=dict(values=[df['listing_id'],df['price'],df['bed'],df['bath'],df['area_sqft'],df['fireplaces'],df['Type']],
           fill = dict(color='#F5F8FF'),
           align = ['left'] * 5,
           font = dict(color = '#506784', size = 12),
           height = 30))
    data = [trace] 
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/get_recommendation', methods=['GET', 'POST'])
def get_recommendation():
    if request.method == "POST":
        age = 12
        user_agent_received = request.get_json()
        area = user_agent_received['pid']
        bdrm = user_agent_received['bdrm']
        bthrm = user_agent_received['bthrm']
        sqrft = user_agent_received['sqrft']
        fire = user_agent_received['fire']
        features = user_agent_received['features']
        price = predict_price(bdrm,bthrm,sqrft,age,fire,features,area)
        
        sample_df = pd.DataFrame({"price":int(price),"bed":int(bdrm),"bath":int(bthrm),\
                              "area_sqft":int(sqrft),"fireplaces":int(fire)},index=[0])
        sample_df[features]=1
        type_cols = set(type_list)-(set({features}))
        for col in type_cols:
            sample_df[col]=0
        sample_df = sample_df[['price', 'bed', 'bath', 'area_sqft', 'fireplaces', 'House', 'Apt/Condo',
               'Townhouse', 'Land/Lot', 'Duplex', 'Mfd/Mobile Home', 'Multifamily']]
        
        df,latlong = rew_dataset(sample_df,rew,rew_latlong,rew_clean,area)
       
        response = {}
        if df.empty:
            return jsonify({'error':'Missing Data!'})
        else:
            response['price'] = round(price,2)
            response['table_1'] = create_table(df)
            response['locations'] = latlong.values.tolist()
            return jsonify(response)
    
    return jsonify({'error':'Missing Data!'})
        
       
    

if __name__ == '__main__':
    server.title = "Vancouver Real Estate Analysis And Prediction"
    app.title = "Vancouver Real Estate Analysis And Prediction"
    app.run(port=5000, debug=True)