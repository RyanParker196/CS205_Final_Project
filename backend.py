from flask import Flask, render_template, request
import sqlite3
import csv
import os

# https://mapeck.w3.uvm.edu

app = Flask(__name__)

# ----------------------------------------------------------------------------------------------------------------------

@app.route("/cs205/")
def index():
    cur = connectDB()
    return render_template("index.html", dbTable = displayAll(cur))

# ----------------------------------------------------------------------------------------------------------------------

@app.route("/cs205/", methods=['POST'])
def indexSearch():
    cur = connectDB()
    searchInput = request.form['search']
    return render_template("index.html", dbTable = displayAll(cur), resultTable = searchDB(cur, searchInput), searchInput = "Results for: " + searchInput)

# ----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run()

# ======================================================================================================================

def connectDB():
    sql = sqlite3.connect('recipes.db')
    cur = sql.cursor()
    return cur

# ======================================================================================================================

def displayAll(cur):
    dbTable = ''
    cur.execute("SELECT * FROM recipes")
    entireDB = cur.fetchall()
    for entry in entireDB:
        dbTable += '<tr><td>' + str(entry[0]) + '</td><td>'+str(entry[1]) + '</td></tr>'
    return dbTable

# ======================================================================================================================

def searchDB(cur, searchInput):
    resultTable = ''
    searchInput = searchInput.split(" ")
    cur.execute("SELECT * FROM recipes")
    entireDB = cur.fetchall()
    for word in searchInput:
        for entry in entireDB:
            if word.lower() in str(entry[0]).lower() or word.lower() in str(entry[1]).lower():
                resultTable += '<tr><td>' + str(entry[0]) + '</td><td>'+str(entry[1]) + '</td></tr>'
    return resultTable

# ======================================================================================================================