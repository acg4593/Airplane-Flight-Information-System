from flask import render_template
from constants import keys
from extras import randomString
import os, time, datetime
from pysqlite.SqliteApp import get_available_flights, get_all_flights
from extras import table_to_html

def indexRoute():
    response = get_all_flights();
    flight_number = response.remove_column('flight_number');
    leg_number = response.remove_column('leg_number');
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

    return render_template('index.html', flightData = html);


def generateHtmlTable(data):
    for tr in data:
        tr[5] = tr[5].strftime('%b %d %Y at %I:%M %p')
    return data

#def generateHtmlTable(data):
#    header = ['Departure Airport', 'Departure City', 'Departure State', 'Date', 'Arrival Airport', 'Arrival City', 'Arrival State']
#    table = '<div class="flightTable">'
#    table += '<div class="tr">'
#    for th in header:
#        table += '<div class="th">' + th + '</div>'
#    table += '</div>'
#    for tr in data:
#        flight_number = tr.pop(0)
#        leg_number = tr.pop(0)
#        tr[3] = tr[3].strftime('%b %d %Y at %I:%M %p')
#        table += '<a class="tr flightLink" href="/customer?flight_number=' + str(flight_number) + "&leg_number=" + str(leg_number) + '">'
#        for td in tr:
#            table += "<div class='td'><div>" + str(td) + "</div></div>"
#        table += "</a>"
#    table += '</div>'
#    return table