#!/usr/bin/env python

"""
HW10_Anshul_Kapoor.py
"""

__author__ = "Anshul Kapoor"

import os
import sqlite3
from collections import defaultdict
from collections import Counter
from prettytable import PrettyTable

class Repository:
    def __init__(self, path):
        """ init class operation """
        self.path = path
        self.grade_file_header = True
        self.grade_file_fields = 4
        self.grade_file_sep = '|'
        self.students_file_path = os.path.join(self.path, "students.txt")
        self.instructors_file_path = os.path.join(self.path, "instructors.txt")
        self.grades_file_path = os.path.join(self.path, "grades.txt")
        self.majors_file_path = os.path.join(self.path, "majors.txt")
        self.passing_grade_list = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']
        self.students_file_analysis_container = (Student(self.students_file_path, 3, sep=';', header=True)).students_summary
        self.instructors_file_analysis_container = (Instructor(self.instructors_file_path, 3, sep='|', header=True)).instructors_summary
        self.majors_files_analysis_container = (Majors(self.majors_file_path, 3, sep='\t', header=True)).majors_summary
        self.grades_reading_gen()

    def grades_reading_gen(self):
        """ Grades File Reading Operation which reads Data from it
            and update the containers of DefaultDicts of Student_summary
            and Instructor_summary respectively """
        grades_summary_dict = {}
        grades_summary_dict_i = {}
        grades_summary_list = list()
        file_name = self.grades_file_path
        try:
            fp = open(file_name, 'r', encoding='utf-8')
        except FileNotFoundError as file_not_found:
            raise file_not_found
        else:
            with fp:
                line_count = 0
                if self.grade_file_header is True:
                    next(fp)
                line = fp.readline().strip('\r\n')
                while line:
                    i = 0
                    line_count += 1
                    grades_summary_list.clear()
                    current_line = line.strip().split(self.grade_file_sep)
                    if len(current_line) != self.grade_file_fields:
                        raise ValueError(f"{os.path.basename(self.grades_file_path)} has {len(current_line)} fields on line {line_count} but expected {self.grade_file_fields}")
                    while i < self.grade_file_fields:
                        grades_summary_list.append(current_line[i])
                        i = i + 1

                    if grades_summary_list[0] not in grades_summary_dict:
                        grades_summary_dict[grades_summary_list[0]] = []
                    grades_summary_dict[grades_summary_list[0]] += [{"Course": grades_summary_list[1],
                                                                     "Grade": grades_summary_list[2],
                                                                     "Instructor": grades_summary_list[3]}]

                    if grades_summary_list[3] not in grades_summary_dict_i:
                        grades_summary_dict_i[grades_summary_list[3]] = []
                    grades_summary_dict_i[grades_summary_list[3]] += [grades_summary_list[1]]

                    line = fp.readline().strip('\r\n')

            for key, value in grades_summary_dict.items():
                report = defaultdict(str)
                for i in range(len(value)):
                    if value[i]['Course'] not in report:
                        report[value[i]['Course']] = value[i]['Grade']
                try:
                    self.students_file_analysis_container[key]['container'] = report
                except KeyError:
                    print("***************************************************")
                    print(f"No Student found in Database with CWID : {key}")
                    print("***************************************************")


            for key, value in self.students_file_analysis_container.items():
                if value['major'] not in self.majors_files_analysis_container:
                    raise ValueError
                else:
                    completed_subject_taken_list = []
                    remaining_electives = self.majors_files_analysis_container[value['major']]["Electives"]
                    remaining_required = self.majors_files_analysis_container[value['major']]["Required"]
                    for subject, grade in (value['container']).items():
                        if grade in self.passing_grade_list:
                            completed_subject_taken_list.append(subject)
                            if subject in remaining_electives:
                                remaining_electives = ["None"]

                    completed_subject_taken_list.sort()

                    for sub in completed_subject_taken_list:
                        remaining_required = [x for x in remaining_required if x != sub]

                    remaining_required.sort()

                    self.students_file_analysis_container[key]["completed"] = completed_subject_taken_list
                    self.students_file_analysis_container[key]["remaining required"] = remaining_required
                    self.students_file_analysis_container[key]["remaining electives"] = remaining_electives

            for key, value in grades_summary_dict_i.items():
                try:
                    self.instructors_file_analysis_container[key]['container'] = dict(Counter(value))
                except KeyError:
                    print("***************************************************")
                    print(f"No Instructor found in Database with CWID : {key}")
                    print("***************************************************")


    def pretty_print_students(self):
        """  Pretty Print Students Summary  """
        table = PrettyTable()
        table.field_names = ["CWID", "Name", "Major", "Completed Courses", "Remaining Required", "Remaining Electives"]

        for key, value in self.students_file_analysis_container.items():
            table.add_row([key, value['name'], value['major'], value['completed'], value['remaining required'], value['remaining electives']])

        return table

    def pretty_print_instructors(self):
        """  Pretty Print Instructors Summary  """
        table = PrettyTable()
        table.field_names = ["CWID", "Name", "Dept", "Course", "Students"]

        for key, value in self.instructors_file_analysis_container.items():
            cwid = key
            name = value['name']
            dept = value['department']
            if value['container']:
                for key1, value1 in value['container'].items():
                    table.add_row([cwid, name, dept, key1, value1])
            # else:
            #     table.add_row([cwid, name, dept, "None", "None"])

        return table

    def pretty_print_majors(self):
        """  Pretty Print Instructors Summary  """
        table = PrettyTable()
        table.field_names = ["Dept", "Required", "Electives"]

        for key, value in self.majors_files_analysis_container.items():
            dept = key
            req = value["Required"]
            elec = value["Electives"]
            table.add_row([dept, req, elec])

        return table

