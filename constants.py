from time import time

keys = []
flight_leg_max = 60
flight_leg_last = 0
flight_leg_current = 0

def flight_leg_timer_check():
    global flight_leg_max
    global flight_leg_last
    global flight_leg_current
    flight_leg_current = time()
    if flight_leg_current - flight_leg_last > flight_leg_max:
        flight_leg_last = flight_leg_current
        return True
    return False