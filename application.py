from flask import Flask, send_from_directory
from pagepy.adminPage import *
from pagepy.indexPage import *
from pagepy.customerPage import *
from pagepy.loginPage import *
from pagepy.itinerary import *
from pagepy.reporting import *
from pysqlite.SqliteApp import *
import os;

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def loadIndex():
    return indexRoute()

@app.route('/sqltest')
def loadSqltest():
    return sqldbRoute()

@app.route("/login", methods = ['POST', 'GET'])
def loadLogin():
    return loginRoute()

@app.route("/admin", methods = ['GET', 'POST'])
def load_get_admin():
    return admin_get_route()

#START GET REQUEST ROUTES
@app.route("/admin/update")
def admin_update_get():
    return admin_update_route();
#END GET REQUEST ROUTES

#START POST REQUEST ROUTES
@app.route("/admin/submit")
def admin_submit_post():
    return admin_submit_route();

#START DELETE REQUEST
@app.route('/admin/delete')
def admin_delete_item():
    return delete_item_route();
#END DELETE REQUEST

#START SELECT REQUEST
@app.route('/admin/select')
def admin_select():
    return admin_select_route();

#START CUSTOMER
@app.route("/customer")
def load_customer():
    return customer_route();

@app.route('/customer/select')
def load_customer_select():
    return customer_select_route()

@app.route('/customer/search')
def load_customer_search():
    return customer_search_route();

@app.route('/reserve')
def post_reserve():
    return post_reservation();

@app.route('/reservation')
def load_customer_reservation():
    return customer_reservation_route();

@app.route('/reservation_cancel')
def load_customer_reservation_cancel():
    return customer_reservation_cancel_route();

@app.route('/cancel_reservation_for')
def load_customer_cancel_reservation_for():
    return customer_cancel_reservation_for_route();
#END CUSTOMER

#START ITINERARY

@app.route('/itinerary')
def load_itinerary():
    return itinerary_route()

#END ITINERARY

#START REPORTING

@app.route('/reporting')
def load_reporting():
    return reporting_route()

@app.route('/roster_request')
def load_roster_request():
    return get_roster_route()

@app.route('/schedule_request')
def load_schedule_request():
    return get_schedule_route()

@app.route('/report_request')
def load_report_request():
    return get_report_route()

#END REPORTING

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate";
    r.headers["Pragma"] = "no-cache";
    r.headers["Expires"] = "0";
    r.headers['Cache-Control'] = 'public, max-age=0';
    return r;

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True, port=5000)