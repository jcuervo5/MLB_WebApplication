# import necessary libraries
from models import create_classes
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
from flask import after_this_request
import pandas as pd
from bs4 import BeautifulSoup
import requests
from flask_cors import CORS

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
CORS(app, supports_credentials=True)
#################################################
# Database Setup
#################################################

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Andrew8270@localhost:5432/Project_2'

# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class statcast_ids(db.Model):
    player_id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(50))
    first_name = db.Column(db.String(50))

class player_demos(db.Model):
    birthyear = db.Column(db.Integer)
    birthcountry = db.Column(db.String(120))
    birthstate = db.Column(db.String(120))
    birthcity = db.Column(db.String(120))
    first_name = db.Column(db.String(120), primary_key=True)
    last_name = db.Column(db.String(120), primary_key=True)
    weight = db.Column(db.Integer)
    height = db.Column(db.Integer)
    bats = db.Column(db.String(120))
    throws = db.Column(db.String(120))


# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index2.html")


@app.route("/scrape",methods=['POST','GET'])
def scrape_data():
    db.engine.dispose()
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    req = request.get_json()
    first_name = req['first_name']
    last_name = req['last_name']

    first_name = first_name.title()
    last_name = last_name.title()

    demographics = db.session.query(player_demos.birthyear,player_demos.birthcountry,player_demos.birthstate,
    player_demos.birthcity,player_demos.first_name,player_demos.last_name,player_demos.weight,player_demos.height,
    player_demos.bats,player_demos.throws).\
        filter(player_demos.first_name == first_name).\
        filter(player_demos.last_name == last_name).\
        filter(player_demos.birthyear >= 1980).one()

    player_id = db.session.query(statcast_ids.player_id).\
        filter(statcast_ids.first_name == first_name).\
        filter(statcast_ids.last_name == last_name).one().player_id

    stat_tables = pd.read_html(f'https://baseballsavant.mlb.com/savant-player/{first_name}-{last_name}-{player_id}')
    statcast_tables = pd.read_html(f'https://baseballsavant.mlb.com/savant-player/{first_name}-{last_name}-{player_id}', match = 'Pitches')
    
    statcast = statcast_tables[0].to_json()
    stats = stat_tables[0].to_json()

    meta_dict = {'demo':demographics, 'statcast':statcast, 'stats':stats}
    
    # return jsonify(demographics),jsonify(statcast),jsonify(stats)

    return jsonify(meta_dict)
    


if __name__ == "__main__":
    app.run()
