############################
# import dependencies
############################

import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

############################
# database setup
############################

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)


############################
# create references to Measurement and Station tables
############################

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

###########################
# initialize Flask app
###########################

app = Flask(__name__)

###########################
# initalize Flask routes
###########################

@app.route("/")

def home():
	"""List of all returnable API routes."""
	
	return(
		f"Welcome to the Hawaii weather API!<br/>"
		f"Available Routes: <br/>"
		
		f"/api/v1.0/precipitation<br/>"
		f"Returns a JSON representation of dates and precipitation.<br/><br/>"
		
		f"/api/v1.0/stations<br/>"
		f"Returns a JSON list of weather stations in Hawaii.<br/><br/>"
		
		f"/api/v1.0/tobs<br/>"
		f"Returns dates and temperature observations for the last year of data.<br/><br/>"
		
		f"/api.v1.0/<start><br/>"
		f"Returns a JSON list of the minumum, average and max temperatures after a given date.<br/><br/>"
		
		f"/api.v1.0/<start>/<end><br/>"
		f"Returns a JSON list of the minimum, average and max temperatures between a specified date range.<br/><br/>"
     )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return Dates and Temps from the past year of data"""
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > 2016-08-22.all()
    
    # create JSONified list
    precipitation_list = [results]
    
    return jsonify(precipitation_list)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation)
    
    #create a JSONified list of dicts
    
    station_list = []
    for result in results:
        row = {}
        row['station'] = result[0]
        row['name'] = result[1]
        row['latitude'] = result[2]
        row['longitude'] = result[3]
        row['elevation'] = result[4]
        station_list.append(row)
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temp_obs():
    """Return a list of temperature observations for the previous year"""
    results = session.query(Station.name, Measurement.date, Measurement.tobs).\
    filter(Measurement.date > "2016-08-22").all()
    
    # create a JSONified list of dictionaries for results
    tobs_list = []
    for result in results:
        row = {}
        row["station"] = result [0]
        row["date"] = result[1]
        row["temperature"] = int(result[2])
        tobs_list.append(row)
        
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>/")
def start_date(date):
    """Return the min, max and average temp for all dates after start date"""
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date > date).all()
    
    # create JSONified list of dictionaries
    data_list = []
    for result in results:
        row = {}
        row["Start Date"] = date
        row["Minimum Temperature"] = result[0]
        row["Maximum Temperature"] = result[1]
        row["Average Temperature"] = result[2]
        data_list.append(row)
        
    return jsonify(data_list)

@app.route("/api/v1.0/<start>/<end>")
def query_dates(start_date, end_date):
    """Return the min, max and average temp for all dates in a given date range"""
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
    
    # create JSONified list of dicts
    data_list = []
    for result in results:
        row = {}
        row["Start Date"] = start_date
        row["End Date"] = end_date
        row["Minimum Temperature"] = result[0]
        row["Maximum Temperature"] = result[1]
        row["Average Temperature"] = result[2]
        data_list.append(row)
        
    return jsonify(data_list)
    
if __name__ == '__main__':
    app.run(debug=True)
    

		