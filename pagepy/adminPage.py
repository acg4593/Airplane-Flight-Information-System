from flask import request, render_template, redirect, url_for
from constants import keys
from datetime import datetime, time, date
import pysqlite.SqliteApp as db
from flask.json import jsonify
from extras import table_to_html
import json;

def admin_get_route():
    print('[ROUTE]', 'admin_get_route()');
    flight_leg = get_selection_flight_leg()
    airplane = get_selection_airplane();
    flight = get_selection_flight();
    airport = get_selection_airport();
    airplane_type = get_selection_airplane_type();
    if "key" in request.args:
        key = request.args['key']
        if key in keys:
            return render_template('adminMenu.html',
            flight_leg= flight_leg, 
            airplane=airplane,
            flight=flight,
            airport=airport,
            airplane_type=airplane_type
            );
    return redirect(url_for('loadLogin'))

def admin_update_route():
    print('[ROUTE]', 'admin_update_route()');
    if 'type' in request.args:
        type = request.args['type'];
        if 'leg_instance' == type:
            return jsonify({'status': 'success', 'data': leg_instance_update_get(request.args['flight_id'])});
        elif 'flight_leg' == type:
            return jsonify({'status': 'success', 'data': flight_leg_update_get(request.args['flight_number'])});
        elif 'flight' == type:
            return jsonify({'status': 'success', 'data': flight_update_get()});
        elif 'airport' == type:
            return jsonify({'status': 'success', 'data': airport_update_get()});
        elif 'fares' == type:
            return jsonify({'status': 'success', 'data': fares_update_get(request.args['flight_number'])});
        elif 'airplane_type' == type:
            return jsonify({'status': 'success', 'data': airplane_type_update_get()});
        elif 'can_land' == type:
            return jsonify({'status': 'success', 'data': can_land_update_get()});
        elif 'airplane' == type:
            return jsonify({'status': 'success', 'data': airplane_update_get()});
        elif 'seat_reservation' == type:
            return jsonify({'status': 'success', 'data': seat_reservation_update_get()});
    return jsonify({'status': 'failure'});

def admin_submit_route():
    print('[ROUTE]', 'admin_submit_route()');
    if 'type' in request.args:
        type = request.args['type'];
        if 'leg_instance' == type:
            return create_leg_instance();
        elif 'flight_leg' == type:
            return create_flight_leg();
        elif 'flight' == type:
            return create_flight();
        elif 'airport' == type:
            return create_airport();
        elif 'fares' == type:
            return create_fares();
        elif 'airplane_type' == type:
            return create_airplane_type();
        elif 'can_land' == type:
            return create_can_land();
        elif 'airplane' == type:
            return create_airplane();
    return jsonify({'status': 'failure'});

def admin_select_route():
    print('[ROUTE]', 'admin_select_route()');
    if 'type' in request.args:
        type = request.args['type'];
        if 'flight_leg' == type:
            return jsonify({'status': 'success', 'data': get_selection_flight_leg()});
        elif 'airplane' == type:
            return jsonify({'status': 'success', 'data': get_selection_airplane()});
        elif 'flight' == type:
            return jsonify({'status': 'success', 'data': get_selection_flight()});
        elif 'airport' == type:
            return jsonify({'status': 'success', 'data': get_selection_airport()});
        elif 'airplane_type' == type:
            return jsonify({'status': 'success', 'data': get_selection_airplane_type()});

    return jsonify({'status': 'failure'});

#START CREATE HELPERS
def create_leg_instance():
    print('[ADMIN MODIFY]','leg_instance');
    flight_id = request.args['flight_id'].split(':');
    airplane_id = request.args['airplane_id'];
    leg_date = request.args['leg_date'];
    departure_time = datetime.strptime(request.args['departure_time'], '%Y-%m-%dT%H:%M');
    arrival_time = datetime.strptime(request.args['arrival_time'], '%Y-%m-%dT%H:%M');

    flight_legs = db.query("SELECT * FROM flight_leg where :fn = flight_number and :ln = leg_number", { "fn": flight_id[0], "ln": flight_id[1]});
    airplanes = db.query("SELECT * FROM airplane where :ai = airplane_id", {'ai': airplane_id});
    flight_leg = flight_legs.get_row(0);
    airplane = airplanes.get_row(0);

    if(db.leg_instance_exists(flight_leg['flight_number'], flight_leg['leg_number'], leg_date)):
        db.update_leg_instance(flight_leg['flight_number'], flight_leg['leg_number'], leg_date, airplane['total_number_of_seats'], airplane_id, departure_time, arrival_time)
        return jsonify({'status': 'success', 'command': 'updated'})
    else:
        db.create_leg_instance(flight_leg['flight_number'], flight_leg['leg_number'], leg_date, airplane['total_number_of_seats'], airplane_id, flight_leg['departure_airport_code'], departure_time, flight_leg['arrival_airport_code'], arrival_time);
        return jsonify({'status': 'success', 'command': 'created'})

