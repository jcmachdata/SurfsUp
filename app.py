from flask import Flask, jsonify
import sqlalchemy
##from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)


@app.route("/")
def welcome():
    return ("Welcome to my Hawaii weather app! <br/>"
        f"Test Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"api/v1.0/stations<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
            )
  

@app.route("/api/v1.0/precipitation")
def precipitation():
    precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').all()
    precip_dict = dict(precip)
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    stationlist = session.query(Measurement.station).all()
    return jsonify(stationlist)

@app.route("/api/v1.0/tobs")
def temperature():
    temp = session.query(Measurement.tobs).filter(Measurement.station == "USC00519281", Measurement.date >= '2016-08-23').all()
    return jsonify(temp)

@app.route("/api/v1.0/<start>")
def temperaturestart(start):
    tempstart = session.query(Measurement.tobs).filter(Measurement.station == "USC00519281", Measurement.date >= start).all()
    return jsonify(tempstart)

@app.route("/api/v1.0/<start>/<end>")
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    startend = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    return jsonify(startend)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
