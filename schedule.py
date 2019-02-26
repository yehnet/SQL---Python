import sqlite3
import os
import sys

def main(args):
    databaseexisted = os.path.isfile('schedule.db')
    if not databaseexisted:
        print("schedule.db not found")
        return #the database file does not exist
    
    dbcon = sqlite3.connect('schedule.db')
    with dbcon:
        cursor = dbcon.cursor()
        i = 0
        cursor.execute("SELECT count(*) as total FROM courses")
        data = cursor.fetchone()
        numOfCourses = int(data[0])
        while True:
            if numOfCourses > 0:
                cursor.execute("SELECT * FROM courses")
                coursesData = cursor.fetchall() # get a course
                classes = []
                for course in coursesData:
                    cursor.execute("SELECT * FROM classrooms WHERE id = (?)",(int(course[4]),))
                    classroom = cursor.fetchone() # get a free classroom
                    if classroom[2] == 0 and not (classroom[0] in classes): # classroom is free
                        print("(" + str(i) + ") " + classroom[1] + ": " + course[1] + " is schedule to start")
                        cursor.execute("UPDATE classrooms SET current_course_id = (?) ,current_course_time_left = (?) WHERE id = (?)",(course[0],course[5],course[4])) # enter the course into the classroom
                        cursor.execute("SELECT count FROM students WHERE grade = (?)",(course[2],))
                        countOfStudents = cursor.fetchone()
                        cursor.execute("UPDATE students SET count = (?) WHERE grade = (?)",(int(countOfStudents[0])-int(course[3]),course[2] )) # remove the number of the students who taking this course
                        classes.append(classroom[0])
                    elif classroom[3] == 1 and not (classroom[0] in classes) : #classroom is occupied, check if course is done
                        print("(" + str(i) + ") " + classroom[1] + ": " + course[1] + " is done")
                        cursor.execute("DELETE FROM courses WHERE id = (?) ", (course[0],)) # delete the course from the table
                        numOfCourses -=1
                        cursor.execute("UPDATE classrooms SET current_course_id = 0 , current_course_time_left = 0 WHERE current_course_id = (?)", (course[0],))
                    elif not (classroom[0] in classes):
                        cursor.execute("SELECT course_name FROM courses WHERE id = (?) ",(classroom[2],))
                        occupyCourse = cursor.fetchone()
                        print("(" + str(i) + ") " + classroom[1] + ": occupied by " + occupyCourse[0] )
                        cursor.execute("UPDATE classrooms SET current_course_time_left = (?) WHERE id = (?)",(classroom[3] - 1,course[4],))  # minus 1 for time left   
                        classes.append(classroom[0])
            i+=1
            #print the updated tables.
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
            if numOfCourses == 0 :
                return #no courses left
            
if __name__ == '__main__':
    main(sys.argv)