def create_flight_leg():
    print('[ADMIN MODIFY]','flight_leg');
    flight_number = request.args['flight_number'];
    leg_number = request.args['leg_number'];
    departure_airport_code = request.args['departure_airport_code'];
    arrival_airport_code = request.args['arrival_airport_code'];
    if db.flight_leg_exists(flight_number, leg_number):
        db.update_flight_leg(flight_number,leg_number,departure_airport_code,arrival_airport_code);
        return jsonify({'status': 'success', 'command': 'updated'});
    else:
        db.insert_flight_leg(flight_number,leg_number,departure_airport_code,None,arrival_airport_code,None);
        return jsonify({'status': 'success', 'command': 'created'});

def create_flight():
    print('[ADMIN MODIFY]','flight');
    number = request.args['number'];
    airline = request.args['airline'];
    weekdays = request.args['weekdays'];
    if db.flight_exists(number):
        db.update_flight(number, airline, weekdays);
        return jsonify({'status': 'success', 'command': 'updated'});
    else:
        db.insert_flight(number,airline,weekdays);
        return jsonify({'status': 'success', 'command': 'created'});

def create_airport():
    print('[ADMIN MODIFY]','airport');
    airport_code = request.args['airport_code'];
    name = request.args['name'];
    city = request.args['city'];
    state = request.args['state'];
    if db.airport_exists(airport_code):
        db.update_airport(airport_code, name, city, state);
        return jsonify({'status': 'success', 'command': 'updated'});
    else:
        db.insert_airport(airport_code,name,city,state);
        return jsonify({'status': 'success', 'command': 'created'});

def create_fares():
    print('[ADMIN MODIFY]','fares');
    flight_number = request.args['flight_number'];
    fare_code = request.args['fare_code'];
    amount = request.args['amount'];
    restrictions = request.args['restrictions'];
    if db.fares_exists(flight_number,fare_code):
        db.update_fares(flight_number,fare_code,amount,restrictions);
        return jsonify({'status': 'success', 'command': 'updated'});
    else:
        db.insert_fares(flight_number,fare_code,amount,restrictions);
        return jsonify({'status': 'success', 'command': 'created'});

def create_airplane_type():
    print('[ADMIN MODIFY]','airplane_type');
    type_name = request.args['type_name'];
    max_seats = request.args['max_seats'];
    company = request.args['company'];
    if db.airplane_type_exists(type_name):
        db.update_airplane_type(type_name, max_seats, company);
        return jsonify({'status': 'success', 'command': 'updated'});
    else:
        db.insert_airplane_type(type_name, max_seats, company);
        return jsonify({'status': 'success', 'command': 'created'});

def create_can_land():
    print('[ADMIN MODIFY]','can_land');
    airplane_type_name = request.args['airplane_type_name'];
    airport_code = request.args['airport_code'];
    db.insert_can_land(airplane_type_name,airport_code);
    return jsonify({'status': 'success'})

def create_airplane():
    print('[ADMIN MODIFY]','airplane');
    airplane_id = request.args['airplane_id'];
    type_name = request.args['type_name']
    airplane_types = db.query('SELECT * FROM airplane_type where type_name = :tn', {'tn': type_name});
    airplane_type = airplane_types.get_row(0);
    if db.airplane_exists(airplane_id):
        db.update_airplane(airplane_id, airplane_type['max_seats'], type_name);
        return jsonify({'status': 'success', 'command': 'updated'});
    else:
        db.insert_airplane(airplane_id, airplane_type['max_seats'], type_name);
        return jsonify({'status': 'success', 'command': 'created'});
