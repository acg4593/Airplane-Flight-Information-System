from flask import render_template, request
import pysqlite.SqliteApp as db

def reporting_route():
    navigation = request.args.get('navigation') or 'flight_roster'
    return render_template('reporting.html', navigation=navigation)

