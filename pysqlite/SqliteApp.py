import sqlite3
from flask import request
from pysqlite.SqlResponse import SqlResponse, sql_response_from_cursor
from extras import table_to_html
from constants import flight_leg_timer_check

#START QUERY HELPERS
def query(query, paramaters={}):
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute(query, paramaters)
        return sql_response_from_cursor(c)

def call(query, paramaters={}):
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute(query, paramaters)

def get_all_flights():
    print('[QUERY]', 'get_all_flights()')
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute("SELECT * FROM leg_instance")
        print('[QUERY]', 'get_all_flights()', "Executed Successfully!");
        return sql_response_from_cursor(c)

def get_available_flights(limitCount=100):
    print('[QUERY]', 'get_available_flights()')
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute("SELECT * FROM get_available_flights LIMIT :lc", {'lc':limitCount});
        print('[QUERY]', 'get_available_flights()', "Executed Successfully!");
        return sql_response_from_cursor(c)

def get_calendar_flights(flight_number, leg_number, leg_date, limitCount=100):
    print('[GETTING DATE]', leg_date)
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute("""SELECT * 
            FROM get_available_flights  WHERE
            CASE WHEN (:fn  <> '') 
                THEN flight_number = :fn
                ELSE flight_number <> :fn 
            END AND
            CASE WHEN (:ln  <> '') 
                THEN leg_number = :ln
                ELSE leg_number <> :ln 
            END AND
            CASE WHEN (:dd  <> '') 
                THEN departure_date = :dd
                ELSE departure_date <> :dd 
            END LIMIT :lc""", 
        {'fn': flight_number, 'ln': leg_number, 'dd': leg_date, 'lc':limitCount});
        print('[QUERY]', 'get_available_flights()', "Executed Successfully!");
        return sql_response_from_cursor(c)

def update_flight_leg_data():
    if flight_leg_timer_check() is False:
        return;
    print('[QUERY]', 'update_flight_leg_data()')
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON')
        c.execute('BEGIN')

        c.execute('SELECT * FROM get_earliest_leg_instance')
        response = sql_response_from_cursor(c)
        flight_number = response.get_column('flight_number')
        leg_number = response.get_column('leg_number')
        departure_time = response.get_column('departure_time')
        arrival_time = response.get_column('arrival_time')

        for i in range(len(flight_number)):
            c.execute('''UPDATE flight_leg
            SET scheduled_departure_time = :dt,
                scheduled_arrival_time = :at
            WHERE
                flight_number = :fn AND leg_number = :ln;''', 
            {'fn': flight_number[i], 'ln': leg_number[i], 'dt': departure_time[i], 'at': arrival_time[i]})
        
        c.execute('COMMIT')


#END QUERY HELPERS

#START CREATE HERLPERS
def create_leg_instance(flight_number, leg_number, leg_date, number_of_available_seats, 
airplane_id, departure_airport_code, departure_time, arrival_airport_code, arrival_time):
    print('[QUERY CREATE]', 'create_leg_instance()')
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('SELECT a.total_number_of_seats from airplane as a where a.airplane_id=:ai', {"ai": airplane_id})
        num_of_seats = c.fetchone()[0] or 0;
        c.execute('BEGIN')
        print('[TRANSACTION]', 'Begin Transaction...')
        c.execute("INSERT INTO leg_instance VALUES (:fn, :ln, :ld, :noas, :ai, :dac, :dt, :aac, :at)",
        {"fn": flight_number, "ln": leg_number, "ld": leg_date, "noas": number_of_available_seats, 
        "ai": airplane_id, "dac": departure_airport_code, "dt": departure_time, 
        "aac": arrival_airport_code, "at": arrival_time})
        for seat_number in range(num_of_seats):
            c.execute("INSERT INTO seat_reservation VALUES (:fn, :ln, :sd, :sn, :cn, :cp)",
            {"fn": flight_number, "ln": leg_number, "sd": leg_date
            , "sn": seat_number, "cn": None, "cp": None})
        c.execute("COMMIT")
        print('[TRANSACTION]', 'Transaction Complete!')
        print('[QUERY CREATE]', 'create_leg_instance()', 'Executed Successfully!')

