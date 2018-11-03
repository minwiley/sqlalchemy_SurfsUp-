# Step 2 - Climate App
# Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.
# Use FLASK to create your routes.

# Dependencies
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import create_engine, func, inspect, desc

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# R&R dates 11/1/18-11/15/18 - 15 days
inspector = inspect(engine) 
inspector.get_table_names()
inspector = inspect(engine)
columns = inspector.get_columns('station')
for c in columns:
	print(c['name'], c['type'])

inspector = inspect(engine)
columns = inspector.get_columns('measurement')
for c in columns:
	print(c['name'], c['type'])

 # Query All Records in the the Database
data_station = engine.execute("SELECT * FROM station")

for record_stat in data_station:
	print(record_stat)

 # Query All Records in the the Database
data_measurement = engine.execute("SELECT * FROM measurement LIMIT 25")

for record_measure in data_measurement:
	print(record_measure)

app = Flask(__name__)

@app.route("/")
def home():
	print("Server received request for 'Home' page.")
	return (
		f'Now entering the Surfs Up Weather API!<br/><br/>'
		f'Available Endpoints<br/><br/>'
		f'/api/v1.0/precipitation '
		f'<a href="/api/v1.0/precipitation">/api/v1.0/precipitation<a/><br/><br/>'

		f'/api/v1.0/stations '
		f'<a href="/api/v1.0/stations">/api/v1.0/stations<a/><br/><br/>'

		f'/api/v1.0/tobs '
		f'<a href="/api/v1.0/tobs">/api/v1.0/tobs<a/><br/><br/>'

		f'/api/v1.0/<start> '
		f'<a href="/api/v1.0/<start>">/api/v1.0/<start><a/><br/><br/>'

		f'/api/v1.0/<start>/<end> '
		f'<a href="/api/v1.0/<start>/<end>">/api/v1.0/<start>/<end><a/>'
		)
	
# Routes

# /api/v1.0/precipitation
# Convert the query results to a Dictionary using date as the key and prcp as the value.Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
	results_dacp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-24").\
	group_by(Measurement.date).all()
	precip_list = [results_dacp]
	return jsonify(precip_list)

# /api/v1.0/stations
# Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
	station_list = session.query(Measurement.station).all()
	station_lists = list(np.ravel(station_list))
	return jsonify(station_lists)

# /api/v1.0/tobs
# query for the dates and temperature observations from a year from the last data point. Return a JSON list of Temperature Observations (tobs) for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():
	results_tob = session.query(Measurement.tobs).filter(Measurement.date >= "2016-08-24").all()
	tobs_list = [results_tob]
	return jsonify(tobs_list)

# /api/v1.0/<start> and /api/v1.0/<start>/<end>
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range. When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive. 

@app.route('/api/v1.0/<start>', methods=["GET"])

def start_stats(start=None):

	results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
	filter(Measurement.date >= start).all()

	weather_stats = []

	for Tmin, Tmax, Tavg in results:

		weather_stats_dict = {}
		weather_stats_dict["Minimum Temperature"] = Tmin
		weather_stats_dict["Maximum Temperature"] = Tmax
		weather_stats_dict["Average Temperature"] = Tavg
		weather_stats.append(weather_stats_dict)

	return jsonify(weather_stats)
	
@app.route("/api/v1.0/<start>/<end>", methods=["GET"])

def calc_stats(start=None, end=None):

	results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
	filter(Measurement.date >= start).filter(Measurement.date <= end).all()

	start_end = []

	for Tmin, Tmax, Tavg in results:

		start_end_dict = {}
		start_end_dict["Minimum Temperature"] = Tmin
		start_end_dict["Maximum Temperature"] = Tmax
		start_end_dict["Average Temperature"] = Tavg

		start_end.append(start_end)
	
	return jsonify(start_end)



if __name__ == "__main__":
	app.run(debug=True)