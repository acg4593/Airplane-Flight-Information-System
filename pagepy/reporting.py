from flask import *
import pysqlite.SqliteApp as db
from extras import table_to_html
from datetime import datetime
import calendar

def reporting_route():
    navigation = request.args.get('navigation') or 'flight_roster'
    return render_template('reporting.html', navigation=navigation)

def get_roster_route():
    flight_number = request.args.get('flight_number')
    leg_number = request.args.get('leg_number')
    year = int(request.args.get('year') or datetime.now().year)
    month = int(request.args.get('month') or datetime.now().month)
    data = create_roster_calendar(flight_number, leg_number, year, month)
    return jsonify({'status': 'success', 'data': data})

def get_schedule_route():
    year = int(request.args.get('year') or datetime.now().year)
    month = int(request.args.get('month') or datetime.now().month)
    airline = request.args.get('airline')
    departure_city = request.args.get('departure_city')
    arrival_city = request.args.get('arrival_city')
    data = create_schedule_calendar(year, month, airline, departure_city, arrival_city)
    return jsonify({'status': 'success', 'data': data})

def get_report_route():
    year = int(request.args.get('year') or datetime.now().year)
    month = int(request.args.get('month') or datetime.now().month)
    airline = request.args.get('airline')
    data = create_report_calendar(year, month, airline)
    return jsonify({'status': 'success', 'data': data})

def create_schedule_calendar(year, month, airline, departure_city, arrival_city):
    print('[GET CALENDAR]', '{0}-{1}'.format(year, month))
    data = calendar.monthcalendar(year, month)
    html = '<div class="flightTable">'
    html += '<div class="tr">'
    for head in ['Mon', 'Tue', "Wed", 'Thu', 'Fri', 'Sat', 'Sun']:
        html += '<div class="th">{0}</div>'.format(head)
    html += '</div>'
    for week in data:
        html += '<div class="tr">'
        for day in week:
            if day == 0:
                html += '<div class="td"></div>'
            else:
                date = '{0}-{1}-{2}'.format(year,str(month).zfill(2), str(day).zfill(2))
                info = get_flight_for_date(airline, departure_city, arrival_city, date)
                html += '<div class="td"><div class="day">{0}</div>{1}</div>'.format(day, info)
        html += '</div>'
    html += '</div>'
    return html

def create_roster_calendar(flight_number, leg_number, year, month):
    print('[GET CALENDAR]', '{0}-{1}'.format(year, month))
    data = calendar.monthcalendar(year, month)
    html = '<div class="flightTable">'
    html += '<div class="tr">'
    for head in ['Mon', 'Tue', "Wed", 'Thu', 'Fri', 'Sat', 'Sun']:
        html += '<div class="th">{0}</div>'.format(head)
    html += '</div>'
    for week in data:
        html += '<div class="tr">'
        for day in week:
            if day == 0:
                html += '<div class="td"></div>'
            else:
                date = '{0}-{1}-{2}'.format(year,str(month).zfill(2), str(day).zfill(2))
                info = get_legs_for_date(flight_number, leg_number, date)
                html += '<div class="td"><div class="day">{0}</div>{1}</div>'.format(day, info)
        html += '</div>'
    html += '</div>'
    return html

def create_report_calendar(year, month,airline):
    print('[GET CALENDAR]', '{0}-{1}'.format(year, month))
    data = calendar.monthcalendar(year, month)
    html = '<div class="flightTable">'
    html += '<div class="tr">'
    for head in ['Mon', 'Tue', "Wed", 'Thu', 'Fri', 'Sat', 'Sun']:
        html += '<div class="th">{0}</div>'.format(head)
    html += '</div>'
    for week in data:
        html += '<div class="tr">'
        for day in week:
            if day == 0:
                html += '<div class="td"></div>'
            else:
                date = '{0}-{1}-{2}'.format(year,str(month).zfill(2), str(day).zfill(2))
                info = get_flight_report_for_date(airline, date)
                html += '<div class="td"><div class="day">{0}</div>{1}</div>'.format(day, info)
        html += '</div>'
    html += '</div>'
    return html

