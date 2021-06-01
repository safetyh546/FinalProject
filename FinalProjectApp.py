#################################################
# import dependencies
#################################################

from matplotlib import style
import matplotlib.pyplot as plt
from pandas import DataFrame
import pandas as pd
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc, distinct
from flask import Flask, jsonify, render_template
from config import password

#################################################
# Database Setup
#################################################
# create engine 
engine = create_engine(f'postgresql://postgres:{password}@localhost:5432/flight_db')
connection = engine.connect()

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
flight = Base.classes.flight
#top_tags = Base.classes.top_tags

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route("/Flights/<Year>")
#return a list of dictionaries with Borough name and Sale Count
def Flights(Year):
    session = Session(engine)
    FlightCount = session.query(flight.op_carrier_airline,func.count(flight.flightid),func.sum(flight.arr_del15)).filter(flight.year == Year).filter(flight.cancelled == 0).filter(flight.diverted == 0).group_by(flight.op_carrier_airline).order_by(desc(func.count(flight.flightid))).all()
    Flight_Dict_list = []
    for b,ct,s in FlightCount:
        FlightDict = {}
        FlightDict["Airline"] = b
        FlightDict["FlightCount"] = ct
        FlightDict["PercentDelayed"] = round(float(s/ct)*100,2)
        Flight_Dict_list.append(FlightDict)
    session.close()  
    return jsonify(Flight_Dict_list)




if __name__ == "__main__":
    app.run(debug=True)        