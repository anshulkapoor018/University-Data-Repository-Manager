#!/usr/bin/env python

"""
HW11_Test_Anshul_Kapoor.py
This Script demonstrates the use-case of
import statements and code segregation
for logic and unitTests in different files
"""

__author__ = "Anshul Kapoor"

import unittest
from HW11_Anshul_Kapoor import Repository


class TestRepository(unittest.TestCase):
    def test_repository(self):
        """ Testing Class Repository """
        repo = Repository("/Users/django/PycharmProjects/810A/University-Data-Repository-Manager/stevens db files")

        student_name_list = list()
        student_major_list = list()
        student_completed_course_list = list()
        student_remaining_course_list = list()
        student_remaining_electives_list = list()

        instructor_name_list = list()
        instructor_dept_list = list()
        instructor_courses_taught_list = list()

        for j in repo.students_file_analysis_container.values():
            student_name_list.append(j["name"])
            student_major_list.append(j["major"])
            student_completed_course_list.append(j["completed"])
            student_remaining_course_list.append(j["remaining required"])
            student_remaining_electives_list.append(j["remaining electives"])

        for j in repo.instructors_file_analysis_container.values():
            instructor_name_list.append(j["name"])
            instructor_dept_list.append(j["department"])
            instructor_courses_taught_list.append(list(j["container"]))

        # Testing Student Summary Data of Repo Instance
        self.assertEqual(student_name_list, ['Jobs, S', 'Bezos, J', 'Musk, E', 'Gates, B'])

        self.assertEqual(student_major_list, ['SFEN', 'SFEN', 'SFEN', 'CS'])

        self.assertEqual(student_completed_course_list, [['CS 501', 'SSW 810'], ['SSW 810'],
                                                         ['SSW 555', 'SSW 810'], ['CS 546', 'CS 570', 'SSW 810']])
        self.assertEqual(student_remaining_course_list, [['SSW 540', 'SSW 555'], ['SSW 540', 'SSW 555'],
                                                         ['SSW 540'], []])

        self.assertEqual(student_remaining_electives_list, [['None'], ['CS 501', 'CS 546'],
                                                            ['CS 501', 'CS 546'], ['None']])

        # Testing Instructor Summary Data of Repo Instance
        self.assertEqual(instructor_name_list, ['Cohen, R', 'Rowland, J', 'Hawking, S'])

        self.assertEqual(instructor_dept_list, ['SFEN', 'SFEN', 'CS'])

        self.assertEqual(instructor_courses_taught_list, [['CS 546'], ['SSW 810', 'SSW 555'], ['CS 501', 'CS 546', 'CS 570']])

        # # Testing Major Summary Data of Repo Instance
        self.assertEqual(repo.majors_files_analysis_container, {'SFEN': {'Required': ['SSW 540', 'SSW 810', 'SSW 555'],
                                                                         'Electives': ['CS 501', 'CS 546']},
                                                                'CS': {'Required': ['CS 570', 'CS 546'],
                                                                       'Electives': ['SSW 810', 'SSW 565']}})

        # Testing for DirectoryNotFound
        with self.assertRaises(FileNotFoundError):
            Repository("/Users/django/PycharmProjects/810A/stevens_not_exists")


if __name__ == '__main__':
    unittest.main(exit=False, verbositiy=2)
