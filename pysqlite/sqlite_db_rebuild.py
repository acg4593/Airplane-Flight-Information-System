import sqlite3, random, string
from datetime import datetime, timedelta

tables = [ 
    'airport', 'flight', 'flight_leg', 'leg_instance', 'fares',
    'airplane_type', 'can_land', 'airplane', 'seat_reservation', 'seat_fares',
    ]
views = [
    'get_available_flights',
    'get_earliest_leg_instance'
    ]
triggers = [
    'noas_trigger_update']
airport = '''CREATE TABLE airport(
        airport_code INT(10) NOT NULL,
        name VARCHAR(255) NOT NULL,
        city varchar(255) not null,
        state varchar(255) not null,
        primary key(airport_code))''';

flight = '''CREATE table flight(
        number int(10) not null,
        airline varchar(255) not null,
        weekdays varchar(255) not null,
        primary key(number)
        )''';

flight_leg = '''CREATE table flight_leg(
        flight_number int(10) not null,
        leg_number int(10) not null,
        departure_airport_code int(10) not null,
        scheduled_departure_time timestamp,
        arrival_airport_code int(10) not null,
        scheduled_arrival_time timestamp,
        primary key(flight_number, leg_number),
        foreign key(flight_number) references flight(number) ON DELETE CASCADE
        )''';

leg_instance = '''CREATE table leg_instance(
        flight_number int(10) not null,
        leg_number int(10) not null,
        leg_date timestamp not null,
        number_of_available_seats int(5) not null,
        airplane_id int(10) not null,
        departure_airport_code int(10) not null,
        departure_time timestamp,
        arrival_airport_code int(10) not null,
        arrival_time timestamp,
        primary key(flight_number, leg_number, leg_date),
        foreign key(flight_number, leg_number) references flight_leg(flight_number, leg_number) ON DELETE CASCADE,
        foreign key(airplane_id) references airplane(airplane_id) ON DELETE CASCADE,
        foreign key(departure_airport_code) references airport(airport_code) ON DELETE CASCADE,
        foreign key(arrival_airport_code) references airport(airport_code) ON DELETE CASCADE
        )''';

fares = '''CREATE table fares(
        flight_number int(10) not null,
        fare_code int(10) not null,
        amount decimal(5,2) not null,
        restrictions varchar(255),
        primary key(flight_number, fare_code),
        foreign key(flight_number) references flight(number) ON DELETE CASCADE
        )''';

airplane_type = '''CREATE table airplane_type(
        type_name varchar(255) not null,
        max_seats int(5) not null,
        company varchar(255) not null,
        primary key(type_name)
        )''';

can_land = '''CREATE table can_land(
        airplane_type_name varchar(255) not null,
        airport_code int(10) not null,
        primary key(airplane_type_name, airport_code),
        foreign key(airplane_type_name) references  airplane_type(type_name) ON DELETE CASCADE,
        foreign key(airport_code) references airport(airport_code) ON DELETE CASCADE
        )''';

airplane =  '''CREATE table airplane(
        airplane_id int(10) not null,
        total_number_of_seats int(5) not null,
        airplane_type varchar(255) not null,
        primary key(airplane_id),
        foreign key(airplane_type) references airplane_type(type_name) ON DELETE CASCADE
        )''';

seat_reservation = '''CREATE table seat_reservation(
        flight_number int(10) not null,
        leg_number int(10) not null,
        seat_date timestamp not null,
        seat_number int(5) not null,
        customer_name varchar(255),
        customer_phone varchar(15),
        primary key(flight_number, leg_number, seat_date, seat_number),
        foreign key(flight_number, leg_number, seat_date) references leg_instance(flight_number, leg_number, leg_date) ON DELETE CASCADE
        )''';

seat_fares = '''CREATE table seat_fares(
    flight_number int(10) not null,
    leg_number int(10) not null,
    seat_date timestamp not null,
    seat_number int(5) not null,
    fare_code int(10) not null,
    primary key(flight_number, leg_number, seat_date, seat_number),
    foreign key(flight_number, leg_number, seat_date, seat_number) references seat_reservation(flight_number, leg_number, seat_date, seat_number) ON DELETE CASCADE
    )'''

get_available_flights = '''CREATE VIEW get_available_flights AS SELECT 
        l.flight_number as flight_number, 
        l.leg_number as leg_number, 
        s1.name as departure_airport, 
        s1.city as departure_city, 
        s1.state as departure_state, 
        l.leg_date as departure_date, 
        s2.name as arrival_airport, 
        s2.city as arrival_city, 
        s2.state as arrival_state,
        l.number_of_available_seats as available_seats
        FROM leg_instance l, airport s1, airport s2
        WHERE l.departure_airport_code = s1.airport_code
        AND l.number_of_available_seats > 0
        AND l.arrival_airport_code = s2.airport_code
        AND l.leg_date > datetime('now', 'localtime') ORDER BY departure_date ASC''';

get_earliest_leg_instance = '''CREATE VIEW get_earliest_leg_instance AS SELECT * FROM 
        (SELECT * 
        FROM leg_instance 
        ORDER BY leg_date DESC)
    WHERE leg_date > datetime('now', 'localtime') 
    GROUP BY flight_number, leg_number
'''

