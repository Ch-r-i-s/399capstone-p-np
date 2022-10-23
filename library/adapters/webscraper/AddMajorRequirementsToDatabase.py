import json
import sqlite3
import re
import os

f = open('major_reqs.json')
major_reqs = json.load(f)


sqliteConnection = sqlite3.connect("\\".join(os.getcwd().split("\\")[:os.getcwd().split("\\").index("399capstone-p-np") + 1]) + "\\library\\adapters\\399courses.db")

cursor = sqliteConnection.cursor()
print("Successfully Connected to SQLite")

cursor.execute("""DELETE FROM "majorRequirements" """)
cursor.execute("""DELETE FROM "group" """)
cursor.execute("""DELETE FROM "majorGroupLink" """)
cursor.execute("""UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='majorRequirements' """)
cursor.execute("""UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='group' """)

major_reqs = open('major_reqs.json')
major_information = json.load(major_reqs)

query = """INSERT INTO majorRequirements(majorName, totalPointsNeeded, pointsGenEd, year, honours, level, pointsAboveStage1, pointsAboveStage2) VALUES(?, ?, ?, ?, ?, ?, ?, ?)"""
for major in major_information:
    total = 0
    for groups in major[1:]:
        for group in groups:
            if len(group[0]) == 1:
                total += int(group[0][0])

    if "from-2019" in major[0][0][2]:
        year = 2020
    else:
        year = 2018
    
    if "hon" in major[0][0][2]:
        honours = 1
    else:
        honours = 0
 

    cursor.execute(query, (major[0][0][0], total, 30, year, honours, major[0][0][1], 180, 75))
    sqliteConnection.commit()



for major in major_information:
    if "from-2019" in major[0][0][2]:
        year = 2020
    else:
        year = 2018
    if "hon" in major[0][0][2]:
        honours = 1
    else:
        honours = 0
    cursor.execute("""SELECT majorID FROM majorRequirements WHERE majorName = ? AND  honours = ? AND year = ?""", (major[0][0][0], honours, year))
    majorID = cursor.fetchall()[0]
    print(majorID)
    groupID = 0
    for groups in major[1:]:
        for group in groups:
            groupID += 1
            if len(group[0]) == 1:
                try:
                    cursor.execute("""INSERT INTO majorGroupLink("majorID", "groupID", pointsRequired) VALUES(?, ?, ?)""", (majorID[0], groupID, group[0][0]))
                except:
                    print("something fucked up VVVVV")
                    print(group)
                for course in group[1:]:
                    if type(course) == str:
                        cursor.execute("""INSERT INTO "groupMiscData"(majorID, groupID, miscData) VALUES(?, ?, ?)""", (majorID[0], groupID, course))
                    cursor.execute("""INSERT INTO "group"(groupID, majorID, courseNumber, subject) VALUES(?, ?, ?, ?)""", (groupID, majorID[0], course[1], course[0]))
            else:
                cursor.execute("""INSERT INTO majorGroupLink("majorID", "groupID", pointsRequired) VALUES(?, ?, ?)""", (majorID[0], groupID, 0))
            sqliteConnection.commit()

cursor.close()
print("successful")
