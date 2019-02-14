import sqlite3
from contextlib import closing
from myobjects import Assignment, People
conn = None


def connect():
    global conn
    if not conn:
        DB_FILE = "students.db"

        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row


def delete_file(file_location):
    sql = '''DELETE FROM File WHERE location = ?'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (file_location,))
        conn.commit()


def get_files():
    query = '''SELECT location
               FROM File'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

    files = []
    for row in results:
        files.append(row["location"])
    return files


def get_people():
    query = '''SELECT *
               FROM Student'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

    people = []
    for row in results:
        person = People(row["studentID"],row["name"], row["isInstructor"],row["password"])
        people.append(person)
    return people


def get_file_location(fileid):
    query = '''SELECT location
                   FROM File
                   WHERE FileID = ? '''

    with closing(conn.cursor()) as c:
        c.execute(query, (fileid,))
        result = c.fetchone()

    return result["location"]


def get_assignments():
    query = '''SELECT *
               FROM Assignment'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

    assignments = []
    for row in results:
        assignment = Assignment(row["assignmentID"],row["name"],row["fileID"],row["maxPoint"], row["grades"])
        # print(row["grades"])
        assignments.append(assignment)
    return assignments


def update_grade(assignmentID, grades):
    query = '''UPDATE Assignment
                SET grades = ?
                WHERE assignmentID = ?'''

    with closing(conn.cursor()) as c:
        c.execute(query, (grades, assignmentID))
        conn.commit()


def add_assignment(name, fileID, maxPoint):
    sql = '''INSERT INTO Assignment (name, fileID, maxPoint, grades) 
                 VALUES (?, ?, ?, ?)'''

    with closing(conn.cursor()) as c:
        c.execute(sql, (name, fileID, maxPoint, '{}'))
        conn.commit()


def add_file_to_db(filename):
    sql = '''INSERT INTO File (location) 
                     VALUES (?)'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (filename,))
        conn.commit()

    sql = '''SELECT fileID 
            FROM File
            WHERE location = ?
            ORDER BY fileID DESC LIMIT 1'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (filename,))
        conn.commit()
        result = c.fetchone()
    return result["fileID"]


def delete_assignment(assignmenID):
    sql = '''DELETE FROM Assignment WHERE assignmentID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (assignmenID,))
        conn.commit()


def close():
    if conn:
        conn.close()

