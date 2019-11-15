from flask import render_template, request, redirect, url_for
from constants import keys
from extras import randomString

def loginRoute():
    if request.method == 'POST' and request.form['username'] == 'admin' and request.form['password'] == 'admin':
        key = randomString(32)
        keys.append(key)
        if len(keys) > 10:
            keys.pop(0)
        return redirect(url_for('load_get_admin', key=key))
    else:
        return render_template('/adminLogin.html')