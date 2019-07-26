import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
#setup
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#flask
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return precipitation for given date"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).\
    group_by(Measurement.date).\
    all()

    # Convert list of tuples into normal list
    precip_list = list(np.ravel(results))

    return jsonify(precip_list)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    # Query all passengers
    results = session.query(Station.station).distinct().all()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(results))

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return tobs for given date"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.tobs).\
    group_by(Measurement.date).\
    all()

    # Convert list of tuples into normal list
    tobs_list = list(np.ravel(results))

    return jsonify(tobs_list)


if __name__ == '__main__':
    app.run(debug=True)