#END CREATE HELPERS

#START SELECTION HELPERS

def get_selection_flight_leg():
    print('[ADMIN GET]','flight_leg');
    flight_leg = get_leg_instance_flight_leg();
    flight_id = flight_leg['flight_id'];
    flight_data = flight_leg['flight_leg_data'];
    html = ''
    for i in range(len(flight_id)):
        html += '<option value="{0}">{1}</option>'.format(flight_id[i], flight_data[i]);
    return html;

def get_selection_airplane():
    print('[ADMIN GET]','airplane');
    airplane = get_leg_instance_airplane();
    airplane_id = airplane['airplane_id'];
    airplane_data = airplane['airplane_data'];
    html = ''
    for i in range(len(airplane_id)):
        html += '<option value="{0}">{1}</option>'.format(airplane_id[i], airplane_data[i]);
    return html;

def get_selection_flight():
    print('[ADMIN GET]','flight');
    flight = get_flight_leg_flight();
    flight_number = flight['flight_number']
    flight_data = flight['flight_data']
    html = ''
    for i in range(len(flight_number)):
        html += '<option value="{0}">{1}</option>'.format(flight_number[i], flight_data[i]);
    return html;

def get_selection_airport():
    print('[ADMIN GET]','airport');
    airport = get_flight_leg_airport();
    airport_code = airport['airport_code'];
    airport_data = airport['airport_data'];
    html = ''
    for i in range(len(airport_code)):
        html += '<option value="{0}">{1}</option>'.format(airport_code[i], airport_data[i]);
    return html;

def get_selection_airplane_type():
    print('[ADMIN GET]','airplane_type');
    airplane_type = get_airplane_type_name();
    type_name = airplane_type['type_name']
    type_data = airplane_type['type_data']
    html = ''
    for i in range(len(type_name)):
        html += '<option value="{0}">{1}</option>'.format(type_name[i], type_data[i]);
    return html;

#END SELECTION HELPERS

#START GET HELPERS
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

def get_airplane_type_name():
    query = db.query('SELECT type_name, max_seats, company FROM airplane_type');
    type_name = query.get_column('type_name');
    max_seats = query.get_column('max_seats');
    company = query.get_column('company');
    type_data = []
    for i in range(len(type_name)):
        type_data.append('{0} made by {1} with {2} seats'.format(type_name[i], company[i], max_seats[i]));
    return { 'type_name': type_name, 'type_data': type_data };

#END GET HELPERS

#START HTML TABLE HELPER
def get_html_table(type, table, headers, primarykeys, deletable=True):
    html = '<div class="flightTable">';
    html += '<div class="tr">';
    for header in headers:
        html += '<div class="th">{0}</div>'.format(header.replace('_', ' '));
    if deletable:
        html += '<div class="th">Commands</div>';
    html += '</div>';
    for j in range(len(table)):
        html += '<div class="tr">'
        if deletable:
            data = '{' + '"type":"{0}"'.format(type);
        for i in range(len(table[j])):
            td = table[j][i]
            if headers[i] in primarykeys:
                if deletable:
                    data += ',"{0}":"{1}"'.format(headers[i], td);
            html += '<div class="td">{0}</div>'.format(td);
        if deletable:
            data += '}'
            html += '''<div class="td"><button onclick="delete_row_item(this)" data='{0}'>Delete</button></div>'''.format(data);
        html += '</div>';
    html += '</div>';
    return html;
#END HTML TABLE HELPER

#START GET QUERIES
def leg_instance_update_get(flight_id):
    print('[ADMIN UPDATE GET]','leg_instance');
    flight_leg = flight_id.split(':') if flight_id != 'undefined' else ['',''];
    query = db.query('SELECT * from leg_instance li where li.flight_number = :fn and li.leg_number = :ln order by li.leg_date', {
        'fn': flight_leg[0], 'ln': flight_leg[1]});
    return get_html_table('leg_instance', query.get_table(), query.get_headers(), ['flight_number', 'leg_number', 'leg_date']);