def update_seat_transaction(flight_number,leg_number,leg_date, seat_number, fare_code, customer_name,customer_phone):
    print('[QUERY CREATE]', 'update_seat_transaction()')
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('BEGIN')
        print('[TRANSACTION]', 'Begin Transaction...')
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('''UPDATE seat_reservation
        SET customer_name = :cn, customer_phone = :cp
        WHERE flight_number = :fn AND leg_number = :ln AND seat_date = :sd AND seat_number=:sn''',
        {"fn": flight_number, "ln": leg_number, "sd": leg_date, 'sn': seat_number, "cn": customer_name, "cp": customer_phone});

        c.execute("INSERT INTO seat_fares VALUES (:fn, :ln, :sd, :sn, :fc)",
        {"fn": flight_number, "ln": leg_number, "sd": leg_date
        , "sn": seat_number, "fc": fare_code});
        c.execute("COMMIT")
        print('[TRANSACTION]', 'Transaction Complete!')
        print('[QUERY CREATE]', 'update_seat_transaction()', 'Executed Successfully!')

#END CREATE HELPERS

#START INSERTS
def insert_airport(airport_code, name, city, state):
    print('[QUERY INSERT]', 'insert_airport()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute("INSERT INTO airport VALUES (:ac, :n, :c, :s)", 
        {"ac": airport_code, "n": name, "c": city, "s": state})
        print('[QUERY INSERT]', 'insert_airport()', 'Executed Successfully!');

def insert_flight(number, airline, weekdays):
    print('[QUERY INSERT]', 'insert_flight()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute("INSERT INTO flight VALUES (:n, :a, :w)",
        {"n": number, "a": airline, "w": weekdays})
        print('[QUERY INSERT]', 'insert_flight()', 'Executed Successfully!');


