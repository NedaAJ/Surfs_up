import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#Set up Database
# engine=create_engine("sqlite:///hawaii.sqlite", connect_args={"check_same_thread": False})
engine=create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

#Set up Flask
app = Flask(__name__)

#Setting up the welcome route
@app.route("/")
def welcome():
    session = Session(engine)
    return(
    '''
    <xmp>
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    </xmp>
    ''')

#Setting up the Precipitation route
@app.route('/api/v1.0/precipitation') 

def precipitation():
    session = Session(engine)
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    session.close
    return jsonify(precip)

#Setting up the Stations route
@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    session.close
    return jsonify(stations=stations)

#Setting up the Tobs route
@app.route('/api/v1.0/tobs')
def  temp_monthly():
    session = Session(engine)
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >=prev_year).all()
    temps = list(np.ravel(results))
    session.close
    return jsonify(temps=temps)

#Setting up Statics Route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    session = Session(engine)
    sel=[func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify (temps = temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    session.close
    return jsonify(temps = temps)

if __name__ == "__main__":
    app.run(debug=True)