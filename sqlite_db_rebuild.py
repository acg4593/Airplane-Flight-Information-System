execution = [
    'drop table if exists airport',
    'drop table if exists flight',
    'drop table if exists flight_leg',
    'drop table if exists leg_instance',
    'drop table if exists fares',
    'drop table if exists airplane_type',
    'drop table if exists can_land',
    'drop table if exists airplane',
    'drop table if exists seat_reservation',
    'drop view IF EXISTS get_available_flights',
    '''CREATE TABLE airport(
        airport_code INT(10) NOT NULL,
        name VARCHAR(255) NOT NULL,
        city varchar(255) not null,
        state varchar(255) not null,
        primary key(airport_code))''',
    '''CREATE table flight(
        number int(10) not null,
        airline varchar(255) not null,
        weekdays varchar(255) not null,
        primary key(number)
        )''',
    '''CREATE table flight_leg(
        flight_number int(10) not null,
        leg_number int(10) not null,
        departure_airport_code int(10) not null,
        scheduled_departure_time timestamp,
        arrival_airport_code int(10) not null,
        scheduled_arrival_time timestamp,
        primary key(flight_number, leg_number),
        foreign key(flight_number) references flight(number)
        )''',
    '''CREATE table leg_instance(
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
        foreign key(flight_number, leg_number) references flight_leg(flight_number, leg_number),
        foreign key(airplane_id) references airplane(airplane_id),
        foreign key(departure_airport_code) references airport(airport_code),
        foreign key(arrival_airport_code) references airport(airport_code)
        )''',
    '''CREATE table fares(
        flight_number int(10) not null,
        fare_code int(10) not null,
        amount decimal(5,2) not null,
        restrictions varchar(255),
        primary key(flight_number),
        foreign key(flight_number) references flight(number)
        )''',
    '''CREATE table airplane_type(
        type_name varchar(255) not null,
        max_seats int(5) not null,
        company varchar(255) not null,
        primary key(type_name)
        )''',
    '''CREATE table can_land(
        airplane_type_name varchar(255) not null,
        airport_code int(10) not null,
        primary key(airplane_type_name, airport_code),
        foreign key(airplane_type_name) references  airplane_type(type_name),
        foreign key(airport_code) references airport(airport_code)
        )''',
    '''CREATE table airplane(
        airplane_id int(10) not null,
        total_number_of_seats int(5) not null,
        airplane_type varchar(255) not null,
        primary key(airplane_id),
        foreign key(airplane_type) references airplane_type(type_name)
        )''',
    '''CREATE table seat_reservation(
        flight_number int(10) not null,
        leg_number int(10) not null,
        seat_date timestamp not null,
        seat_number int(5) not null,
        customer_name varchar(255),
        customer_phone varchar(15),
        primary key(flight_number, leg_number, seat_date, seat_number),
        foreign key(flight_number, leg_number, seat_date) references leg_instance(flight_number, leg_number, leg_date)
        )''',
    '''CREATE VIEW get_available_flights AS select 
        l.flight_number as flight_number, 
        l.leg_number as leg_number, 
        s1.name as departure_airport, 
        s1.city as departure_city, 
        s1.state as departure_state, 
        l.leg_date as departure_date, 
        s2.name as arrival_airport, 
        s2.city as arrival_city, 
        s2.state as arrival_state
        from leg_instance l, airport s1, airport s2
        where l.departure_airport_code = s1.airport_code
        and l.arrival_airport_code = s2.airport_code
        and l.leg_date - date('now') > 0''',
    '''insert into airport values
        (292929, 'Santago Airport', 'Santago', 'Montanta'),
        (314030, 'Billywise Airport', 'Lammaton', 'Massachusetts'),
        (315000, 'P.O.I. Airport', 'ParkPlace', 'Massachusetts'),
        (500020, 'Wilmington Airport', 'Wilmington', 'North Carolina'),
        (111111, 'Pomcast Airport', 'Pomcast', 'California'),
        (433030, 'Snowton Airport', 'Snowton', 'New Hampshire'),
        (433031, 'Snowton Classic Airport', 'Snowton', 'New Hampshire'),
        (933330, 'Lylac Airport', 'Lylac', 'South Dakota'),
        (473870, 'James Pulk Airport', 'Pinkerton', 'New York')''',
    '''insert into flight values
        (111123, 'CoopAir', 'Mon-Thurs'),
        (111124, 'CoopAir', 'Mon-Sat'),
        (111125, 'CoopAir', 'Tue-Fri'),
        (111126, 'CoopAir', 'Mon-Wed, Fri-Sat'),
        (116003, 'AmericanAir', 'Mon-Thurs'),
        (116004, 'AmericanAir', 'Mon-Sun'),
        (116005, 'AmericanAir', 'Mon-Sun'),
        (116006, 'AmericanAir', 'Mon-Sun'),
        (200001, 'HolidayAir', 'Mon-Thurs'),
        (200003, 'HolidayAir', 'Mon-Thurs'),
        (876530, 'MadeUpAir', 'Tues-Sat'),
        (986753, 'MadeUpAir', 'Tues-Thurs')''',
    '''insert into airplane_type values 
        ('B330',75, 'Toldark'),
        ('B270',55, 'Toldark'),
        ('J22',20, 'Rainsford'),
        ('Batwing',3, 'WaneEnterprices'),
        ('B580',175, 'BerthaInc'),
        ('Unstable339',100, 'RealCo')''',
    '''insert into airplane values 
        (40001,50, 'B330'),
        (45003,60, 'B330'),
        (90501,120, 'B580'),
        (40002,50, 'B330'),
        (40003,50, 'B330'),
        (40054,50, 'B270'),
        (00003,5, 'J22'),
        (00007,5, 'J22'),
        (00000,1, 'Batwing')''',
    '''insert into flight_leg values 
        (111123, 0004, 292929,'2014-01-01 00:00:00', 473870,'2014-01-01 00:40:00'),
        (111124, 0002, 314030,'2017-10-11 06:40:00', 111123, '2017-10-11 06:40:00'),
        (111123, 0005, 315000,'2014-01-01 12:00:00',473870,'2014-01-01 00:40:00'),
        (111123, 0006, 433030,'2014-01-02 01:20:00',473870,'2014-01-01 00:40:00'),
        (116003, 0001,473870,'2016-11-11 10:10:00', 111111,'2016-11-11 10:13:00')''',
    '''insert into leg_instance values 
        (111123,0004,'2014-01-01',20,40002,473870,'2014-01-01 00:40:00',315000,'2014-01-01 04:20:00'),
        (111123,0005,'2020-01-01',20,40054,500020,'2014-01-01 04:20:00',433030,'2014-01-01 09:24:00'),
        (116003,0001,'2016-11-11',0,90501,111111,'2016-11-11 10:13:00',433030,'2016-11-12 02:10:00')''',
    '''insert into fares values 
        (116003, 91199, 50.00,''),
        (111123, 02219, 45.00,'Suspect at large: Mia Tacker, do not permit to fly.'),
        (111124, 77703, 90.00,'')''',
    '''insert into can_land values 
        ('B330',292929),
        ('B270',433030)''',
    '''insert into seat_reservation values 
        (116003, 0001,'2016-11-11',32,'JoeMama',9109109910 ),
        (116003, 0001,'2016-11-11',33,'JoeFatha',9109109920 ),
        (116003, 0001,'2016-11-11',34,'JoeSister',9109109940 ),
        (116003, 0001,'2016-11-11',42,'MarkJeston',9105303113 ),
        (116003, 0001,'2016-11-11',04,'JoeMama',9109109910 )''',
    
]

view_example = '''
CREATE view view AS select * from emp_master
'''

transaction_example = '''
BEGIN;
DELETE FROM emp_master WHERE dept_id=3;
[COMMIT, ROLLBACK];
'''

trigger_example = '''
CREATE [TEMP | TEMPORARY] TRIGGER name
[BEFORE | AFTER] event ON [database-name]table-name
[FOR EACH ROW | FOR EACH STATEMENT] [WHEN expression]
BEGIN
trigger-step; [teigger-step;] *
END
'''

prepared_statement_example = '''
cursor.execute("SELECT * FROM employees WHERE last=:last and first=:first", {'last': value, 'first': value})
'''

executemany = """
persons = [("first", "last"), (...)]; 
con.executemany("INSERT INTO person(first, last) VALUES (?, ?)", persons)"""

def rebuild(c, conn):
    for code in execution:
        c.execute(code);
        conn.commit()
    print('DATABASE HAS BEEN REBUILT')