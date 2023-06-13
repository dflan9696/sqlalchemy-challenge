# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model.
Base = automap_base()

# reflect the tables.
Base.prepare(autoload_with=engine)

# Save references to each table.
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB.
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def homepage():
    #List all available api routes.
    return (
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"/api/v1.0/<start><br/>"
        f"<br/>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Create our session (link) from Python to the DB.
    session = Session(engine)
    
    # Calculate the date one year from the last date in data set.
    year_last_date = dt.date(2017,8,23) - dt.timedelta(days = 365)
    
    # Perform a query to retrieve the data and precipitation scores.
    prcp_year = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year_last_date).all()
    
    # Close Session.
    session.close()
    
    # Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data)
    # to a dictionary using date as the key and prcp as the value.
    prcp_analysis = []
    for date, prcp in prcp_year:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_analysis.append(prcp_dict)
        
    return jsonify(prcp_analysis)

@app.route("/api/v1.0/stations")
def stations():
    
    # Create our session (link) from Python to the DB.
    session = Session(engine)
    
    # Preform a query to retrieve data for all stations.
    stations = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    
    # Close Session.
    session.close()
    
    # Create a dictionary from the data.
    station_analysis = []
    for station, name, latitude, longitude, elevation in stations:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Latitude"] = latitude
        station_dict["Longitude"] = longitude
        station_dict["Elevation"] = elevation
        station_analysis.append(station_dict)
        
    return jsonify(station_analysis)

@app.route("/api/v1.0/tobs")
def tobs():
    
    # Create our session (link) from Python to the DB.
    session = Session(engine)
    
    # Calculate the date one year from the last date in data set.
    year_last_date = dt.date(2017,8,23) - dt.timedelta(days = 365)
    
    # Query the dates and temperature observations of the most-active station for the previous year of data.
    most_active_station = session.query(measurement.date, measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= year_ago_date).all()
    
    # Close Session.
    session.close()
    
    ## Convert the query results from your tobs analysis (i.e. retrieve only the last 12 months of data)
    # to a dictionary using date as the key and temp as the value.
    most_active_analysis = []
    for date, temp in most_active_station:
        active_dict = {}
        active_dict[date] = temp
        most_active_analysis.append(active_dict)
        
    return jsonify(most_active_analysis)

@app.route("/api/v1.0/<start>")
def start(start):

    # Create our session (link) from Python to the DB.
    session = Session(engine)
    
    # Query the minimum, maximum, and average temperature for a specified start date of the dataset.
    start_results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start).all()
    
    # Close Session.
    session.close()
    
    # Create a dictionary from the data.
    start_date_analysis = []
    for min, max, avg in start_results:
        start_dict = {}
        start_dict["Min Temp"] = min
        start_dict["Max Temp"] = max
        start_dict["Avg Temp"] = avg
        start_date_analysis.append(start_dict)
        
    return jsonify(start_date_analysis)

@app.route("/api/v1.0/<start>/<end>")
def range_date(start,end):
    
    # Create our session (link) from Python to the DB.
    session = Session(engine)
    
    # Query the minimum, maximum, and average temperature for a specified start date and end date of the dataset.
    start_end_results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
    
    # Close Session.
    session.close()
    
    # Create a dictionary from the row data and append to list range_date.
    range_date_analysis = []
    for min, max, avg in start_end_results:
        range_dict = {}
        range_dict["Minimum Temperature"] = min
        range_dict["Maxium Temperature"] = max
        range_dict["Average Temperature"] = avg
        range_date_analysis.append(range_dict)
        
    return jsonify(range_date_analysis)
    
if __name__ == '__main__':
    app.run(debug=True)