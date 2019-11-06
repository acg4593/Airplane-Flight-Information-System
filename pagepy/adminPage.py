from flask import render_template, request, redirect, url_for
from constants import keys

def adminRoute():
    key = request.args.get("key")
    if "key" in request.args:
        if key in keys:
            return render_template('adminMenu.html',title="hello!")
    return redirect(url_for('loadLogin'))