def get_flight_report_for_date(airline, date):
    db.update_flight_leg_data()
    response = db.query('''SELECT
        f.number as flight_number,
        fl.leg_number,
        li.leg_date, 
        f.airline,
        CASE WHEN fl.scheduled_arrival_time <= li.departure_time
            THEN 'On Time'
            ELSE 'Delayed'
        END as time_status
    FROM
        flight as f, flight_leg as fl, leg_instance as li
    WHERE
        CASE WHEN (:al  <> '') 
            THEN lower(f.airline) = lower(:al)
            ELSE lower(f.airline) <> lower(:al) 
        END AND
        f.number = fl.flight_number AND f.number = li.flight_number AND
        fl.leg_number = li.leg_number AND
        li.leg_date = :ld
        LIMIT 25''', {'al': airline, 'ld': date})
    airline = response.get_column('airline')
    flight_number = response.get_column('flight_number')
    leg_number = response.get_column('leg_number')
    leg_date = response.get_column('leg_date')
    time_status = response.get_column('time_status')
    html = '<div>'
    for i in range(len(flight_number)):
        stat_class = 'red' if time_status[i] == 'Delayed' else 'green'
        html += '<div class="leg">'
        html += '<div class="info">Airline: {0}</div>'.format(airline[i])
        html += '<div class="info">Flight Number: {0}</div>'.format(flight_number[i])
        html += '<div class="info">Leg Number: {0}</div>'.format(leg_number[i])
        html += '<div class="info">Leg Date: {0}</div>'.format(leg_date[i])
        html += '<div class="info {0}">STATUS: {1}</div>'.format(stat_class, time_status[i])
        html += '</div>'
    html += '</div>'
    return html


def get_flight_for_date(airline, departure_city, arrival_city, date):
    response = db.query('''SELECT 
        f.number as flight_number,
        fl.leg_number, 
        li.leg_date, 
        a0.city as departure_city, 
        a1.city as arrival_city,
        f.airline
    FROM 
        flight as f, flight_leg as fl, leg_instance as li, airport as a0, airport as a1
    WHERE
        CASE WHEN (:al  <> '') 
            THEN lower(f.airline) = lower(:al)
            ELSE lower(f.airline) <> lower(:al) 
        END AND
        CASE WHEN (:dc  <> '') 
            THEN lower(a0.city) = lower(:dc)
            ELSE lower(a0.city) <> lower(:dc) 
        END AND
        CASE WHEN (:ac  <> '') 
            THEN lower(a1.city) = lower(:ac)
            ELSE lower(a1.city) <> lower(:ac)
        END AND
        f.number = fl.flight_number AND f.number = li.flight_number AND
        fl.departure_airport_code = a0.airport_code AND fl.arrival_airport_code = a1.airport_code AND
        fl.leg_number = li.leg_number AND
        li.leg_date = :ld
        LIMIT 25''', {'al': airline, 'dc': departure_city, 'ac': arrival_city, 'ld': date});
    airline = response.get_column('airline')
    flight_number = response.get_column('flight_number')
    leg_number = response.get_column('leg_number')
    leg_date = response.get_column('leg_date')
    departure_city = response.get_column('departure_city')
    arrival_city = response.get_column('arrival_city')
    html = '<div>'
    for i in range(len(flight_number)):
        html += '<div class="leg">'
        html += '<div class="info">Airline: {0}</div>'.format(airline[i])
        html += '<div class="info">Flight Number: {0}</div>'.format(flight_number[i])
        html += '<div class="info">Leg Number: {0}</div>'.format(leg_number[i])
        html += '<div class="info">Leg Date: {0}</div>'.format(leg_date[i])
        html += '<div class="info">From City: {0}</div>'.format(departure_city[i])
        html += '<div class="info">To City: {0}</div>'.format(arrival_city[i])
        html += '</div>'
    html += '</div>'
    return html

def get_legs_for_date(flight_number, leg_number, date):
    response = db.get_calendar_flights(flight_number, leg_number, date, 25)
    flight_number = response.get_column('flight_number')
    leg_number = response.get_column('leg_number')
    leg_date = response.get_column('departure_date')
    departure_airport = response.get_column('departure_airport')
    arrival_airport = response.get_column('arrival_airport')
    html = '<div>'
    for i in range(len(flight_number)):
        html += '<div class="leg">'
        html += '<div class="info">Flight Number: {0}</div>'.format(flight_number[i])
        html += '<div class="info">Leg Number: {0}</div>'.format(leg_number[i])
        html += '<div class="info">Leg Date: {0}</div>'.format(leg_date[i])
        html += '<div class="info">From: {0}</div>'.format(departure_airport[i])
        html += '<div class="info">To: {0}</div>'.format(arrival_airport[i])
        html += '</div>'
    html += '</div>'
    return html