def insert_flight_leg(flight_number, leg_number, departure_airport_code, 
scheduled_departure_time, arrival_airport_code, scheduled_arrival_time):
    print('[QUERY INSERT]', 'insert_flight_leg()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor();
        c.execute("INSERT INTO flight_leg VALUES (:fn, :ln, :dac, :sdt, :aac, :sat)",
        {"fn": flight_number, "ln": leg_number, "dac": departure_airport_code
        , "sdt": scheduled_departure_time, "aac": arrival_airport_code, "sat": scheduled_arrival_time})
        print('[QUERY INSERT]', 'insert_flight_leg()', 'Executed Successfully!');


def insert_leg_instance(flight_number, leg_number, leg_date, number_of_available_seats, 
airplane_id, departure_airport_code, departure_time, arrival_airport_code, arrival_time):
    print('[QUERY INSERT]', 'insert_leg_instance()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute("INSERT INTO leg_instance VALUES (:fn, :ln, :ld, :noas, :ai, :dac, :dt, :aac, :at)",
        {"fn": flight_number, "ln": leg_number, "ld": leg_date, "noas": number_of_available_seats, 
        "ai": airplane_id, "dac": departure_airport_code, "dt": departure_time, 
        "aac": arrival_airport_code, "at": arrival_time})
        print('[QUERY INSERT]', 'insert_leg_instance()', 'Executed Successfully!');


def insert_fares(flight_number, fare_code, amount, restrictions):
    print('[QUERY INSERT]', 'insert_fares()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute("INSERT INTO fares VALUES (:fn, :fc, :a, :r)",
        {"fn": flight_number, "fc": fare_code, "a": amount, "r": restrictions})
        print('[QUERY INSERT]', 'insert_fares()', 'Executed Successfully!');


def insert_airplane_type(type_name, max_seats, company):
    print('[QUERY INSERT]', 'insert_airplane_type()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute("INSERT INTO airplane_type VALUES (:tn, :ms, :c)",
        {"tn": type_name, "ms": max_seats, "c": company})
        print('[QUERY INSERT]', 'insert_airplane_type()', 'Executed Successfully!');


def insert_can_land(airplane_type_name, airport_code):
    print('[QUERY INSERT]', 'insert_can_land()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute("INSERT INTO can_land VALUES (:atn, :ac)",
        {"atn": airplane_type_name, "ac": airport_code})
        print('[QUERY INSERT]', 'insert_can_land()', 'Executed Successfully!');


def insert_airplane(airplane_id, total_number_of_seats, airplane_type):
    print('[QUERY INSERT]', 'insert_airplane()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute("INSERT INTO airplane VALUES (:ai, :tnos, :at)",
        {"ai": airplane_id, "tnos": total_number_of_seats, "at": airplane_type})
        print('[QUERY INSERT]', 'insert_airplane()', 'Executed Successfully!');


def insert_seat_reservation(flight_number, leg_number, seat_date, seat_number, customer_name, customer_phone):
    print('[QUERY INSERT]', 'insert_seat_reservation()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute("INSERT INTO seat_reservation VALUES (:fn, :ln, :sd, :sn, :cn, :cp)",
        {"fn": flight_number, "ln": leg_number, "sd": seat_date
        , "sn": seat_number, "cn": customer_name, "cp": customer_phone});
        print('[QUERY INSERT]', 'insert_seat_reservation()', 'Executed Successfully!');

def insert_seat_fares(flight_number, leg_number, seat_date, seat_number, fare_code):
    print('[QUERY INSERT]', 'insert_seat_fares()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute("INSERT INTO seat_fares VALUES (:fn, :ln, :sd, :sn, :fc)",
        {"fn": flight_number, "ln": leg_number, "sd": seat_date, "sn": seat_number, "fc": fare_code});
        print('[QUERY INSERT]', 'insert_seat_fares()', 'Executed Successfully!');


#END INSERTS

#START DELETES
def delete_leg_instance(flight_number, leg_number, leg_date):
    print('[QUERY DELETE]', 'delete_leg_instance()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor();
        c.execute('PRAGMA foreign_keys = ON');
        c.execute("DELETE FROM leg_instance WHERE flight_number = :fn and leg_number = :ln and leg_date = :ld", {'fn': flight_number, 'ln': leg_number, 'ld': leg_date});
        print('[QUERY DELETE]', 'delete_leg_instance()', 'Executed Successfully!');

def delete_flight_leg(flight_number, leg_number):
    print('[QUERY DELETE]', 'delete_flight_leg()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor();
        c.execute('PRAGMA foreign_keys = ON');
        c.execute("DELETE FROM flight_leg WHERE flight_number = :fn and leg_number = :ln", {'fn': flight_number, 'ln': leg_number});
        print('[QUERY DELETE]', 'delete_flight_leg()', 'Executed Successfully!');

def delete_flight(number):
    print('[QUERY DELETE]', 'delete_flight()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor();
        c.execute('PRAGMA foreign_keys = ON');
        c.execute("DELETE FROM flight WHERE number = :n", {'n': number});
        print('[QUERY DELETE]', 'delete_flight()', 'Executed Successfully!');

def delete_airport(airport_code):
    print('[QUERY DELETE]', 'delete_airport()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor();
        c.execute('PRAGMA foreign_keys = ON');
        c.execute("DELETE FROM airport WHERE airport_code = :ac", {'ac': airport_code});
        print('[QUERY DELETE]', 'delete_airport()', 'Executed Successfully!');

def delete_fares(flight_number, fare_code):
    print('[QUERY DELETE]', 'delete_fares()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor();
        c.execute('PRAGMA foreign_keys = ON');
        c.execute("DELETE FROM fares WHERE flight_number = :fn and fare_code = :fc", {'fn': flight_number, 'fc': fare_code});
        print('[QUERY DELETE]', 'delete_fares()', 'Executed Successfully!');

def delete_airplane_type(type_name):
    print('[QUERY DELETE]', 'delete_airplane_type()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor();
        c.execute("DELETE FROM airplane_type WHERE type_name = :tn", {'tn': type_name});
        print('[QUERY DELETE]', 'delete_airplane_type()', 'Executed Successfully!');

def delete_can_land(airplane_type_name, airport_code):
    print('[QUERY DELETE]', 'delete_can_land()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor();
        c.execute('PRAGMA foreign_keys = ON');
        c.execute("DELETE FROM can_land WHERE airplane_type_name = :atn and airport_code = :ac", {'atn': airplane_type_name, 'ac': airport_code});
        print('[QUERY DELETE]', 'delete_can_land()', 'Executed Successfully!');

def delete_airplane(airplane_id):
    print('[QUERY DELETE]', 'delete_airplane()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor();
        c.execute('PRAGMA foreign_keys = ON');
        c.execute("DELETE FROM airplane WHERE airplane_id = :ai", {'ai': airplane_id});
        print('[QUERY DELETE]', 'delete_airplane()', 'Executed Successfully!');
#END DELETES

#START EXISTS



#END EXISTS

#START UPDATES

def update_leg_instance(flight_number, leg_number, leg_date, number_of_available_seats,
airplane_id, departure_time, arrival_time):
    print('[QUERY UPDATE]', 'update_leg_instance()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('''UPDATE leg_instance 
        SET airplane_id=:ai, departure_time=:dt, arrival_time=:at, number_of_available_seats=:noas
        WHERE flight_number=:fn and leg_number=:ln and leg_date=:ld''', 
        {"fn": flight_number, "ln": leg_number, "ld": leg_date, 'noas': number_of_available_seats, 
        "ai": airplane_id, "dt": departure_time, "at": arrival_time});
        print('[QUERY UPDATE]', 'update_leg_instance()', 'Executed Successfully!');

def update_airport(airport_code, name, city, state):
    print('[QUERY UPDATE]', 'update_airport()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('''UPDATE airport 
        SET name=:n, city=:c, state=:s 
        WHERE airport_code = :ac''',  
        {"ac": airport_code, "n": name, "c": city, "s": state});
        print('[QUERY UPDATE]', 'update_airport()', 'Executed Successfully!');

def update_flight(number, airline, weekdays):
    print('[QUERY UPDATE]', 'update_flight()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('''UPDATE flight 
        SET airline=:a, weekdays=:w 
        WHERE number = :n''', 
        {"n": number, "a": airline, "w": weekdays});
        print('[QUERY UPDATE]', 'update_flight()', 'Executed Successfully!');

def update_flight_leg(flight_number, leg_number, departure_airport_code, arrival_airport_code):
    print('[QUERY UPDATE]', 'update_flight_leg()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor();
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('''UPDATE flight_leg 
        SET departure_airport_code=:dac, arrival_airport_code=:aac 
        WHERE flight_number = :fn AND leg_number = :ln''',
        {"fn": flight_number, "ln": leg_number, "dac": departure_airport_code, "aac": arrival_airport_code});
        print('[QUERY UPDATE]', 'update_flight_leg()', 'Executed Successfully!');

def update_fares(flight_number, fare_code, amount, restrictions):
    print('[QUERY UPDATE]', 'update_fares()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('''UPDATE fares
        SET amount=:a, restrictions=:r
        WHERE flight_number = :fn AND fare_code = :fc''', 
        {"fn": flight_number, "fc": fare_code, "a": amount, "r": restrictions});
        print('[QUERY UPDATE]', 'update_fares()', 'Executed Successfully!');

def update_airplane_type(type_name, max_seats, company):
    print('[QUERY UPDATE]', 'update_airplane_type()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('''UPDATE airplane_type
        SET max_seats=:ms, company=:c
        WHERE type_name = :tn''',
        {"tn": type_name, "ms": max_seats, "c": company});
        print('[QUERY UPDATE]', 'update_airplane_type()', 'Executed Successfully!');

def update_airplane(airplane_id, total_number_of_seats, airplane_type):
    print('[QUERY UPDATE]', 'update_airplane()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('''UPDATE airplane
        SET total_number_of_seats = :tnos, airplane_type = :at
        WHERE airplane_id = :ai''',
        {"ai": airplane_id, "tnos": total_number_of_seats, "at": airplane_type});
        print('[QUERY UPDATE]', 'update_airplane()', 'Executed Successfully!');

def update_seat_reservation(flight_number, leg_number, seat_date, seat_number, customer_name, customer_phone):
    print('[QUERY UPDATE]', 'update_seat_reservation()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('''UPDATE seat_reservation
        SET customer_name = :cn, customer_phone = :cp
        WHERE flight_number = :fn AND leg_number = :ln AND seat_date = :sd AND seat_number=:sn''',
        {"fn": flight_number, "ln": leg_number, "sd": seat_date, 'sn': seat_number, "cn": customer_name, "cp": customer_phone});
        print('[QUERY UPDATE]', 'update_seat_reservation()', 'Executed Successfully!');

#END UPDATES

#START EXIST CHECKS
def leg_instance_exists(flight_number, leg_number, leg_date):
    print('[QUERY CHECK]', 'leg_instance_exists()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('SELECT * FROM leg_instance WHERE flight_number=:fl and leg_number=:ln and leg_date=:ld',
        {'fl': flight_number, 'ln': leg_number, 'ld': leg_date});
        print('[QUERY CHECK]', 'leg_instance_exists()', 'Complete!');
        return c.fetchone() != None

def airport_exists(airport_code):
    print('[QUERY CHECK]', 'airport_exists()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('SELECT * FROM airport WHERE airport_code=:ac', {'ac': airport_code});
        print('[QUERY CHECK]', 'airport_exists()', 'Complete!');
        return c.fetchone() != None;

def flight_exists(number):
    print('[QUERY CHECK]', 'flight_exists()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('SELECT * FROM flight WHERE number=:n', {'n': number});
        print('[QUERY CHECK]', 'flight_exists()', 'Complete!');
        return c.fetchone() != None;

def flight_leg_exists(flight_number, leg_number):
    print('[QUERY CHECK]', 'flight_leg_exists()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor();
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('SELECT * FROM flight_leg WHERE flight_number=:fn AND leg_number=:ln',
        {"fn": flight_number, "ln": leg_number});
        print('[QUERY CHECK]', 'flight_leg_exists()', 'Complete!');
        return c.fetchone() != None;

def fares_exists(flight_number, fare_code):
    print('[QUERY CHECK]', 'fares_exists()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('SELECT * FROM fares WHERE flight_number=:fn AND fare_code=:fc',
        {"fn": flight_number, "fc": fare_code});
        print('[QUERY CHECK]', 'fares_exists()', 'Complete!');
        return c.fetchone() != None;

def airplane_type_exists(type_name):
    print('[QUERY CHECK]', 'airplane_type_exists()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('SELECT * FROM airplane_type WHERE type_name=:tn', {'tn': type_name});
        print('[QUERY CHECK]', 'airplane_type_exists()', 'Complete!');
        return c.fetchone() != None;

def airplane_exists(airplane_id):
    print('[QUERY CHECK]', 'airplane_exists()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('SELECT * FROM airplane WHERE airplane_id=:ai', {"ai": airplane_id})
        print('[QUERY CHECK]', 'airplane_exists()', 'Complete!');
        return c.fetchone() != None;

def seat_reservation_exists(flight_number, leg_number, seat_date, customer_name, customer_phone):
    print('[QUERY CHECK]', 'seat_reservation_exists()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('SELECT * FROM seat_reservation WHERE flight_number=:fn AND leg_number=:ln AND seat_date=:sd', 
        {"fn": flight_number, "ln": leg_number, "sd": seat_date});
        print('[QUERY CHECK]', 'seat_reservation_exists()', 'Complete!');
        return c.fetchone() != None;

#END EXIST CHECKS

#START FLIGHT_LEG SCHEDULE



#END FLIGHT_LEG SCHEDULE

#START QUERY ROUTING
def sqldbRoute():
    print('[ROUTE]', 'sqldbRoute()');
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        query = request.args.get("query")
        print(query);
        c.execute(query)
        response = sql_response_from_cursor(c);
        return "<html><link rel='stylesheet' type='text/css' href='/static/styles/index.css'/><body>" + table_to_html(
        table=response.get_table(), table_type="div", table_class="flightTable",
        table_header=response.get_headers(), table_header_type="div", table_header_class="th",
        table_row_type='div', table_row_class='tr', table_data_type="div", table_data_class="td",
        custom_links_class="tr flightLink"); + "</body></html>"
#END QUERY ROUTING