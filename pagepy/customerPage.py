from flask import render_template, request, redirect, url_for
import pysqlite.SqliteApp as db;
from extras import table_to_html
from flask.json import jsonify
from reserve import *
import json

def customer_route():
    title = db.query("SELECT date('now', 'localtime') as d").get_column('d')[0]
    return render_template("/customer.html", title=title)

def customer_select_route():
    flight_number = request.args.get("flight_number")
    leg_number = request.args.get("leg_number")
    seat_date = request.args.get("seat_date")
    title = '{0}:{1}:{2}'.format(flight_number, leg_number, seat_date)

    response = db.query("SELECT * FROM seat_reservation where flight_number = :fn AND leg_number=:ln AND seat_date=:sd AND customer_phone IS NULL AND customer_name IS NULL",
    {'fn': flight_number, 'ln': leg_number, 'sd': seat_date});
    response.remove_column('customer_name')
    response.remove_column('customer_phone')
    seat_date = seat_table(response)

    response = db.query("SELECT * FROM fares WHERE flight_number=:fn", {'fn': flight_number})
    fare_data = fare_table(response)

    return render_template("/customer_select.html", title=title , seatData=seat_date, fareData=fare_data)

def customer_reservation_route():
    confirm = request.args.get('confirmation')
    customer_name = request.args.get('customer_name')
    customer_phone = request.args.get('customer_phone')
    customer = customer_name is not None and customer_phone is not None
    if customer:
        if confirm is not None:
            content = update_seat_reservations(customer_name, customer_phone)
            return render_template('/reservation.html', confirmation=True, content=content)
        else:
            reservations = get_reservations(customer_name,customer_phone)
            return render_template('/reservation.html', customer_name=customer_name, customer_phone=customer_phone, customer=customer, reservations=reservations)

    return render_template('/reservation.html')

def customer_reservation_cancel_route():
    customer_name = request.args.get('customer_name')
    customer_phone = request.args.get('customer_phone')
    customer = customer_name is not None and customer_phone is not None

    if customer:
        response = db.query('SELECT * FROM seat_reservation WHERE customer_name=:cn AND customer_phone=:cp',
        {'cn': customer_name, 'cp': customer_phone});
        data = get_html_table('seat_reservation', response.get_table(), response.get_headers(), 
        ['flight_number', 'leg_number', 'seat_date', 'seat_number']);
        return render_template('/reservation_cancel.html', customer=customer, reservationData=data)

    return render_template('/reservation_cancel.html', customer=customer)

def customer_cancel_reservation_for_route():
    nan = request.args.get('data')
    data = json.loads(nan);
    flight_number = data['flight_number']
    leg_number = data['leg_number']
    seat_date = data['seat_date']
    seat_number = data['seat_number']
    if flight_number is None or leg_number is None or seat_date is None or seat_number is None:
        return jsonify({'status': 'failure'})
    db.update_seat_reservation(flight_number, leg_number, seat_date, seat_number, None, None);
    return jsonify({'status': 'success'})


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
            html += '''<div class="td"><button onclick="cancel_reservation(this)" data='{0}'>Cancel Reservation</button></div>'''.format(data);
        html += '</div>';
    html += '</div>';
    return html;
#END HTML TABLE HELPER

def update_seat_reservations(customer_name, customer_phone):
    key = customer_name + ':' + customer_phone
    if key not in reservations:
        return '<div class="message">There are no Reservations to Confirm!</div>'
    reserves = reservations[key].values()
    for reserve in reserves:
        leg_id = reserve['leg_id']
        seat_number = reserve['seat_number']
        fare_code = reserve['fare_code']
        flight_number, leg_number, leg_date = leg_id.split(':', 2)
        print('[CONFIRM RESERVATION]','{0}, {1}, {2}, {3}'.format(flight_number, leg_number, leg_date, seat_number))
        result = db.query('SELECT customer_name, customer_phone FROM seat_reservation WHERE flight_number=:fn AND leg_number=:ln AND seat_date=:sd AND seat_number=:sn', 
        {'fn': flight_number, 'ln': leg_number, 'sd': leg_date, 'sn': seat_number });
        if result.get_column('customer_name')[0] is None or result.get_column('customer_phone')[0] is None:
            print('[CONFIRM RESERVATION]', 'successfully executed!')
            db.update_seat_transaction(flight_number,leg_number,leg_date, seat_number, fare_code,customer_name,customer_phone);
        else:
            print('[CONFIRM RESERVATION]', 'failed successfully!')
            return '<div class="message">Could not Reserve One of the seats!</div>'
    del reservations[key];
    return '<div class="message">All Reservations have been Confirmed!</div>'

