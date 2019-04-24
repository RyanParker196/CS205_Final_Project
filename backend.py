from flask import Flask, render_template, request
import sqlite3
import csv
import os

# https://mapeck.w3.uvm.edu

app = Flask(__name__)

# ----------------------------------------------------------------------------------------------------------------------

@app.route("/cs205/")
def index():
    print("error in POST")
    cur, sql = connectDB()
    return render_template("index.html", dbTable = displayAll(cur))

# ----------------------------------------------------------------------------------------------------------------------

@app.route("/cs205/", methods=['POST'])
def indexPost():
    print("about to connect cursor")
    cur, sql = connectDB()
    print("connected")
    try:
        searchInput = request.form['search']
    except:
        searchInput = ""
    try:
        addNameInput = request.form['recipeName']
    except:
        addNameInput = ""
    try:
        addDescriptionInput = request.form['description']
    except:
        addDescriptionInput = ""
    # searchInput = ""
    # addNameInput = 'Test3'
    # addDescriptionInput = 'Test4'
    if addNameInput == "" and addDescriptionInput == "":
        return render_template("index.html", dbTable = searchDB(cur, searchInput), searchInput = searchInput)
    elif addNameInput != "" and addDescriptionInput != "":
        addToDB(cur, sql, addNameInput, addDescriptionInput)
        return render_template("index.html", dbTable=displayAll(cur))

# ----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run()

# ======================================================================================================================

def connectDB():
    sql = sqlite3.connect('recipes.db')
    cur = sql.cursor()
    return cur, sql

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

def addToDB(cur, sql, addNameInput, addDescriptionInput):
    cur.execute("INSERT INTO recipes (Title, Directions) VALUES (\'"+ addNameInput +"\',\'"+ addDescriptionInput +"\')")
    sql.commit()