class Majors:
    """ Class to instantiate the Students Summary """
    def __init__(self, path, fields, sep='\t', header=False):
        """ init class operation """
        self.path = path
        self.fields = fields
        self.sep = sep
        self.header = header
        self.majors_summary = dict()
        self.major_reading_gen()

    def major_reading_gen(self):
        """ Function for student file reading """
        majors_summary_dict = {}
        majors_summary_list = list()
        file_name = self.path
        try:
            fp = open(file_name, 'r', encoding='utf-8')
        except FileNotFoundError as file_not_found:
            raise file_not_found
        else:
            with fp:
                line_count = 0
                if self.header is True:
                    next(fp)
                line = fp.readline().strip('\r\n')
                while line:
                    i = 0
                    line_count += 1
                    majors_summary_list.clear()
                    current_line = line.strip().split(self.sep)
                    if len(current_line) != self.fields:
                        raise ValueError(
                            f"{os.path.basename(self.path)} has {len(current_line)} fields on line {line_count} but expected {self.fields}")
                    while i < self.fields:
                        majors_summary_list.append(current_line[i])
                        i = i + 1

                    if majors_summary_list[0] not in majors_summary_dict:
                        if majors_summary_list[1] == "R":
                            majors_summary_dict[majors_summary_list[0]] = {"Required": [majors_summary_list[2]], "Electives": []}
                        elif majors_summary_list[1] == "E":
                            majors_summary_dict[majors_summary_list[0]] = {"Required": [], "Electives": [majors_summary_list[2]]}
                    else:
                        if majors_summary_list[1] == "R":
                            majors_summary_dict[majors_summary_list[0]]["Required"] += [majors_summary_list[2]]
                        elif majors_summary_list[1] == "E":
                            majors_summary_dict[majors_summary_list[0]]["Electives"] += [majors_summary_list[2]]

                    line = fp.readline().strip('\r\n')

            self.majors_summary = majors_summary_dict

class Instructor:
    """ Class to instantiate the Instructor Summary """
    def __init__(self, path, fields, sep='\t', header=False):
        """ init class operation """
        self.path = path
        self.fields = fields
        self.sep = sep
        self.header = header
        self.instructors_summary = dict()
        self.instructors_reading_gen()

    def instructors_reading_gen(self):
        """ Function for instructor file reading """
        instructors_summary_dict = {}
        instructors_summary_list = list()
        file_name = self.path
        try:
            fp = open(file_name, 'r', encoding='utf-8')
        except FileNotFoundError as file_not_found:
            raise file_not_found
        else:
            with fp:
                line_count = 0
                if self.header is True:
                    next(fp)
                line = fp.readline().strip('\r\n')
                while line:
                    i = 0
                    line_count += 1
                    instructors_summary_list.clear()
                    current_line = line.strip().split(self.sep)
                    if len(current_line) != self.fields:
                        raise ValueError(
                            f"{os.path.basename(self.path)} has {len(current_line)} fields on line {line_count} but expected {self.fields}")
                    while i < self.fields:
                        instructors_summary_list.append(current_line[i])
                        i = i + 1

                    instructors_summary_dict[instructors_summary_list[0]] = {"name": instructors_summary_list[1], "department": instructors_summary_list[2], "container": defaultdict(int)}

                    line = fp.readline().strip('\r\n')

            self.instructors_summary = instructors_summary_dict

class Student:
    """ Class to instantiate the Students Summary """
    def __init__(self, path, fields, sep=';', header=True):
        """ init class operation """
        self.path = path
        self.fields = fields
        self.sep = sep
        self.header = header
        self.students_summary = dict()
        self.student_reading_gen()

    def student_reading_gen(self):
        """ Function for student file reading """
        students_summary_dict = {}
        students_summary_list = list()
        file_name = self.path
        try:
            fp = open(file_name, 'r', encoding='utf-8')
        except FileNotFoundError as file_not_found:
            raise file_not_found
        else:
            with fp:
                line_count = 0
                if self.header is True:
                    next(fp)
                line = fp.readline().strip('\r\n')
                while line:
                    i = 0
                    line_count += 1
                    students_summary_list.clear()
                    current_line = line.strip().split(self.sep)
                    if len(current_line) != self.fields:
                        raise ValueError(
                            f"{os.path.basename(self.path)} has {len(current_line)} fields on line {line_count} but expected {self.fields}")
                    while i < self.fields:
                        students_summary_list.append(current_line[i])
                        i = i + 1

                    students_summary_dict[students_summary_list[0]] = {"name": students_summary_list[1],
                                                                       "major": students_summary_list[2],
                                                                       "remaining required": list(),
                                                                       "remaining electives": list(),
                                                                       "completed": list(),
                                                                       "container": defaultdict(str)}

                    line = fp.readline().strip('\r\n')

            self.students_summary = students_summary_dict

def main():
    stevens_dir = "/Users/django/PycharmProjects/810A/University-Data-Repository-Manager/stevens"

    try:
        stevens = Repository(stevens_dir)
        print("\nMajors Summary")
        print(stevens.pretty_print_majors())
        print("\nStudent Summary")
        print(stevens.pretty_print_students())
        print("\nInstructor Summary")
        print(stevens.pretty_print_instructors())

    except FileNotFoundError:
        print(f"No Directory found at path --> {stevens_dir}")


if __name__ == '__main__':
    main()
