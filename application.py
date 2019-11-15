from flask import Flask, send_from_directory
from pagepy.adminPage import *
from pagepy.indexPage import indexRoute
from pagepy.customerPage import customerRoute
from pagepy.loginPage import loginRoute
from pysqlite.SqliteApp import sqldbRoute
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
def loadCustomer():
    return customerRoute()
#END CUSTOMER

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