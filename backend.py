from flask import Flask, render_template, request
import sqlite3
import csv
import os

# https://mapeck.w3.uvm.edu

app = Flask(__name__)

# ----------------------------------------------------------------------------------------------------------------------

@app.route("/cs205/")
def index():

    # Connect to database
    cur, sql = connectDB()

    # Return: "index.html", 'dbTable': The table displayed when browsing database, 'delTable': The table displayed when browsing database entries to delete
    return render_template("index.html", dbTable = displayAll(cur, checkBoxes = False), delTable = displayAll(cur, checkBoxes = True))

# ----------------------------------------------------------------------------------------------------------------------

@app.route("/cs205/", methods=['POST'])
def indexPost():

    # Connect to database
    cur, sql = connectDB()

    # Use Post method to pull data from HTML forms to see which form the user is attempting to use.  Use Try/Except blocks to ensure no errors occur if user doesn't enter any data
    search = False
    add = False
    try:
        searchInput = request.form['search']
        search = True
    except:
        searchInput = ""
    try:
        addNameInput = request.form['recipeName']
        addDescriptionInput = request.form['description']
        add = True
    except:
        addNameInput = ""
        addDescriptionInput = ""

    # ------------------------------------------------------------------------------------------------------------------

    # User is attempting to delete from database:
    if not search and not add:

        # Delete selection from database, and return a string that reports if deleting from database was a failure or a success:
        status = delFromDB(cur, sql)

        # Return: "index.html", 'dbTable': The table displayed when browsing database, 'delTable': The table displayed when browsing database entries to delete, 'status': Success or failure message
        return render_template("index.html", dbTable = displayAll(cur, checkBoxes = False), delTable = displayAll(cur, checkBoxes = True), status = status)

    # ------------------------------------------------------------------------------------------------------------------

    # User is attempting to search database:
    elif search and not add:

        # Here, 'dbTable' is the table of results from the user search:
        dbTable, searchInput = searchDB(cur, searchInput)
        # Return: "index.html", 'dbTable': The table displayed when searching database, 'delTable': The table displayed when browsing database entries to delete, 'searchInput': The user's search term(s)
        return render_template("index.html", dbTable = dbTable, delTable = displayAll(cur, checkBoxes = True), searchInput = searchInput)

    # ------------------------------------------------------------------------------------------------------------------

    # User is attempting to add to database:
    elif add and not search:

        # Add input to database, and return a string that reports if adding to database was a failure or a success:
        status = addToDB(cur, sql, addNameInput, addDescriptionInput)

        # Return: "index.html", 'dbTable': The table displayed when browsing database, 'delTable': The table displayed when browsing database entries to delete, 'status': Success or failure message
        return render_template("index.html", dbTable = displayAll(cur, checkBoxes = False), delTable = displayAll(cur, checkBoxes = True), status = status)

    # ------------------------------------------------------------------------------------------------------------------

    # User is pressing search to display entire database:
    else:

        # Return: "index.html", 'dbTable': The table displayed when browsing database, 'delTable': The table displayed when browsing database entries to delete
        return render_template("index.html", dbTable = displayAll(cur, checkBoxes = False), delTable = displayAll(cur, checkBoxes = True))

# ----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run()

# ======================================================================================================================

# Connect to database
def connectDB():
    sql = sqlite3.connect('recipes.db')
    cur = sql.cursor()
    return cur, sql

# ======================================================================================================================

# Display entire database with or without checkboxes used to select database entries to delete
def displayAll(cur, checkBoxes):

    # Append HTML to 'dbTable' so the table can be displayed as the same length as the current size of the database:
    dbTable = ''

    # Select entire database so it can be looped through:
    cur.execute("SELECT * FROM recipes")
    entireDB = cur.fetchall()

    # Keep a counter to use as the name as each checkbox below, so each checkbox can have a unique name for later reference:
    checkBoxNameCounter = 0
    for entry in entireDB:

        # If checkBoxes are to be printed in table displaying database:
        if checkBoxes == True:

            # Append HTML to 'dbTable' so the table can be displayed as the same length as the current size of the database:
            dbTable += '<tr><td><input type = "checkbox" name = \"' + str(checkBoxNameCounter) + '\" value = "delete"></td><td>' + str(entry[0]) + '</td><td>'+str(entry[1]) + '</td></tr>'
            checkBoxNameCounter += 1

        # If checkboxes are not to be printed in table disokaying database:
        else:

            # Append HTML to 'dbTable' so the table can be displayed as the same length as the current size of the database:
            dbTable += '<tr><td>' + str(entry[0]) + '</td><td>'+str(entry[1]) + '</td></tr>'
    return dbTable

