import datetime as dt
import numpy as np
import pandas as pd

# import dependencies and import flask, jsonify  dependencies

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Create an engine for the hawaii.sqlite database
engine = create_engine("sqlite:///hawaii.sqlite", echo =False)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the Hawaii_Stations and Hawaii_Measurements tables
Station = Base.classes.Hawaii_Stations
Measurement = Base.classes.Hawaii_Measurements

# Create our session (link) from Python to the DB
session = Session(engine)


# Flask Setup

app = Flask(__name__)

# set up object for Flask for future references


# route takes you to certain endpoints in the URL. where data can be accessed.

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Avalable Routes:<br/><br/>"
		
        f"/api/v1.0/precipitation"
		f" - Precipitation query for the last year<br/><br/>"
		

        f"/api/v1.0/stations"
        f" - List of stations from the dataset<br/><br/>"
		

        f"/api/v1.0/tobs"
        f" - List of Temperature Observations (tobs) for the previous year<br/><br/>"
		

        f"/api/v1.0/<start>"
        f" - Enter Start Date in YYYY-MM-DD format. Calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.<br/><br/>"
		

        f"/api/v1.0/<start>/<end>"
        f" - Enter Start and End Date in YYYY-MM-DD formatCalculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive<br/><br/>"
		
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    """Return a list of all precipitation from the last year"""
    # Query all dates and prcp from the Measurement table filtered by last year of data
    results = session.query(Measurement.date, Measurement.prcp).\
	filter(Measurement.date.between('2016-08-23','2017-08-23')).all()

    # Convert list of tuples into normal list
    # variable = list(np.ravel(query variable))
    
    prcp_list = list(np.ravel(results))

    return jsonify(prcp_list)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list stations"""
    # Query all stations from the stations table
    results = session.query(Station.station,Station.name).all()

    station_list = list(np.ravel(results))

    return jsonify(station_list)
	
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list tobs from the last year"""
    # Query all dates and prcp from the Measurement table filtered by last year of data
    results = session.query(Measurement.date, Measurement.prcp).\
	filter(Measurement.date.between('2016-08-23','2017-08-23')).all()

    # Convert list of tuples into normal list
    # variable = list(np.ravel(query variable))
    
    tobs_list = list(np.ravel(results))

    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
def start(start='2016-08-23'):

	""" start defaults to 1 year range
    Return a min, max, and average temps from start date to last day of date 2017-08-23 inputed."""
	
	# query to get temp min, max, average for date range
	results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date.between(start,'2017-08-23')).all()
	# Convert list of tuples into normal list
	sdate_list = list(np.ravel(results))
	return jsonify(sdate_list)
    

@app.route("/api/v1.0/<sdate>,<edate>")
def startrange(sdate='2016-08-23',edate='2017-08-23'):

	""" start defaults to 1 year range
    Return a min, max, and average temps from start date to last day of date 2017-08-23 inputed."""
	
	# query to get temp min, max, average for date range
	results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date.between(sdate,edate)).all()
	# Convert list of tuples into normal list
	sdate_list = list(np.ravel(results))
	return jsonify(sdate_list)
	


# this last bit of code allows you to run the python script through the terminal
if __name__ == '__main__':
    app.run()
