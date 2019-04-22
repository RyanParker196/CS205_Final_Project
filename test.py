from flask import Flask, render_template, request
import sqlite3
import csv
import os

# https://mapeck.w3.uvm.edu

app = Flask(__name__)

@app.route("/cs205/")
def testTemplate():
    return render_template("testhtml.html")

@app.route("/cs205/", methods=['POST'])
def testTemplatePost():
    queryInput = request.form['query']
    cur, sql, f1 = makeDB()
    result = query(cur, queryInput)
    # os.remove('nflTable.db')
    return render_template("testhtml.html", queryInput = "User Entry: " + queryInput, result = "Results: " + result)

# ----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run()

# ======================================================================================================================

def makeDB():

    sql = sqlite3.connect('recipeTable.db')
    cur = sql.cursor()

    # ------------------------------------------------------------------------------------------------------------------

    f1 = open('recipes.csv', 'r')  # open the csv data file
    next(f1, None)  # skip the header row
    reader = csv.reader(f1)

    cur.execute('''CREATE TABLE IF NOT EXISTS recipeTable
                (title, directions)''')  # create the table if it doesn't already exist

    for row in reader:
        cur.execute("INSERT INTO recipeTable VALUES (?, ?)", row)

    return cur, sql, f1

# ======================================================================================================================

