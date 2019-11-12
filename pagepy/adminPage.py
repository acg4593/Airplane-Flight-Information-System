from flask import render_template, request, redirect, url_for
from constants import keys
from datetime import datetime, time, date
import pysqlite.SqliteApp as db
from flask.json import jsonify
from extras import table_to_html

def adminRoute():
    if request.method == 'POST':
        print(request.form);
        if 'create_leg_instance' in request.form:
            create_leg_instance(request.form);

        elif 'create_flight_leg' in request.form:
            create_flight_leg(request.form);

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
    flight_id = form['flight_id'].split(':');
    airplane_id = form['airplane_id'];
    leg_date = form['leg_date'];
    departure_time = form['departure_time'];
    arrival_time = form['arrival_time']

    flight_legs = db.query("SELECT * FROM flight_leg where :fn = flight_number and :ln = leg_number", { "fn": flight_id[0], "ln": flight_id[1]});
    airplanes = db.query("SELECT * FROM airplane where :ai = airplane_id", {'ai': airplane_id});
    flight_leg = flight_legs.get_row(0);
    airplane = airplanes.get_row(0);
    db.create_leg_instance(flight_leg['flight_number'], flight_leg['leg_number'], leg_date, airplane['total_number_of_seats'], airplane_id, flight_leg['departure_airport_code'], departure_time, flight_leg['arrival_airport_code'], arrival_time);


def create_flight_leg(form):
    print('POST: Creating Flight Leg');
    flight_number = form['flight_number'];
    leg_number = form['leg_number'];
    departure_airport_code = form['departure_airport_code'];
    arrival_airport_code = form['arrival_airport_code'];
    db.insert_flight_leg(flight_number,leg_number,departure_airport_code,None,arrival_airport_code,None);

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
        airplane_data.append('With {0} seats on {1} ({2}) made by {3}'.format(
            max_seats[i], airplane_type[i], airplane_id[i] , company[i]
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
        airport_data.append('{0} - {1} ({2}, {3})'.format(airport_code[i], name[i], city[i], state[i]));
    return {'airport_code': airport_code, 'airport_data': airport_data }

def get_html_table(table, headers):
    return table_to_html(
        table=table, table_type="div", table_class="flightTable",
        table_header=headers, table_header_type="div", table_header_class="th",
        table_row_type='div', table_row_class='tr', table_data_type="div", table_data_class="td",
        custom_links_class="tr flightLink");

#Get Leg Instances based on flight_number
def leg_instance_update_get(flight_id):
    flight_leg = flight_id.split(':');
    query = db.query('SELECT * from leg_instance li where li.flight_number = :fn and li.leg_number = :ln order by li.leg_date', {
        'fn': flight_leg[0], 'ln': flight_leg[1]});
    return get_html_table(query.get_table(), query.get_headers());

def flight_leg_update_get(flight_number):
    flight_number = flight_number;
    query = db.query('SELECT * from flight_leg f where f.flight_number = :fn order by f.leg_number',{'fn': flight_number});
    return get_html_table(query.get_table(), query.get_headers());


def leg_instance_update_route():
    flight_id = request.args.get('flight_id');
    if not flight_id:
        return jsonify({'status': 'error'});
    return jsonify({'status': 'success', 'data': leg_instance_update_get(flight_id)});

def flight_leg_update_route():
    flight_number = request.args.get('flight_number');
    if not flight_number:
        return jsonify({'status': 'error'});
    return jsonify({'status': 'success', 'data': flight_leg_update_get(flight_number)});
