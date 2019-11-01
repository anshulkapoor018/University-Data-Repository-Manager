#!/usr/bin/env python

"""
HW09_Anshul_Kapoor.py
"""

__author__ = "Anshul Kapoor"

import os
from collections import defaultdict
from collections import Counter
from prettytable import PrettyTable

class Repository:
    def __init__(self, path):
        """ init class operation """
        self.path = path
        self.grade_file_header = False
        self.grade_file_fields = 4
        self.grade_file_sep = '\t'
        self.students_file_path = self.path + "/students.txt"
        self.instructors_file_path = self.path + "/instructors.txt"
        self.grades_file_path = self.path + "/grades.txt"
        self.students_file_analysis_container = (Student(self.students_file_path, 3, sep='\t', header=False)).students_summary
        self.instructors_file_analysis_container = (Instructor(self.instructors_file_path, 3, sep='\t', header=False)).instructors_summary
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
                self.students_file_analysis_container[key]['container'] = report

            for key, value in grades_summary_dict_i.items():
                self.instructors_file_analysis_container[key]['container'] = dict(Counter(value))

    def pretty_print_students(self):
        """  Pretty Print Students Summary  """
        table = PrettyTable()
        table.field_names = ["CWID", "Name", "Completed Courses"]

        for key, value in self.students_file_analysis_container.items():
            subject_list = list()
            cwid = key
            name = value['name']
            for item in value['container']:
                subject_list.append(item)
            subject_list.sort()

            table.add_row([cwid, name, subject_list])

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
            else:
                table.add_row([cwid, name, dept, "None", "None"])

        return table

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
    def __init__(self, path, fields, sep='\t', header=False):
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

                    students_summary_dict[students_summary_list[0]] = {"name": students_summary_list[1], "major": students_summary_list[2], "container": defaultdict(str)}

                    line = fp.readline().strip('\r\n')

            self.students_summary = students_summary_dict

def main():
    stevens_dir = "/Users/django/PycharmProjects/810A/University-Data-Repository-Manager/stevens"

    try:
        stevens = Repository(stevens_dir)
        print(stevens.pretty_print_students())
        print(stevens.pretty_print_instructors())
    except FileNotFoundError:
        print(f"No Directory found at path --> {stevens_dir}")


if __name__ == '__main__':
    main()
