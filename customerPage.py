from flask import render_template, request, redirect, url_for
from SqliteApp import get_available_flights
from extras import table_to_html

def customerRoute():
    search = request.args.get("search")
    flight_number = request.args.get("flight_number")
    leg_number = request.args.get("leg_number")
    isSearch = search != None
    isSelected = flight_number != None or leg_number != None

    response = get_available_flights()
    flight_number = response.get_column('flight_number');
    leg_number = response.get_column('leg_number');
    custom_links_href = [];
    for i in range(len(flight_number)):
        custom_links_href.append("/customer?flight_number={0}&leg_number={1}".format(flight_number[i],leg_number[i]));

    html = table_to_html(
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

    return render_template("/customer.html", search=isSearch, selected=isSelected, flightData=html)