from flask import jsonify

reservations = {}

def create_reservation(leg_id, fare_code, seat_number, customer_name, customer_phone):
    key = customer_name + ":" + customer_phone;
    value = {'leg_id': leg_id, 'seat_number': seat_number, 'fare_code':fare_code, 'customer_name': customer_name, 'customer_phone': customer_phone};
    if key in reservations and leg_id in reservations[key]:
        reservations[key][leg_id] = value
    else:
        reservations[key] = ({'leg_id': value})
