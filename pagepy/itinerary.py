from flask import render_template, request
import pysqlite.SqliteApp as db

def itinerary_route():
    customer_name = request.args.get('customer_name')
    customer_phone = request.args.get('customer_phone')
    date = get_date()
    customer = customer_name is not None and customer_phone is not None

    return render_template('itinerary.html', 
    customer=customer, date=date, 
    customer_name=customer_name, customer_phone=customer_phone, 
    flight_data=get_traveler_information(customer_name,customer_phone), 
    price_data=get_price_summary(customer_name,customer_phone));

def get_itinerary(customer_name, customer_phone):
    html = ''

    seat_reservation = db.query('SELECT flight_number, leg_number, seat_date, seat_number FROM seat_reservation WHERE customer_name=:cn AND customer_phone=:cp', 
    {'cn': customer_name, 'cp': customer_phone});


    return ''

def get_traveler_information(customer_name, customer_phone):
    seat_reservation = db.query('SELECT flight_number, leg_number, seat_date, seat_number FROM seat_reservation WHERE customer_name=:cn AND customer_phone=:cp', 
    {'cn': customer_name, 'cp': customer_phone});

    flight_number = seat_reservation.get_column('flight_number');
    leg_number = seat_reservation.get_column('leg_number');
    seat_date = seat_reservation.get_column('seat_date');
    seat_number = seat_reservation.get_column('seat_number');
    restrictions = []
    departure_time = []
    arrival_time = []
    travel_time = []
    from_city = []
    from_state = []
    from_airport = []
    to_airport = []
    to_city = []
    to_state = []
    for i in range(len(flight_number)):
        result = db.query('''SELECT 
        l.departure_time as departure_time, l.arrival_time as arrival_time, 
        a0.city as from_city, a0.state as from_state, a0.name as from_airport,
        a1.city as to_city, a1.state as to_state, a1.name as to_airport,
        ROUND((julianday(l.arrival_time) - julianday(l.departure_time)) * 24, 2) as travel_time
        FROM leg_instance as l, airport as a0, airport as a1 
        WHERE l.flight_number=:fn AND l.leg_number=:ln AND l.leg_date=:ld AND l.departure_airport_code=a0.airport_code AND l.arrival_airport_code=a1.airport_code''',
        {'fn': flight_number[i], 'ln':leg_number[i], 'ld': seat_date[i]});
        departure_time.append(result.get_column('departure_time')[0]);
        arrival_time.append(result.get_column('arrival_time')[0]);
        travel_time.append(result.get_column('travel_time')[0])

        from_city.append(result.get_column('from_city')[0]);
        from_state.append(result.get_column('from_state')[0]);
        from_airport.append(result.get_column('from_airport')[0]);

        to_airport.append(result.get_column('to_airport')[0]);
        to_city.append(result.get_column('to_city')[0]);
        to_state.append(result.get_column('to_state')[0]);

        result = db.query('''SELECT f.restrictions as restrictions FROM seat_fares as s, fares as f 
        WHERE s.flight_number=:fn AND s.leg_number=:ln AND s.seat_date=:sd AND  s.seat_number=:sn AND s.flight_number=f.flight_number AND f.fare_code=s.fare_code''',
        {'fn': flight_number[i], 'ln': leg_number[i], 'sd': seat_date[i], 'sn': seat_number[i]});

        restrictions.append(result.get_column('restrictions')[0])

    html = ''
    for i in range(len(flight_number)):
        html += '<div class="trip_content">'
        html += "<div class='trip_head'>"
        html += "{0} -> {1}".format(from_airport[i], to_airport[i])
        html += "</div><div class='trip_body'>"
        html += "<div class='trip_row'><div class='trip_key'>{0}, {1}</div><div class='trip_value'>Departure Time: {2}</div></div>".format(from_city[i], from_state[i], departure_time[i]);
        html += "<div class='trip_row'><div class='trip_key'>{0}, {1}</div><div class='trip_value'>Arrival Time: {2}</div></div>".format(to_city[i], to_state[i], arrival_time[i]);
        html += "<div class='trip_row'><div class='trip_key'>Seat #{0}</div><div class='trip_value'>Travel Time: {1} hours</div></div>".format(seat_number[i], travel_time[i]);
        html += "<div class='trip_row'>Restrictions: {0}</div>".format(restrictions[i]);
        html += '</div></div>'

    return html

def get_price_summary(customer_name, customer_phone):
    seat_reservation = db.query('SELECT flight_number, leg_number, seat_date, seat_number FROM seat_reservation WHERE customer_name=:cn AND customer_phone=:cp', 
    {'cn': customer_name, 'cp': customer_phone});

    flight_number = seat_reservation.get_column('flight_number');
    leg_number = seat_reservation.get_column('leg_number');
    seat_date = seat_reservation.get_column('seat_date');
    seat_number = seat_reservation.get_column('seat_number');
    amount = []
    total = 0
    for i in range(len(flight_number)):
        result = db.query('''SELECT f.amount as amount FROM seat_fares as s, fares as f 
        WHERE s.flight_number=:fn AND s.leg_number=:ln AND s.seat_date=:sd AND  s.seat_number=:sn AND s.flight_number=f.flight_number AND f.fare_code=s.fare_code''',
        {'fn': flight_number[i], 'ln': leg_number[i], 'sd': seat_date[i], 'sn': seat_number[i]});
        a = result.get_column('amount')[0];
        amount.append(a);
        total += int(a)

    html = '<div class="price_content">'
    for i in range(len(flight_number)):
        html += '<div class="price_row">'
        html += '<div class="price_key">Flight {0}</div><div class="price_value">${1}</div>'.format(flight_number[i], amount[i])
        html += '</div>'
    html += '<div class="price_row">'
    html += '<div class="price_key">Total:</div><div class="price_value">${0}</div>'.format(total)
    html += '</div>'
    html += '</div>'
    return html

def get_date():
    result = db.query("SELECT datetime('now', 'localtime') current_date");
    return result.get_column('current_date')[0]