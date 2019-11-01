#!/usr/bin/env python

"""
HW09_Test_Anshul_Kapoor.py
This Script demonstrates the use-case of
import statements and code segregation
for logic and unitTests in different files
"""

__author__ = "Anshul Kapoor"

import unittest
from HW09_Anshul_Kapoor import Repository


class TestRepository(unittest.TestCase):
    def test_repository(self):
        """ Testing Class Repository """
        repo = Repository("/Users/django/PycharmProjects/810A/University Data Manager/stevens")
        repo_first_year = Repository("/Users/django/PycharmProjects/810A/University Data Manager/stevens first year")

        new_student_name_list = list()
        new_major_name_list = list()
        new_course_completed_list = list()

        student_name_list = list()
        student_major_list = list()
        student_course_completed_list = list()

        instructor_name_list = list()
        instructor_dept_list = list()
        instructor_courses_taught_list = list()

        for j in repo_first_year.students_file_analysis_container.values():
            new_student_name_list.append(j["name"])
            new_major_name_list.append(j["major"])
            new_course_completed_list.append(list(j["container"]))

        for j in repo.students_file_analysis_container.values():
            student_name_list.append(j["name"])
            student_major_list.append(j["major"])
            student_course_completed_list.append(list(j["container"]))

        for j in repo.instructors_file_analysis_container.values():
            instructor_name_list.append(j["name"])
            instructor_dept_list.append(j["department"])
            instructor_courses_taught_list.append(list(j["container"]))

        # Testing Student Summary Data of repo_first_year Instance
        self.assertEqual(new_student_name_list, ['Baldwin, C', 'Wyatt, X', 'Forbes, I', 'Erickson, D',
                                                 'Chapman, O', 'Cordova, I', 'Wright, U', 'Kelly, P',
                                                 'Morton, A', 'Fuller, E'])

        self.assertEqual(new_major_name_list, ['SFEN', 'SFEN', 'SFEN', 'SFEN', 'SFEN',
                                               'SYEN', 'SYEN', 'SYEN', 'SYEN', 'SYEN'])

        """ Testing to check if some students will have no grades in grades.txt which 
            means they have not completed any course yet i.e. First Year Students   """
        self.assertEqual(new_course_completed_list, [[], ['SSW 567', 'SSW 564', 'SSW 687', 'CS 545'],
                                                     ['SSW 555', 'SSW 567'], ['SSW 567', 'SSW 564', 'SSW 687'],
                                                     ['SSW 689'], ['SSW 540'], ['SYS 800', 'SYS 750', 'SYS 611'],
                                                     ['SSW 540'], ['SYS 611', 'SYS 645'], []])

        # Testing Student Summary Data of Repo Instance
        self.assertEqual(student_name_list, ['Baldwin, C', 'Wyatt, X', 'Forbes, I', 'Erickson, D',
                                             'Chapman, O', 'Cordova, I', 'Wright, U', 'Kelly, P',
                                             'Morton, A', 'Fuller, E'])

        self.assertEqual(student_major_list, ['SFEN', 'SFEN', 'SFEN', 'SFEN', 'SFEN',
                                              'SYEN', 'SYEN', 'SYEN', 'SYEN', 'SYEN'])

        self.assertEqual(student_course_completed_list, [['SSW 567', 'SSW 564', 'SSW 687', 'CS 501'],
                                                         ['SSW 567', 'SSW 564', 'SSW 687', 'CS 545'],
                                                         ['SSW 555', 'SSW 567'],
                                                         ['SSW 567', 'SSW 564', 'SSW 687'],
                                                         ['SSW 689'],
                                                         ['SSW 540'],
                                                         ['SYS 800', 'SYS 750', 'SYS 611'],
                                                         ['SSW 540'],
                                                         ['SYS 611', 'SYS 645'],
                                                         ['SSW 540']])

        # Testing Instructor Summary Data of Repo Instance
        self.assertEqual(instructor_name_list, ['Einstein, A', 'Feynman, R', 'Newton, I',
                                                'Hawking, S', 'Edison, A', 'Darwin, C'])

        self.assertEqual(instructor_dept_list, ['SFEN', 'SFEN', 'SFEN', 'SYEN', 'SYEN', 'SYEN'])

        self.assertEqual(instructor_courses_taught_list,
                         [['SSW 567', 'SSW 540'], ['SSW 564', 'SSW 687', 'CS 501', 'CS 545'],
                          ['SSW 555', 'SSW 689'], [], [], ['SYS 800', 'SYS 750', 'SYS 611', 'SYS 645']])

        # Testing for DirectoryNotFound
        with self.assertRaises(FileNotFoundError):
            Repository("/Users/django/PycharmProjects/810A/stevens_not_exists")


if __name__ == '__main__':
    unittest.main(exit=False, verbositiy=2)
