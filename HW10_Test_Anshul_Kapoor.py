#!/usr/bin/env python

"""
HW10_Test_Anshul_Kapoor.py
This Script demonstrates the use-case of
import statements and code segregation
for logic and unitTests in different files
"""

__author__ = "Anshul Kapoor"

import unittest
from HW10_Anshul_Kapoor import Repository


class TestRepository(unittest.TestCase):
    def test_repository(self):
        """ Testing Class Repository """
        repo = Repository("/Users/django/PycharmProjects/810A/University-Data-Repository-Manager/stevens")

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
        self.assertEqual(student_name_list, ['Baldwin, C', 'Wyatt, X', 'Forbes, I', 'Erickson, D',
                                             'Chapman, O', 'Cordova, I', 'Wright, U', 'Kelly, P',
                                             'Morton, A', 'Fuller, E'])

        self.assertEqual(student_major_list, ['SFEN', 'SFEN', 'SFEN', 'SFEN', 'SFEN',
                                              'SYEN', 'SYEN', 'SYEN', 'SYEN', 'SYEN'])

        self.assertEqual(student_completed_course_list, [['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'],
                                                         ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'],
                                                         ['SSW 555', 'SSW 567'], ['SSW 564', 'SSW 567', 'SSW 687'],
                                                         ['SSW 689'], ['SSW 540'], ['SYS 611', 'SYS 750', 'SYS 800'],
                                                         [], ['SYS 611', 'SYS 645'], ['SSW 540']])
        self.assertEqual(student_remaining_course_list, [['SSW 540', 'SSW 555'],
                                                         ['SSW 540', 'SSW 555'],
                                                         ['SSW 540', 'SSW 564'],
                                                         ['SSW 540', 'SSW 555'],
                                                         ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'],
                                                         ['SYS 612', 'SYS 671', 'SYS 800'],
                                                         ['SYS 612', 'SYS 671'],
                                                         ['SYS 612', 'SYS 671', 'SYS 800'],
                                                         ['SYS 612', 'SYS 671', 'SYS 800'],
                                                         ['SYS 612', 'SYS 671', 'SYS 800']])

        self.assertEqual(student_remaining_electives_list, [['None'], ['None'],
                                                             ['CS 501', 'CS 513', 'CS 545'],
                                                             ['CS 501', 'CS 513', 'CS 545'],
                                                             ['CS 501', 'CS 513', 'CS 545'],
                                                             ['None'],
                                                             ['SSW 810', 'SSW 565', 'SSW 540'],
                                                             ['SSW 810', 'SSW 565', 'SSW 540'],
                                                             ['SSW 810', 'SSW 565', 'SSW 540'],
                                                             ['None']])

        # Testing Instructor Summary Data of Repo Instance
        self.assertEqual(instructor_name_list, ['Einstein, A', 'Feynman, R', 'Newton, I',
                                                'Hawking, S', 'Edison, A', 'Darwin, C'])

        self.assertEqual(instructor_dept_list, ['SFEN', 'SFEN', 'SFEN', 'SYEN', 'SYEN', 'SYEN'])

        self.assertEqual(instructor_courses_taught_list,
                         [['SSW 567', 'SSW 540'], ['SSW 564', 'SSW 687', 'CS 501', 'CS 545'],
                          ['SSW 555', 'SSW 689'], [], [], ['SYS 800', 'SYS 750', 'SYS 611', 'SYS 645']])

        # Testing Major Summary Data of Repo Instance
        self.assertEqual(repo.majors_files_analysis_container, {'SFEN': {'Required': ['SSW 540', 'SSW 564', 'SSW 555', 'SSW 567'],
                                                                         'Electives': ['CS 501', 'CS 513', 'CS 545']},
                                                                'SYEN': {'Required': ['SYS 612', 'SYS 671', 'SYS 800'],
                                                                         'Electives': ['SSW 810', 'SSW 565', 'SSW 540']}})

        # Testing for DirectoryNotFound
        with self.assertRaises(FileNotFoundError):
            Repository("/Users/django/PycharmProjects/810A/stevens_not_exists")


if __name__ == '__main__':
    unittest.main(exit=False, verbositiy=2)
