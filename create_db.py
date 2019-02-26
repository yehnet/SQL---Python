import sqlite3
import os
import sys

def main(args):
    databaseexisted = os.path.isfile('schedule.db')

    dbcon = sqlite3.connect('schedule.db')
    with dbcon:
        cursor = dbcon.cursor()
        if not databaseexisted: # First time creating the database. Create the tables
            cursor.execute("CREATE TABLE students(grade TEXT PRIMARY KEY, count INTEGER NOT NULL);") #create table students
            cursor.execute("CREATE TABLE classrooms(id INTEGER PRIMARY KEY, location TEXT NOT NULL, current_course_id INTEGER NOT NULL, current_course_time_left INTEGER NOT NULL);") #create table classrooms
            cursor.execute("CREATE TABLE courses(id INTEGER PRIMARY KEY, course_name TEXT NOT NULL, student TEXT NOT NULL, number_of_students INTEGER NOT NULL, class_id INTEGER REFERENCES classrooms(id), course_length INTEGER NOT NULL);") #create table courses
            inputfilename = args[1]
            with open(inputfilename) as inputfile:
                for line in inputfile:
                    command = line.split(',')
                    vType = command[0].strip()
                    if vType == 'C':
                        vID = command[1].strip()
                        vCourseName = command[2].strip()
                        vStudent = command[3].strip()
                        vNumOfStuds = command[4].strip()
                        vClassId = command[5].strip()
                        vCourseLen = command[6].strip()
                        cursor.execute("INSERT INTO courses(id, course_name, student, number_of_students, class_id, course_length) VALUES (?,?,?,?,?,?);", (vID,vCourseName,vStudent,vNumOfStuds,vClassId,vCourseLen,))
                    if vType == 'S':
                        vGrade = command[1].strip()
                        vCount = command[2].strip()
                        cursor.execute("INSERT INTO students(grade, count) VALUES (?,?);", (vGrade,vCount,))
                    if vType == 'R':
                        vId = command[1].strip()
                        vLocation = command[2].strip()
                        cursor.execute("INSERT INTO classrooms(id, location, current_course_id, current_course_time_left) VALUES (?,?,0,0);",(vId,vLocation,)) 
            #print the tables
            print('courses')
            cursor.execute("SELECT * FROM courses")
            coursesList = cursor.fetchone()
            while not coursesList == None:
                print(coursesList)
                coursesList = cursor.fetchone()
            print('classrooms')
            cursor.execute("SELECT * FROM classrooms")
            classroomsList = cursor.fetchone()
            while not classroomsList == None:
                print(classroomsList)
                classroomsList = cursor.fetchone()
            print("students")
            cursor.execute("SELECT * FROM students")
            studentsList = cursor.fetchone()
            while not studentsList == None:
                print(studentsList)
                studentsList = cursor.fetchone()
            return    
        else :
            return
            
if __name__ == '__main__':
    main(sys.argv)
