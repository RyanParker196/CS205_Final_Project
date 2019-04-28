from flask import Flask, render_template, request
import sqlite3
import csv
import os

# https://mapeck.w3.uvm.edu

app = Flask(__name__)

# ----------------------------------------------------------------------------------------------------------------------

@app.route("/cs205/")
def index():
    cur, sql = connectDB()
    return render_template("index.html", dbTable = displayAll(cur, checkBoxes = False), delTable = displayAll(cur, checkBoxes = True))

# ----------------------------------------------------------------------------------------------------------------------

@app.route("/cs205/", methods=['POST'])
def indexPost():
    cur, sql = connectDB()
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

    # ------------------------------------------------------------------------------------------------------------------

    #User is attempting to delete from database:
    if searchInput == "" and addNameInput == "" and addDescriptionInput == "":
        testVar = delFromDB(cur, sql)
        return render_template("index.html", dbTable=displayAll(cur, checkBoxes=False),
                           delTable=displayAll(cur, checkBoxes=True), testVar = testVar)

    # ------------------------------------------------------------------------------------------------------------------

    # User is attempting to search database:
    elif addNameInput == "" and addDescriptionInput == "" and searchInput != "":
        return render_template("index.html", dbTable = searchDB(cur, searchInput), searchInput = "Results for: " + searchInput, delTable = displayAll(cur, checkBoxes = True))

    # ------------------------------------------------------------------------------------------------------------------

    # User is attempting to add to database:
    elif addNameInput != "" and addDescriptionInput != "":
        addToDB(cur, sql, addNameInput, addDescriptionInput)
        return render_template("index.html", dbTable = displayAll(cur, checkBoxes = False), delTable = displayAll(cur, checkBoxes = True))

    # ------------------------------------------------------------------------------------------------------------------

    # User is pressing search to display entire database:
    else:
        return render_template("index.html", dbTable=displayAll(cur, checkBoxes=False),
                               delTable=displayAll(cur, checkBoxes=True))

# ----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run()

# ======================================================================================================================

def connectDB():
    sql = sqlite3.connect('recipes.db')
    cur = sql.cursor()
    return cur, sql

# ======================================================================================================================

def displayAll(cur, checkBoxes):
    dbTable = ''
    cur.execute("SELECT * FROM recipes")
    entireDB = cur.fetchall()
    checkBoxNameCounter = 0
    for entry in entireDB:
        if checkBoxes == True:
            dbTable += '<tr><td><input type = "checkbox" name = \"' + str(checkBoxNameCounter) + '\" value = "delete" /></td><td>' + str(entry[0]) + '</td><td>'+str(entry[1]) + '</td></tr>'
            checkBoxNameCounter += 1
        else:
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

# ======================================================================================================================

def delFromDB(cur, sql):
    cur.execute("SELECT * FROM recipes")
    entireDB = cur.fetchall()
    index = 0
    testVar = ""
    for entry in entireDB:
        try:
            if request.form[str(index)] == "delete":
                testVar += str(index) + ", "
                cur.execute("DELETE FROM recipes WHERE Title = \"" + entry[0] + "\"")
        except:
            print("error")
        index += 1
    sql.commit()
    return testVar