noas_trigger_update = '''CREATE TRIGGER noas_trigger_update AFTER UPDATE ON seat_reservation
    BEGIN
    UPDATE leg_instance
    SET number_of_available_seats =  
    (SELECT total_number_of_seats FROM airplane WHERE airplane.airplane_id in
    (SELECT airplane_id FROM leg_instance WHERE flight_number = new.flight_number and leg_number = new.leg_number and leg_date = new.seat_date)) - 
    (SELECT count(*) FROM seat_reservation WHERE flight_number = new.flight_number AND leg_number = new.leg_number AND leg_date = new.seat_date AND customer_name is not null AND customer_phone is not null)
    WHERE
    flight_number = new.flight_number and leg_number = new.leg_number and leg_date = new.seat_date;
    END
    '''

def create_flight(multiplyer):
    names = open('names.txt', 'r', encoding='ascii').read().splitlines()
    weekday_choices = ['Mon', 'Tue', "Wed", 'Thu', 'Fri', 'Sat', 'Sun']
    matches = []
    for i in range(len(weekday_choices)):
        for j in range(i, len(weekday_choices)):
            matches.append('{0}-{1}'.format(weekday_choices[i],weekday_choices[j]))
    flights = []
    for i in range(multiplyer):
        number = random.randint(100000,999999)
        airline = '{0} Airline'.format(random.choice(names))
        weekdays = random.choice(matches)
        flights.append({'number': number, 'airline':airline, 'weekdays': weekdays})
    return flights

def create_airport(multiplyer):
    states = open('states.txt', 'r', encoding='ascii').read().splitlines()
    cities = open('cities.txt', 'r', encoding='ascii').read().splitlines()
    airports = []
    for i in range(multiplyer):
        airport_code = random.randint(100000, 999999)
        city = random.choice(cities)
        name = '{0} Airport'.format(city)
        state = random.choice(states)
        airports.append({'airport_code': airport_code, 'city': city, 'name': name, 'state': state})
    return airports

def create_airplane_type(multiplyer):
    companies = open('companies.txt', 'r', encoding='ascii', errors='ignore').read().splitlines()
    airplane_types = []
    for i in range(multiplyer):
        type_name = '{0}{1}'.format(
            ''.join(random.sample(string.ascii_uppercase, random.randint(1,2))), 
            random.randint(0,999));
        max_seats = int(5 * round(float(random.randint(10, 100))/5))
        company = random.choice(companies)
        airplane_types.append({'type_name': type_name, 'max_seats':max_seats, 'company':company})

    return airplane_types

def create_airplanes(multiplyer, airplane_types):
    airplanes = []
    for i in range(multiplyer):
        airplane_id = random.randint(10000,99999)
        airplane = random.choice(airplane_types)
        airplane_type = airplane['type_name']
        total_number_of_seats = airplane['max_seats']
        airplanes.append({'airplane_id':airplane_id,'airplane_type':airplane_type, 'total_number_of_seats':total_number_of_seats})
    return airplanes

def create_can_lands(airplane_types, airports):
    can_lands = []
    for airplane_type in airplane_types:
        for airport in airports:
            airplane_type_name = airplane_type['type_name']
            airport_code = airport['airport_code']
            can_lands.append({'airplane_type_name':airplane_type_name, 'airport_code':airport_code})
    return can_lands

def create_fares(flights):
    all_fares = []
    restrictions_list = ['None', 'No Dogs', 'No Cats', 'No Exotic Species', 'No Humans', 'No Poor People', 'No Rich People', 'No Jokes', 'No Programmers']
    for flight in flights:
        flight_number = flight['number'];
        for i in range(random.randint(1, 3)):
            fare_code = random.randint(1000,9999);
            amount = int(10 * round(float(random.randint(10, 1000))/10));
            restrictions = random.choice(restrictions_list)
            all_fares.append({
                'flight_number':flight_number,  'fare_code':fare_code, 'amount':amount, 'restrictions':restrictions})
    return all_fares

def create_flight_legs(flights, airports):
    flight_legs = []
    for flight in flights:
        flight_number = flight['number'];
        original = arrival_airport_code = random.choice(airports)['airport_code']
        path_length = random.randint(2,10)
        for j in range(path_length):
            leg_number = j
            departure_airport_code = arrival_airport_code
            if j == path_length - 1:
                arrival_airport_code = original
            else:
                arrival_airport_code = random.choice(airports)['airport_code']
            flight_legs.append({
                'flight_number':flight_number,  
                'leg_number':leg_number, 
                'scheduled_departure_time': None,
                'scheduled_arrival_time': None,  
                'departure_airport_code':departure_airport_code, 
                'arrival_airport_code':arrival_airport_code})

    return flight_legs

