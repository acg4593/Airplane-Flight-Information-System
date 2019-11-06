from flask import Flask, send_from_directory
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

@app.route("/admin")
def loadAdmin():
    return adminRoute()

@app.route("/customer")
def loadCustomer():
    return customerRoute()

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    from indexPage import indexRoute
    from SqliteApp import sqldbRoute
    from loginPage import loginRoute
    from adminPage import adminRoute
    from customerPage import customerRoute
    app.run(debug=True, port=5000)