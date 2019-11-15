import sqlite3
from flask import request
from pysqlite.SqlResponse import SqlResponse, sql_response_from_cursor
from extras import table_to_html

#START QUERY HELPERS
def query(query, paramaters={}):
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute(query, paramaters)
        return sql_response_from_cursor(c)

def get_all_flights():
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute("SELECT * FROM leg_instance")
        return sql_response_from_cursor(c)

def get_available_flights():
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute("SELECT * FROM get_available_flights")
        return sql_response_from_cursor(c)
#END QUERY HELPERS

#START CREATE HERLPERS
def create_leg_instance(flight_number, leg_number, leg_date, number_of_available_seats, 
airplane_id, departure_airport_code, departure_time, arrival_airport_code, arrival_time):
    #number_of_available_seats can be larger than total_number_of_seats currently!
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('SELECT a.total_number_of_seats from airplane as a where a.airplane_id=:ai', {"ai": airplane_id})
        num_of_seats = c.fetchone()[0] or 0
        c.execute('BEGIN')
        c.execute("INSERT INTO leg_instance VALUES (:fn, :ln, :ld, :noas, :ai, :dac, :dt, :aac, :at)",
        {"fn": flight_number, "ln": leg_number, "ld": leg_date, "noas": number_of_available_seats, 
        "ai": airplane_id, "dac": departure_airport_code, "dt": departure_time, 
        "aac": arrival_airport_code, "at": arrival_time})
        for seat_number in range(num_of_seats):
            c.execute("INSERT INTO seat_reservation VALUES (:fn, :ln, :sd, :sn, :cn, :cp)",
            {"fn": flight_number, "ln": leg_number, "sd": leg_date
            , "sn": seat_number, "cn": None, "cp": None})
        c.execute("COMMIT")
        print('COMPLETED TRANSACTION')

#END CREATE HELPERS

#START INSERTS
def insert_airport(airport_code, name, city, state):
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute("INSERT INTO airport VALUES (:ac, :n, :c, :s)", 
        {"ac": airport_code, "n": name, "c": city, "s": state})

def insert_flight(number, airline, weekdays):
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute("INSERT INTO flight VALUES (:n, :a, :w)",
        {"n": number, "a": airline, "w": weekdays})

def insert_flight_leg(flight_number, leg_number, departure_airport_code, 
scheduled_departure_time, arrival_airport_code, scheduled_arrival_time):
    with sqlite3.connect('database.db') as con:
        c = con.cursor();
        c.execute("INSERT INTO flight_leg VALUES (:fn, :ln, :dac, :sdt, :aac, :sat)",
        {"fn": flight_number, "ln": leg_number, "dac": departure_airport_code
        , "sdt": scheduled_departure_time, "aac": arrival_airport_code, "sat": scheduled_arrival_time})

def insert_leg_instance(flight_number, leg_number, leg_date, number_of_available_seats, 
airplane_id, departure_airport_code, departure_time, arrival_airport_code, arrival_time):
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute("INSERT INTO leg_instance VALUES (:fn, :ln, :ld, :noas, :ai, :dac, :dt, :aac, :at)",
        {"fn": flight_number, "ln": leg_number, "ld": leg_date, "noas": number_of_available_seats, 
        "ai": airplane_id, "dac": departure_airport_code, "dt": departure_time, 
        "aac": arrival_airport_code, "at": arrival_time})

def insert_fares(flight_number, fare_code, amount, restrictions):
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute("INSERT INTO fares VALUES (:fn, :fc, :a, :r)",
        {"fn": flight_number, "fc": fare_code, "a": amount, "r": restrictions})

def insert_airplane_type(type_name, max_seats, company):
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute("INSERT INTO airplane_type VALUES (:tn, :ms, :c)",
        {"tn": type_name, "ms": max_seats, "c": company})

def insert_can_land(airplane_type_name, airport_code):
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute("INSERT INTO can_land VALUES (:atn, :ac)",
        {"atn": airplane_type_name, "ac": airport_code})

def insert_airplane(airplane_id, total_number_of_seats, airplane_type):
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute("INSERT INTO airplane VALUES (:ai, :tnos, :at)",
        {"ai": airplane_id, "tnos": total_number_of_seats, "at": airplane_type})