def create_leg_instances(multiplyer, flight_legs, airplanes):
    leg_instances = []
    for flight in flight_legs:
        flight_number = flight['flight_number'];
        leg_number = flight['leg_number']
        departure_airport_code = flight['departure_airport_code']
        arrival_airport_code = flight['arrival_airport_code']
        leg_date = datetime.today();
        for j in range(multiplyer):
            airplane = random.choice(airplanes)
            number_of_available_seats = airplane['total_number_of_seats'];
            airplane_id = airplane['airplane_id']
            leg_date = leg_date + timedelta(days=j)
            offset = leg_number * random.randint(240,600)
            departure_time = leg_date + timedelta(minutes=random.randint(30,90) + offset)
            arrival_time = departure_time + timedelta(minutes=random.randint(240,600) + offset)
            leg_instances.append({
                'departure_time':departure_time.strftime('%Y-%m-%d %H:%M:%S'), 
                'arrival_time':arrival_time.strftime('%Y-%m-%d %H:%M:%S'),
                'departure_airport_code':departure_airport_code,  
                'arrival_airport_code':arrival_airport_code, 
                'flight_number':flight_number, 
                'leg_number':leg_number,  
                'number_of_available_seats':number_of_available_seats, 
                'airplane_id':airplane_id,  
                'leg_date':leg_date.strftime('%Y-%m-%d')})
            leg_date = arrival_time
    return leg_instances

def create_seat_reservations(leg_instances):
    seat_reservations = []
    for leg_instance in leg_instances:
        flight_number = leg_instance['flight_number']
        leg_number = leg_instance['leg_number']
        seat_date = leg_instance['leg_date']
        for i in range(leg_instance['number_of_available_seats']):
            seat_reservations.append({
                'flight_number':flight_number, 
                'leg_number':leg_number, 
                'seat_date':seat_date, 
                'seat_number':i,
                'customer_phone':None, 
                'customer_name':None, })
    return seat_reservations

def create_random_data(c):
    flights = create_flight(100)
    airports = create_airport(100)
    airplane_types = create_airplane_type(20)
    airplanes = create_airplanes(20, airplane_types)
    can_lands = create_can_lands(airplane_types, airports)
    all_fares = create_fares(flights)
    flight_legs = create_flight_legs(flights, airports)
    leg_instances = create_leg_instances(10, flight_legs, airplanes)
    seat_reservations = create_seat_reservations(leg_instances)

    for flight in flights:
        c.execute('INSERT INTO flight VALUES (:number, :airline, :weekdays)', flight)
    for airport in airports:
        c.execute('INSERT INTO airport VALUES (:airport_code, :name, :city, :state)', airport)
    for airplane_type in airplane_types:
        c.execute('INSERT INTO airplane_type VALUES (:type_name, :max_seats, :company)', airplane_type)
    for airplane in airplanes:
        c.execute('INSERT INTO airplane VALUES (:airplane_id, :total_number_of_seats, :airplane_type)', airplane)
    for can_land in can_lands:
        c.execute('INSERT INTO can_land VALUES (:airplane_type_name, :airport_code)', can_land)
    for fares in all_fares:
        c.execute('INSERT INTO fares VALUES (:flight_number, :fare_code, :amount, :restrictions)', fares)
    for flight_leg in flight_legs:
        c.execute('INSERT INTO flight_leg VALUES (:flight_number, :leg_number, :departure_airport_code, :scheduled_departure_time, :arrival_airport_code, :scheduled_arrival_time)', flight_leg)
    for leg_instance in leg_instances:
        c.execute('INSERT INTO leg_instance VALUES (:flight_number, :leg_number, :leg_date, :number_of_available_seats, :airplane_id, :departure_airport_code, :departure_time, :arrival_airport_code, :arrival_time)', leg_instance)
    for seat_reservation in seat_reservations:
        c.execute('INSERT INTO seat_reservation VALUES (:flight_number, :leg_number, :seat_date, :seat_number, :customer_name, :customer_phone)', seat_reservation)


if __name__ == "__main__":
    with sqlite3.connect('database.db') as con:
        c = con.cursor();
        c.execute('PRAGMA foreign_keys = OFF');
        print('[REBUILD]', 'Dropping Tables...');
        for table in tables:
            c.execute('DROP TABLE IF EXISTS {0}'.format(table));
        print('[REBUILD]', 'Dropping Views...');
        for view in views:
            c.execute('DROP VIEW IF EXISTS {0}'.format(view));
        print('[REBUILD]', 'Dropping Triggers...');
        for trigger in triggers:
            c.execute('DROP TRIGGER IF EXISTS {0}'.format(trigger));
        print('[REBUILD]', 'Creating Tables...');
        c.execute(airport);
        c.execute(flight);
        c.execute(flight_leg);
        c.execute(leg_instance);
        c.execute(fares);
        c.execute(airplane_type);
        c.execute(can_land);
        c.execute(airplane);
        c.execute(seat_reservation);
        c.execute(seat_fares);
        print('[REBUILD]', 'Inserting Data...');
        create_random_data(c)
        print('[REBUILD]', 'Creating Views...');
        c.execute(get_available_flights);
        c.execute(get_earliest_leg_instance)
        print('[REBUILD]', 'Creating Triggers...');
        c.execute(noas_trigger_update);
        c.execute('PRAGMA foreign_keys = ON');
    print('[REBUILD]', 'Database has been rebuilt!');