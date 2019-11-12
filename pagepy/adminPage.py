from flask import render_template, request, redirect, url_for
from constants import keys
from datetime import datetime, time, date
import pysqlite.SqliteApp as db

def adminRoute():
    if request.method == 'POST':
        print(request.form);
        if 'create_leg_instance' in request.form:
            create_leg_instance(request.form);

        elif 'create_flight_leg' in request.form:
            print('POST: Creating Flight Leg');

    leg_instance_flight_leg = get_leg_instance_flight_leg()
    leg_instance_airplane = get_leg_instance_airplane();
    flight_leg_flight = get_flight_leg_flight();
    flight_leg_airport = get_flight_leg_airport();
    
    key = request.args.get("key")
    if "key" in request.args:
        if key in keys:
            return render_template('adminMenu.html',
            leg_instance_len_flight_id= len(leg_instance_flight_leg['flight_id']), 
            leg_instance_flight_id= leg_instance_flight_leg['flight_id'],
            leg_instance_flight_leg_data=leg_instance_flight_leg['flight_leg_data'],
            leg_instance_len_airplanes=len(leg_instance_airplane['airplane_id']),
            leg_instance_airplane_id=leg_instance_airplane['airplane_id'],
            leg_instance_airplane_data=leg_instance_airplane['airplane_data'],
            flight_leg_len_flight=len(flight_leg_flight['flight_number']),
            flight_leg_flight_number=flight_leg_flight['flight_number'],
            flight_leg_flight_data=flight_leg_flight['flight_data'],
            flight_leg_leg_number=0,
            flight_leg_len_airport=len(flight_leg_airport['airport_code']),
            flight_leg_airport_code=flight_leg_airport['airport_code'],
            flight_leg_airport_data=flight_leg_airport['airport_data'],
            );
    return redirect(url_for('loadLogin'))



def create_leg_instance(form):
    print('POST: Creating Leg Instance');
    flight_id = request.form['flight_id'].split(':');
    airplane_id = request.form['airplane_id'];
    leg_date = request.form['leg_date'];
    
    departure_time = datetime.strptime('{0} {1}'.format(leg_date, request.form['departure_time']),  '%Y-%m-%d %H:%M');
    arrival_time = datetime.strptime('{0} {1}'.format(leg_date, request.form['arrival_time']),  '%Y-%m-%d %H:%M');

    flight_legs = db.query("SELECT * FROM flight_leg where :fn = flight_number and :ln = leg_number", { "fn": flight_id[0], "ln": flight_id[1]});
    airplanes = db.query("SELECT * FROM airplane where :ai = airplane_id", {'ai': airplane_id});
    flight_leg = flight_legs.get_row(0);
    airplane = airplanes.get_row(0);
    db.create_leg_instance(flight_leg['flight_number'], flight_leg['leg_number'], leg_date, airplane['total_number_of_seats'], airplane_id, flight_leg['departure_airport_code'], departure_time, flight_leg['arrival_airport_code'], arrival_time);


def get_leg_instance_flight_leg():
    db_flight_legs = db.query("SELECT fl.flight_number flight_number, fl.leg_number leg_number, a1.name departure_name, a1.city departure_city, a1.state departure_state, a2.name arrival_name, a2.city arrival_city, a2.state arrival_state from flight_leg fl, airport a1, airport a2 where fl.departure_airport_code = a1.airport_code and fl.arrival_airport_code = a2.airport_code");
    flight_number = db_flight_legs.get_column('flight_number');
    leg_number = db_flight_legs.get_column('leg_number')
    departure_name = db_flight_legs.get_column('departure_name');
    departure_city = db_flight_legs.get_column('departure_city');
    departure_state = db_flight_legs.get_column('departure_state');
    arrival_name = db_flight_legs.get_column('arrival_name');
    arrival_city = db_flight_legs.get_column('arrival_city');
    arrival_state = db_flight_legs.get_column('arrival_state');
    flight_id = []
    for i in range(len(db_flight_legs)):
        flight_id.append('{0}:{1}'.format(flight_number[i], leg_number[i]))
    flight_leg_data = []
    for i in range(len(db_flight_legs)):
        flight_leg_data.append('From {0} ({1}, {2}) to {3} ({4}, {5}) on Flight ({6} leg {7})'.format(
            departure_name[i], departure_city[i], departure_state[i],
            arrival_name[i], arrival_city[i], arrival_state[i],
            flight_number[i], leg_number[i]
        ));
    return {'flight_id': flight_id, 'flight_leg_data': flight_leg_data};

def get_leg_instance_airplane():
    db_airplanes = db.query('SELECT a.airplane_id airplane_id, a.airplane_type airplane_type, t.max_seats max_seats, t.company company from airplane a, airplane_type t where a.airplane_type = t.type_name');
    airplane_id = db_airplanes.get_column('airplane_id');
    airplane_type = db_airplanes.get_column('airplane_type');
    max_seats = db_airplanes.get_column('max_seats');
    company = db_airplanes.get_column('company');
    airplane_data = []
    for i in range(len(db_airplanes)):
        airplane_data.append('With {0} seats on {1} made by {2}'.format(
            max_seats[i], airplane_type[i], company[i]
        ));
    return {'airplane_id': airplane_id,'airplane_data': airplane_data};

def get_flight_leg_flight():
    db_flight = db.query('SELECT number flight_number, airline airline from flight');
    flight_number = db_flight.get_column('flight_number');
    airline = db_flight.get_column('airline');
    flight_data = []
    for i in range(len(flight_number)):
        flight_data.append('{0} - {1}'.format(flight_number[i], airline[i]));
    return {'flight_data': flight_data, 'flight_number': flight_number}

def get_flight_leg_airport():
    db_airport = db.query('SELECT airport_code airport_code, name name, city city, state state FROM airport');
    airport_code = db_airport.get_column('airport_code');
    name = db_airport.get_column('name');
    city = db_airport.get_column('city');
    state = db_airport.get_column('state');
    airport_data = []
    for i in range(len(airport_code)):
        airport_data.append('{0} ({1}, {2})'.format(name[i], city[i], state[i]));
    return {'airport_code': airport_code, 'airport_data': airport_data }


