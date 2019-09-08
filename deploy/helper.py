from flask import Flask, request, jsonify, render_template
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import json
import pickle


from keras.models import load_model
 

def create_app():
    app = Flask(__name__)
    app = Flask(__name__,template_folder="templates")

    return app

def create_server(app):
    server = dash.Dash(__name__, server=app, url_base_pathname='/peek/')

    server.css.append_css({
        "external_url": "https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css"
    })

    server.css.append_css({
        "external_url": "/static/css/landing-page.min.css"
    })

    # Extra Dash styling.
    server.css.append_css({
        "external_url": 'https://codepen.io/chriddyp/pen/bWLwgP.css'
    })

    server.scripts.append_script({
            "external_url": "https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"
        })
    # Bootstrap Javascript.
    server.scripts.append_script({
        "external_url": "https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"
    })
    
    return server

def create_df():
    df = {}
    area = pd.read_csv('../data/Vancouver_Neigbourhood_Data.csv')
    prices = pd.read_csv('../data/Neigbourhood_2006_2019_Prices.csv')
    schools = pd.read_csv('../data/Neigbourhood_Schools_Ratings.csv')
    model_data = pd.read_csv('../data/Neighbourhood_model_data.csv')
    c_property = pd.read_csv('../data/Complete_tax_2006_2019_Data.csv')
    rew = pd.read_csv('../data/REW_dataset.csv')
    rew_clean = pd.read_csv('../data/clean_rew_data.csv')
    rew_clean.drop(['price', 'bed', 'bath', 'area_sqft', 'fireplaces'],axis=1,inplace=True)
    latlong = pd.read_csv('../data/rew_data/property_listing_latlong.csv')
    latlong.drop(['price', 'bed', 'bath', 'area_sqft', 'fireplaces'],axis=1,inplace=True)

    df['area']=area
    df['prices']=prices
    df['schools']=schools
    df['model_data']=model_data
    df['c_property']=c_property
    df['rew']=rew
    df['rew_clean']=rew_clean
    df['latlong']=latlong
    
    return df
    

def get_recommender():
    model = pickle.load(open('../data/knn_model.pkl','rb'))
    return model

def get_model():
    model = {}
    f1n = 'svr_f1.pkl' # # Try svr_f1_new.pkl if predict_price function fails
    f2n = 'gbr_f2.pkl'
    f3n = 'rfr_f3.pkl' # Try rfr_f3_new.pkl if predict_price function fails
    f4n = 'nn_f4.h5'
    finall = 'finalmodel.pkl'
    model['gbr'] = pickle.load(open('GBR.pkl','rb'))
    model['f1n'] = pickle.load(open(f1n, 'rb'))
    model['f2n'] = pickle.load(open(f2n, 'rb'))
    model['f3n'] = pickle.load(open(f3n, 'rb'))
    model['f4n'] = load_model(f4n)
    model['stackedmodel'] = pickle.load(open(finall, 'rb'))
    return model
    
def get_json():
    with open('../data/geo.json') as f:
        geo_json = json.load(f)
    return geo_json