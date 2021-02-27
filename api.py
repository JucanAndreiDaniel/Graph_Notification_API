import flask
from flask import jsonify
import sqlite3


app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/', methods=["GET"])
def home():
    return "<h1>damn son</h1>"

@app.route('/api/v1/chart/all', methods=['GET'])
def api_all():
    conn=sqlite3.connect("database.db")
    conn.row_factory = dict_factory
    cur = conn.cursor()
    money = cur.execute('''SELECT * FROM dummytable;''').fetchall()
    return jsonify(money)

app.run(host="0.0.0.0")