# ======================================================================================================================

# Searches through database according to user input, and returns search results as a table of database entries:
def searchDB(cur, rawSearchInput):

    # Append HTML to 'resultTable' so the table can be displayed as the same length as the current set of search results from the database:
    resultTable = ''

    # Split the user's search input so each word in the search can be compared individually to database entries:
    searchInput = rawSearchInput.split(" ")

    # If user has entered search terms, then append "results for...:" so the search terms can be displayed neatly when search results are returned:
    if rawSearchInput != "":
        rawSearchInput = "Results for \"" + rawSearchInput + "\":"

    # Select entire database so it can be looped through and searched according to user input:
    cur.execute("SELECT * FROM recipes")
    entireDB = cur.fetchall()
    for word in searchInput:
        for entry in entireDB:

            # If user search term is in the database entry:
            if word.lower() in str(entry[0]).lower() or word.lower() in str(entry[1]).lower():

                # Append HTML to 'resultTable' so the table can be displayed as the same length as the current set of search results from the database:
                resultTable += '<tr><td>' + str(entry[0]) + '</td><td>'+str(entry[1]) + '</td></tr>'
    return resultTable, rawSearchInput

# ======================================================================================================================

# Adds user input to database:
def addToDB(cur, sql, addNameInput, addDescriptionInput):
    # 'status' is a string that reports if adding to database was a failure or a success:
    status = ""
    try:
        cur.execute("SELECT * FROM recipes")
        entireDB = cur.fetchall()
        canAddRecipe = True
        if addNameInput == "" or addDescriptionInput == "":
            status = "Error adding recipe: Please enter both a name and a complete set of directions when adding recipes."
            canAddRecipe = False
        for entry in entireDB:

            # If user search term is in the database entry:
            if addNameInput.lower() == str(entry[0]).lower() and addDescriptionInput.lower() == str(entry[1]).lower():
                status = "Recipe called \"" + addNameInput + "\" already exists.  Please only add unique recipes!"
                canAddRecipe = False

        if canAddRecipe:
            cur.execute("INSERT INTO recipes (Title, Directions) VALUES (\'" + addNameInput.replace('"', "\"").replace("'", "''") + "\',\'" + addDescriptionInput + "\')")
            status = "Recipe \"" + addNameInput + "\" added successfully!"

        # "Save" work
        sql.commit()

    # If there was an error adding recipe:
    except:
        status = "Error adding recipe!"
    return "<p style = \"background-color: lightcoral; color: white; padding-top: 1%; padding-bottom: 1%\">" + status + "</p>"

# ======================================================================================================================

# Deletes selected database entry from database:
def delFromDB(cur, sql):

    # 'status' is a string that reports if adding to database was a failure or a success:
    status = ""
    try:

        # 'numSelected' is a variable that will keep track of the number of rows in the database selected to delete:
        numSelected = 0

        # Select entire database so it can be looped through:
        cur.execute("SELECT * FROM recipes")
        entireDB = cur.fetchall()

        # Use 'index' to keep track of the name checkboxes created previously; they are named in increasing integer values:
        index = 0

        # 'userInput' is a variable that holds the user checkbox selection for each database entry:
        userInput = ""
        for entry in entireDB:

            # User try/except blocks to protect scenario where user does not check a checkbox and no data is posted:
            try:

                # Use post method to retrieve user input:
                userInput = request.form[str(index)]
            except:

                # If user has not checked checkbox:
                userInput = ""

            # If user has checked checkbox:
            if userInput == "delete":

                # Delete selected database entry from database:
                cur.execute("DELETE FROM recipes WHERE Title = \'" + str(entry[0]).replace('"', "\"").replace("'", "''") + "\'")
                numSelected += 1
            index += 1

        # "Save" work
        sql.commit()

        # If no rows were selected to delete:
        if numSelected == 0:
            status = "No rows were deleted, please select at least one row to delete!"

        # If 1 row was selected to delete:
        elif numSelected == 1:
            status = "1 recipe successfully deleted!"

        # If multiple rows were selected to delete:
        else:
            status = str(numSelected) + " recipes successfully deleted!"

    # If there was an error deleting recipe(s):
    except:
        status = "Error deleting recipe(s)!"

    return "<p style = \"background-color: lightcoral; color: white; padding-top: 1%; padding-bottom: 1%\">" + status + "</p>"