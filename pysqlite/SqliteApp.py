import sqlite3
from flask import request
from pysqlite.sqlite_db_rebuild import rebuild
from pysqlite.SqlResponse import SqlResponse, sql_response_from_cursor
from extras import table_to_html

if __name__ == "__main__":
    rebuild_db = False
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    if rebuild_db:
        rebuild(c, conn)

def query(query, paramaters={}):
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
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
            c.execute("INSERT INTO seat_reservation VALUES (:fn, :ln, :d, :sn, :cn, :cp)",
            {"fn": flight_number, "ln": leg_number, "d": leg_date
            , "sn": seat_number, "cn": None, "cp": None})
        c.execute("COMMIT")
        print('COMPLETED TRANSACTION')

#create_leg_instance(666, 1, '2066-11-11', 50, 40001, 111111, '2066-11-11 06:40:00',500020, '2066-11-11 08:55:00')
#with sqlite3.connect('database.db') as con:
#    c.execute("SELECT * from seat_reservation")
#    print(c.fetchall())


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
        c = con.cursor()
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

def insert_seat_reservation(flight_number, leg_number, date, seat_number, customer_name, customer_phone):
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        c.execute("INSERT INTO seat_reservation VALUES (:fn, :ln, :d, :sn, :cn, :cp)",
        {"fn": flight_number, "ln": leg_number, "d": date
        , "sn": seat_number, "cn": customer_name, "cp": customer_phone})

def sqldbRoute():
    with sqlite3.connect('database.db') as con:
        c = con.cursor()
        query = request.args.get("query")
        c.execute(query)
        response = sql_response_from_cursor(c)
        return "<html><body><div>" + table_to_html(table=response) + "</div></body></html>"