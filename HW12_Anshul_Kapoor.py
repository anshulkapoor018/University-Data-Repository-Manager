#!/usr/bin/env python

"""
HW12_Anshul_Kapoor.py
Using Flask
"""

__author__ = "Anshul Kapoor"

from flask import Flask, render_template
import sqlite3
app = Flask(__name__)

@app.route('/instructor_courses')
def instructor_courses():
    dbpath = '/Users/django/PycharmProjects/810A/University-Data-Repository-Manager/repository.db'

    try:
        db = sqlite3.connect(dbpath)
    except sqlite3.OperationalError:
        return f"Error: Unable to open Database at - {dbpath}"
    else:
        query = """ SELECT Instructor_CWID, Name, Dept, Course, count(*) as Students
                    from instructors join grades
                    on instructors.CWID = grades.Instructor_CWID
                    group by instructors.Name, grades.Course
                    order by Instructor_CWID    """
        data1 = [{'cwid': cwid, 'name': name, 'dept': dept, 'courses': courses, 'students': students}
                 for cwid, name, dept, courses, students in db.execute(query)]
        # print(data1)
        db.close()

        return render_template(
            'instructor_courses.html',
            title='Stevens Repository',
            table_title='Number of Students by course and instructors',
            students=data1
        )


if __name__ == '__main__':
    app.run(debug=True)