def insert_seat_reservation(flight_number, leg_number, seat_date, seat_number, customer_name, customer_phone):
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute("INSERT INTO seat_reservation VALUES (:fn, :ln, :sd, :sn, :cn, :cp)",
        {"fn": flight_number, "ln": leg_number, "sd": seat_date
        , "sn": seat_number, "cn": customer_name, "cp": customer_phone})

#END INSERTS

#START DELETES
def delete_leg_instance(flight_number, leg_number, leg_date):
    with sqlite3.connect('database.db') as con:
        c = con.cursor();
        c.execute('PRAGMA foreign_keys = ON');
        c.execute("DELETE FROM leg_instance WHERE flight_number = :fn and leg_number = :ln and leg_date = :ld", {'fn': flight_number, 'ln': leg_number, 'ld': leg_date});

def delete_flight_leg(flight_number, leg_number):
    with sqlite3.connect('database.db') as con:
        c = con.cursor();
        c.execute('PRAGMA foreign_keys = ON');
        c.execute("DELETE FROM flight_leg WHERE flight_number = :fn and leg_number = :ln", {'fn': flight_number, 'ln': leg_number});

def delete_flight(number):
    with sqlite3.connect('database.db') as con:
        c = con.cursor();
        c.execute('PRAGMA foreign_keys = ON');
        c.execute("DELETE FROM flight WHERE number = :n", {'n': number});

def delete_airport(airport_code):
    with sqlite3.connect('database.db') as con:
        c = con.cursor();
        c.execute('PRAGMA foreign_keys = ON');
        c.execute("DELETE FROM airport WHERE airport_code = :ac", {'ac': airport_code});

def delete_fares(flight_number, fare_code):
    with sqlite3.connect('database.db') as con:
        c = con.cursor();
        c.execute('PRAGMA foreign_keys = ON');
        c.execute("DELETE FROM fares WHERE flight_number = :fn and fare_code = :fc", {'fn': flight_number, 'fc': fare_code});

def delete_airplane_type(type_name):
    with sqlite3.connect('database.db') as con:
        c = con.cursor();
        c.execute("DELETE FROM airplane_type WHERE type_name = :tn", {'tn': type_name});

def delete_can_land(airplane_type_name, airport_code):
    with sqlite3.connect('database.db') as con:
        c = con.cursor();
        c.execute('PRAGMA foreign_keys = ON');
        c.execute("DELETE FROM can_land WHERE airplane_type_name = :atn and airport_code = :ac", {'atn': airplane_type_name, 'ac': airport_code});

def delete_airplane(airplane_id):
    with sqlite3.connect('database.db') as con:
        c = con.cursor();
        c.execute('PRAGMA foreign_keys = ON');
        c.execute("DELETE FROM airplane WHERE airplane_id = :ai", {'ai': airplane_id});
#END DELETES

#START EXISTS



#END EXISTS

#START UPDATES

def update_leg_instance(flight_number, leg_number, leg_date, number_of_available_seats,
airplane_id, departure_time, arrival_time):
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('''UPDATE leg_instance 
        SET airplane_id=:ai, departure_time=:dt, arrival_time=:at, number_of_available_seats=:noas
        WHERE flight_number=:fn and leg_number=:ln and leg_date=:ld''', 
        {"fn": flight_number, "ln": leg_number, "ld": leg_date, 'noas': number_of_available_seats, 
        "ai": airplane_id, "dt": departure_time, "at": arrival_time});

def update_airport(airport_code, name, city, state):
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('''UPDATE airport 
        SET name=:n, city=:c, state=:s 
        WHERE airport_code = :ac''',  
        {"ac": airport_code, "n": name, "c": city, "s": state});

def update_flight(number, airline, weekdays):
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('''UPDATE flight 
        SET airline=:a, weekdays=:w 
        WHERE number = :n''', 
        {"n": number, "a": airline, "w": weekdays});

def update_flight_leg(flight_number, leg_number, departure_airport_code, arrival_airport_code):
    with sqlite3.connect('database.db') as con:
        c = con.cursor();
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('''UPDATE flight_leg 
        SET departure_airport_code=:dac, arrival_airport_code=:aac 
        WHERE flight_number = :fn AND leg_number = :ln''',
        {"fn": flight_number, "ln": leg_number, "dac": departure_airport_code, "aac": arrival_airport_code});