def get_reservations(customer_name, customer_phone):
    key = customer_name + ':' + customer_phone
    headers = ['Flight Number', 'Leg Number', 'Leg Date', 'Seat Number', 'Fare Cost']
    if key not in reservations:
        return '<div class="message">There are no Reservations with the input credentials!</div>'
    reserves = reservations[key].values()
    html = '<div class="flightTable">'
    html += "<div class='tr'>"
    for header in headers:
        html += "<div class='th'>{0}</div>".format(header)
    html += "</div>"
    for reserve in reserves:
        leg_id = reserve['leg_id']
        seat_number = reserve['seat_number']
        fare_code = reserve['fare_code']
        flight_number, leg_number, leg_date = leg_id.split(':', 2)
        response = db.query('SELECT amount FROM fares WHERE flight_number=:fn AND fare_code=:fc', {'fn': flight_number, 'fc': fare_code})
        fare_cost = response.get_column('amount')[0]
        html += "<div class='tr'>"
        for val in [flight_number, leg_number, leg_date, seat_number, fare_cost]:
            html += "<div class='td'>{0}</div>".format(val)
        html += "</div>"
    html += '</div>'
    return html

def seat_table(response):
    seat_number = response.get_column('seat_number')
    html = "<div class='flightTable'>"
    html += "<div class='tr'>"
    for header in response.get_headers():
        html += "<div class='th'>{0}</div>".format(header.replace('_', ' '))
    html += "</div>"
    for j in range(len(response.get_table())):
        html += "<div><input id='{0}' class='radio_seat' type='radio' name='seat_number' value={0} required>".format(seat_number[j])
        html += "<label for='{0}' class='tr tr-{1}'>".format(seat_number[j], j % 2)
        for i in response.get_table()[j]:
            html += "<div class='td'>{0}</div>".format(i)
        html += "</label></div>"
    html += "</div>"
    return html

def fare_table(response):
    fare_code = response.get_column('fare_code')
    amount = response.get_column('amount')
    restrictions = response.get_column('restrictions')
    html = '<div class="fares">'
    for j in range(len(response.get_table())):
        html += "<div><input id='{0}' class='radio_fare' type='radio' name='fare_code' value={0} required>".format(fare_code[j])
        html += "<label for='{0}' class='fare'>".format(fare_code[j])
        html += 'Amount: ${0} with Restrictions: {1}'.format(amount[j],restrictions[j] if restrictions[j] else 'None')
        html += "</label></div>"
    html += "</div>"
    return html

def get_available_flight_with_args(from_city_or_airport, to_city_or_airport, date):
    return db.query('''SELECT * FROM get_available_flights WHERE 
    (CASE WHEN (:dd <> '') THEN (departure_date = :dd) ELSE (departure_date <> :dd) END)
    AND  (CASE WHEN (:fcoa  <> '') THEN (departure_city = :fcoa OR departure_airport = :fcoa) ELSE (departure_city <> :fcoa) END)
    AND (CASE WHEN (:tcoa <> '') THEN (arrival_city = :tcoa OR arrival_airport = :tcoa) ELSE (arrival_city <> :tcoa) END)''',
    {'fcoa': from_city_or_airport, 'tcoa': to_city_or_airport, 'dd': date});

def customer_search_route():
    from_city_or_airport = request.args['from'];
    to_city_or_airport = request.args['to'];
    departure_date = request.args['depart'];
    print('[ROUTE CUSTOMER SEARCH]', 'args:', from_city_or_airport, to_city_or_airport, departure_date);
    response = get_available_flight_with_args(from_city_or_airport,to_city_or_airport,departure_date);
    
    flight_number = response.remove_column('flight_number');
    leg_number = response.remove_column('leg_number');
    seat_date = response.get_column('departure_date');
    custom_links_href = [];
    for i in range(len(flight_number)):
        custom_links_href.append("/customer/select?flight_number={0}&leg_number={1}&seat_date={2}".format(flight_number[i],leg_number[i],seat_date[i]));

    data = table_to_html(
        table=response.get_table(),
        table_type="div",
        table_class="flightTable",
        table_header=response.get_headers(),
        table_header_type="div",
        table_header_class="th",
        table_row_type='div',
        table_row_class='tr',
        table_data_type="div",
        table_data_class="td",
        custom_links_href=custom_links_href,
        custom_links_class="tr flightLink");

    return jsonify({'status': 'success', 'data': data});

def post_reservation():
    try:
        leg_id = request.args.get('leg_id')
        seat_number = request.args.get("seat_number")
        customer_name = request.args.get('customer_name')
        customer_phone = request.args.get("customer_phone")
        fare_code = request.args.get("fare_code")
        create_reservation(leg_id, fare_code, seat_number, customer_name, customer_phone);
        return jsonify({'status': 'success'})
    except:
        return jsonify({'status': 'failure'})