def flight_leg_update_get(flight_number):
    print('[ADMIN UPDATE GET]','flight_leg');
    query = db.query('SELECT * from flight_leg f where f.flight_number = :fn order by f.leg_number',{'fn': flight_number});
    return get_html_table('flight_leg', query.get_table(), query.get_headers(), ['flight_number', 'leg_number']);

def flight_update_get():
    print('[ADMIN UPDATE GET]','flight');
    query = db.query('SELECT * from flight');
    return get_html_table('flight', query.get_table(), query.get_headers(), ['number']);

def airport_update_get():
    print('[ADMIN UPDATE GET]','airport');
    query = db.query('SELECT * from airport');
    return get_html_table('airport', query.get_table(), query.get_headers(), ['airport_code']);

def fares_update_get(number):
    print('[ADMIN UPDATE GET]','fares');
    query = db.query('SELECT * from fares where flight_number = :fn', {'fn': number});
    return get_html_table('fares', query.get_table(), query.get_headers(), ['flight_number', 'fare_code']);

def airplane_type_update_get():
    print('[ADMIN UPDATE GET]','airplane_type');
    query = db.query('SELECT * from airplane_type');
    return get_html_table('airplane_type', query.get_table(), query.get_headers(), ['type_name']);

def can_land_update_get():
    print('[ADMIN UPDATE GET]','can_land');
    query = db.query('SELECT * from can_land');
    return get_html_table('can_land', query.get_table(), query.get_headers(), ['airplane_type_name', 'airport_code']);

def airplane_update_get():
    print('[ADMIN UPDATE GET]','airplane');
    query = db.query('SELECT * from airplane');
    return get_html_table('airplane', query.get_table(), query.get_headers(), ['airplane_id']);

def seat_reservation_update_get():
    print('[ADMIN UPDATE GET]','seat_reservation');
    query = db.query('SELECT * from seat_reservation LIMIT 100');
    return get_html_table('seat_reservation', query.get_table(), query.get_headers(), ['flight_number', 'leg_number','seat_date', 'seat_number'], False);

#END GET QUERIES

#START DELETE ROUTING
def delete_item_route():
    nan = request.args.get('data');
    data = json.loads(nan);
    data_type = data['type'];

    if data_type == 'leg_instance':
        print('[ADMIN DELETE]','flight_number: {0}, leg_number: {1}, leg_date: {2}'.format( data['flight_number'], data['leg_number'], data['leg_date']));
        db.delete_leg_instance(data['flight_number'], data['leg_number'], data['leg_date'])
        return jsonify({'status': 'success'});
    elif data_type == 'flight_leg':
        print('[ADMIN DELETE]','flight_number: {0}, leg_number: {1}'.format(data['flight_number'], data['leg_number']));
        db.delete_flight_leg(data['flight_number'], data['leg_number']);
        return jsonify({'status': 'success'});
    elif data_type == 'flight':
        print('[ADMIN DELETE]','flight: {0}'.format(data['number']));
        db.delete_flight(data['number']);
        return jsonify({'status': 'success'});
    elif data_type == 'airport':
        print('[ADMIN DELETE]','airport_code: {0}'.format(data['airport_code']));
        db.delete_airport(data['airport_code']);
        return jsonify({'status': 'success'});
    elif data_type == 'fares':
        print('[ADMIN DELETE]','flight_number: {0}, fare_code: {1}'.format(data['flight_number'], data['fare_code']));
        db.delete_fares(data['flight_number'], data['fare_code']);
        return jsonify({'status': 'success'});
    elif data_type == 'airplane_type':
        print('[ADMIN DELETE]','type_name: {0}'.format(data['type_name']));
        db.delete_airplane_type(data['type_name']);
        return jsonify({'status': 'success'});
    elif data_type == 'can_land':
        print('[ADMIN DELETE]','airplane_type_name: {0}, airport_code: {1}'.format(data['airplane_type_name'], data['airport_code']));
        db.delete_can_land(data['airplane_type_name'], data['airport_code']);
        return jsonify({'status': 'success'});
    elif data_type == 'airplane':
        print('[ADMIN DELETE]','airplane_id: {0}'.format(data['airplane_id']));
        db.delete_airplane(data['airplane_id']);
        return jsonify({'status': 'success'});

    return jsonify({'status': 'error'});
#END DELETE ROUTING