def update_fares(flight_number, fare_code, amount, restrictions):
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('''UPDATE fares
        SET amount=:a, restrictions=:r
        WHERE flight_number = :fn AND fare_code = :fc''', 
        {"fn": flight_number, "fc": fare_code, "a": amount, "r": restrictions});

def update_airplane_type(type_name, max_seats, company):
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('''UPDATE airplane_type
        SET max_seats=:ms, company=:c
        WHERE type_name = :tn''',
        {"tn": type_name, "ms": max_seats, "c": company});

def update_airplane(airplane_id, total_number_of_seats, airplane_type):
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('''UPDATE airplane
        SET total_number_of_seats = :tnos, airaplane_type = :at
        WHERE airplane_id = :ai''',
        {"ai": airplane_id, "tnos": total_number_of_seats, "at": airplane_type});

def update_seat_reservation(flight_number, leg_number, seat_date, customer_name, customer_phone):
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('''UPDATE seat_reservation
        SET customer_name = :cn, customer_phone = :cp
        WHERE flight_number = :fn AND leg_number = :ln AND seat_date = :sd''',
        {"fn": flight_number, "ln": leg_number, "sd": seat_date, "cn": customer_name, "cp": customer_phone});

#END UPDATES

#START EXIST CHECKS
def leg_instance_exists(flight_number, leg_number, leg_date):
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('SELECT * FROM leg_instance WHERE flight_number=:fl and leg_number=:ln and leg_date=:ld',
        {'fl': flight_number, 'ln': leg_number, 'ld': leg_date});
        return c.fetchone() != None

def airport_exists(airport_code):
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('SELECT * FROM airport WHERE airport_code=:ac', {'ac': airport_code});
        return c.fetchone() != None;

def flight_exists(number):
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('SELECT * FROM flight WHERE number=:n', {'n': number});
        return c.fetchone() != None;

def flight_leg_exists(flight_number, leg_number, departure_airport_code, arrival_airport_code):
    with sqlite3.connect('database.db') as con:
        c = con.cursor();
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('SELECT * FROM flight_leg WHERE flight_number=:fn AND leg_number=:ln',
        {"fn": flight_number, "ln": leg_number});
        return c.fetchone() != None;

def fares_exists(flight_number, fare_code, amount, restrictions):
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('''UPDATE fares
        SET amount=:a, restrictions=:r
        WHERE flight_number = :fn AND fare_code = :fc''', 
        {"fn": flight_number, "fc": fare_code, "a": amount, "r": restrictions});

def airplane_type_exists(type_name, max_seats, company):
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('''UPDATE airplane_type
        SET max_seats=:ms, company=:c
        WHERE type_name = :tn''',
        {"tn": type_name, "ms": max_seats, "c": company});

def airplane_exists(airplane_id, total_number_of_seats, airplane_type):
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('''UPDATE airplane
        SET total_number_of_seats = :tnos, airaplane_type = :at
        WHERE airplane_id = :ai''',
        {"ai": airplane_id, "tnos": total_number_of_seats, "at": airplane_type});

def seat_reservation_exists(flight_number, leg_number, seat_date, customer_name, customer_phone):
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute('PRAGMA foreign_keys = ON');
        c.execute('''UPDATE seat_reservation
        SET customer_name = :cn, customer_phone = :cp
        WHERE flight_number = :fn AND leg_number = :ln AND seat_date = :sd''',
        {"fn": flight_number, "ln": leg_number, "sd": seat_date, "cn": customer_name, "cp": customer_phone});

#END EXIST CHECKS

#START QUERY ROUTING
def sqldbRoute():
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        query = request.args.get("query")
        print(query);
        c.execute(query)
        response = sql_response_from_cursor(c)
        return "<html><link rel='stylesheet' type='text/css' href='/static/styles/index.css'/><body>" + table_to_html(
        table=response.get_table(), table_type="div", table_class="flightTable",
        table_header=response.get_headers(), table_header_type="div", table_header_class="th",
        table_row_type='div', table_row_class='tr', table_data_type="div", table_data_class="td",
        custom_links_class="tr flightLink"); + "</body></html>"
#END QUERY ROUTING