def query(cur, query):
    # SQLite Query Format: SELECT column FROM table WHERE whereCon = whereVal

    result = ""

    # # ------------------------------------------------------------------------------------------------------------------
    #
    # # Create Lists of values in each column of each table, starting with the column name in the 0th index:
    # teamList = ['team']
    # cur.execute("SELECT team FROM qbTable")
    # for row in cur:
    #     teamList.append(str(row[0]))
    #
    # qbList = ['qb']
    # cur.execute("SELECT qb FROM qbTable")
    # for row in cur:
    #     qbList.append(str(row[0]))
    #
    # abbreviationList = ['abbreviation']
    # cur.execute("SELECT abbreviation FROM teamTable")
    # for row in cur:
    #     abbreviationList.append(str(row[0]))
    #
    # heightList = ['height']
    # cur.execute("SELECT height FROM qbTable")
    # for row in cur:
    #     heightList.append(row[0])
    #
    # conferenceList = ['conference']
    # cur.execute("SELECT conference FROM teamTable")
    # for row in cur:
    #     conferenceList.append(row[0])
    #
    # # Create a list to hold lists of column values, in order to make it easy to search through all table values at once:
    # dataLists = [teamList, qbList, abbreviationList, heightList, conferenceList]
    #
    # # ------------------------------------------------------------------------------------------------------------------
    #
    # # Create list of column names that are NOT shared between tables:
    # qbTableColumns = ['qbTable', "qb", "height", "QB", "HEIGHT", "Qb", "Height"]
    # teamTableColumns = ['teamTable', "abbreviation", "conference", "Abbreviation", "Conference", "ABBREVIATION",
    #                     "CONFERENCE"]
    #
    # # Create list of column names that ARE shared between tables:
    # sharedColumns = ['team']
    #
    # # Create a list to hold lists of column names, in order to make it easy to search through all column names at once:
    # tableLists = [qbTableColumns, teamTableColumns]
    #
    # # ------------------------------------------------------------------------------------------------------------------
    #
    # # nextEntryIndex: Will serve as variable to reference next word in query, after it is split into list by spaces
    # nextEntryIndex = 0
    #
    # # If words in query are found in the tables, found will be set to true.
    # found = False
    #
    # # If words in query indicate a query that crosses data in two tables.
    # multiTableQuery = False
    #
    # # If user types "list" set this value to true so no query results are printed when "list" is typed
    # list = False
    #
    # # These variables are just holders to hold user information to insert into below SQLite query format:
    # # SQLite Query Format: SELECT column FROM table WHERE whereCon = whereVal
    # table = ''
    # column = ''
    # whereCon = ''
    # whereVal = ''
    #
    # # List all table data other than height and conference:
    # if (query == "list"):
    #
    #     list = True
    #
    #     result += "Teams"
    #     # print("\nTeams:")
    #     cur.execute("SELECT team FROM qbTable")
    #     for row in cur:
    #         result += str(row[0])
    #         # print(row[0])
    #     result += "QBs:"
    #     # print("\nQBs:")
    #     cur.execute("SELECT qb FROM qbTable")
    #     for row in cur:
    #         result += str(row[0])
    #         # print(row[0])
    #     result += "Abbreviations:"
    #     # print("\nAbbreviations:")
    #     cur.execute("SELECT abbreviation FROM teamTable")
    #     for row in cur:
    #         result += str(row[0])
    #         # print(row[0])
    #
    # # Split users entry into a list of their words, separated by spaces:
    # query = query.split(" ")
    #
    # # ------------------------------------------------------------------------------------------------------------------
    #
    # try:
    #     # If query looks like 1 supported multi table query:
    #     if (query[0] + ' ' + query[1] + ' ' + query[2] == 'height qb abbreviation' and query[
    #         3] in abbreviationList) or (query[0] + ' ' + query[1] == 'height qb' and query[2] in abbreviationList):
    #         multiTableQuery = True
    #         try:
    #             # Execute query and print results using the data that the user entered above:
    #             cur.execute("SELECT team FROM teamTable WHERE abbreviation = '" + query[len(query) - 1] + "'")
    #             team = cur.fetchone()
    #             # print("SELECT height FROM qbTable WHERE team = '" + str(team[0]) + "'")
    #             cur.execute("SELECT qb FROM qbTable WHERE team = '" + str(team[0]) + "'")
    #             qb = str(cur.fetchone()[0])
    #             cur.execute("SELECT height FROM qbTable WHERE team = '" + str(team[0]) + "'")
    #             for row in cur:
    #                 result += str(qb + ': ' + row[0])
    #                 # print(qb + ': ' + row[0])
    #         except:
    #             result = "There were no results.  Please enter a properly formed query!"
    #             # print("\nThere were no results.  Please enter a properly formed query!\n")
    # except IndexError:
    #     isError = True
    #
    #     # --------------------------------------------------------------------------------------------------------------
    #
    # try:
    #     # This for loop loops through the list of qbTable and teamTable column names to determine which table to query.
    #     for tableList in tableLists:
    #         # If the user's entry can be found a list of column names or a list of column names shared between tables:
    #         if query[nextEntryIndex] in tableList or query[nextEntryIndex] in sharedColumns:
    #             # If the user's entry is found in list of column names, set the table variable to the right table:
    #             if query[nextEntryIndex] in tableList:
    #                 table = tableList[0]
    #             # If the user seeks data in a column with a shared name of another table:
    #             elif query[nextEntryIndex] in sharedColumns:
    #                 # If next word in user query is found in any of the lists of column values, set the proper table:
    #                 if query[nextEntryIndex + 1] in qbList or query[nextEntryIndex + 1] in heightList or query[
    #                     nextEntryIndex + 1] in qbTableColumns or query[nextEntryIndex + 1] in teamList:
    #                     table = qbTableColumns[0]
    #                 elif query[nextEntryIndex + 1] in abbreviationList or query[
    #                     nextEntryIndex + 1] in conferenceList or query[nextEntryIndex + 1] in teamTableColumns:
    #                     table = teamTableColumns[0]
    #                 # Test for correct table with 2 words, and use try block to catch errors if user input is too small:
    #                 try:
    #                     if query[nextEntryIndex + 1] + ' ' + query[nextEntryIndex + 2] in qbList or query[
    #                         nextEntryIndex + 1] + ' ' + query[nextEntryIndex + 2] in heightList or query[
    #                         nextEntryIndex + 1] + ' ' + query[nextEntryIndex + 2] in qbTableColumns or query[
    #                         nextEntryIndex + 1] + ' ' + query[nextEntryIndex + 2] in teamList:
    #                         table = qbTableColumns[0]
    #                     elif query[nextEntryIndex + 1] + ' ' + query[nextEntryIndex + 2] in abbreviationList or \
    #                             query[nextEntryIndex + 1] + ' ' + query[nextEntryIndex + 2] in conferenceList or \
    #                             query[nextEntryIndex + 1] + ' ' + query[nextEntryIndex + 2] in teamTableColumns:
    #                         table = teamTableColumns[0]
    #                 except IndexError:
    #                     isError = True
    #             # The column that the user seeks data from will always be the first word in query:
    #             column = query[nextEntryIndex]
    #             # Add to nextEntryIndex so the next loop can continue to parse the query in the next words:
    #             nextEntryIndex += 1
    #             break
    #
    #     # --------------------------------------------------------------------------------------------------------------
    #
    #     # This for loop loops through a list of all column values to determine where to query from within each table.
    #     for dataList in dataLists:
    #         # If the user's single word query is found in the table:
    #         if query[nextEntryIndex] in dataList:
    #             found = True
    #         # If the user's 2 word query is found in table (Use try block to catch error if user input is too short):
    #         try:
    #             if query[nextEntryIndex] + ' ' + query[nextEntryIndex + 1] in dataList:
    #                 found = True
    #         except IndexError:
    #             isError = True
    #         # If user query was found in if statements above:
    #         if found:
    #             # If the user's next word in query happens to be the column name/data type instead of actual data:
    #             if query[nextEntryIndex] == dataList[0]:
    #                 nextEntryIndex += 1
    #             # The "where" condition will be set to the column name of the column where the user's entry is from:
    #             whereCon = dataList[0]
    #             # The value that the "where" condition must equal will be the user's next word, or words:
    #             try:
    #                 whereVal = "'" + query[nextEntryIndex] + " " + query[nextEntryIndex + 1] + "'"
    #             except IndexError:
    #                 whereVal = "'" + query[nextEntryIndex] + "'"
    #             break
    #
    # except IndexError:
    #     result = "There were no results.  Please enter a properly formed query!"
    #     # print("\nThere were no results.  Please enter a properly formed query!")
    #     list = True
    #
    # # ------------------------------------------------------------------------------------------------------------------
    #
    # # print("SELECT " + column + " FROM " + table + " WHERE " + whereCon + " = " + whereVal)
    #
    # if multiTableQuery == False and list == False:
    #     try:
    #         # Execute query and print results using the data that the user entered above:
    #         cur.execute("SELECT " + column + " FROM " + table + " WHERE " + whereCon + " = " + whereVal)
    #         for row in cur:
    #             result += str(row[0])
    #             # print(row[0])
    #
    #     except sqlite3.OperationalError:
    #         result = "There were no results.  Please enter a properly formed query!"
    #         # print("\nThere were no results.  Please enter a properly formed query!")

    cur.execute("SELECT * FROM recipeTable")

    for row in cur:
        result += row[0]

    return result

# ======================================================================================================================