import unittest
from queue import Queue

from bears.general.AnnotationBear import (find_start_end,
                                          find_singleline_comments,
                                          in_ranges,
                                          calc_line_col,
                                          AnnotationBear)
from coalib.results.SourceRange import SourceRange
from coalib.settings.Section import Section
from tests.LocalBearTestHelper import execute_bear
from coalib.settings.Setting import Setting


class AnnotationBearTest(unittest.TestCase):

    def setUp(self):
        self.section = Section("")
        self.section.append(Setting('language', 'c'))
        self.section.append(Setting('language_family', 'c'))

    def assertRange(self, file, uut, sourcerange):
        with execute_bear(uut, "filename", file) as results:
            print("results", results)
            for result in results:
                for code in result.contents:
                    self.assertEqual(code.start.line, sourcerange.start.line)
                    self.assertEqual(code.start.column,
                                     sourcerange.start.column)
                    self.assertEqual(code.end.line, sourcerange.end.line)
                    self.assertEqual(code.end.column, sourcerange.end.column)
            self.assertNotEqual(results, [])

    def assertEmpty(self, file, uut):
        with execute_bear(uut, "filename", file) as results:
            for result in results:
                self.assertEqual((), result.contents)

    def test_comments(self):
        file = """comments\n/*in line2*/,  \n"""
        uut = AnnotationBear(self.section, Queue())
        sourcerange = SourceRange.from_values("filename", 2, 1, 2, 13)
        self.assertRange(file, uut, sourcerange)

        file = """comments \n/*"then a string in comment"*/"""
        sourcerange = SourceRange.from_values("filename", 2, 1, 2, 31)
        self.assertRange(file, uut, sourcerange)

        file = """ this line has a //comment """
        sourcerange = SourceRange.from_values("filename", 1, 18, 1, 29)
        self.assertRange(file, uut, sourcerange)

        file = """ this is a //comment 'has a string' \n nextline """
        sourcerange = SourceRange.from_values("filename", 1, 12, 1, 37)
        self.assertRange(file, uut, sourcerange)

        file = """ i have a comment /* and a //comment inside a comment*/ """
        sourcerange = SourceRange.from_values("filename", 1, 19, 1, 56)
        self.assertRange(file, uut, sourcerange)

    def test_string(self):
        section = Section("")
        section.append(Setting('language', 'python3'))
        section.append(Setting('language_family', 'python3'))
        uut = AnnotationBear(section, Queue())
        file = """ strings: "only string" """
        sourcerange = SourceRange.from_values("filename", 1, 11, 1, 24)
        self.assertRange(file, uut, sourcerange)

        file = """ strings: " #then a comment in string" """
        sourcerange = SourceRange.from_values("filename", 1, 11, 1, 39)
        self.assertRange(file, uut, sourcerange)

        file = ' """Trying a multinline string""" '
        sourcerange = SourceRange.from_values("filename", 1, 2, 1, 34)
        self.assertRange(file, uut, sourcerange)

        file = """ i have a string: " and a 'string' inside a string" """
        sourcerange = SourceRange.from_values("filename", 1, 19, 1, 52)
        self.assertRange(file, uut, sourcerange)

        file = """ i have a string: " and a ''' multinline string'''
                   inside a string" """
        sourcerange = SourceRange.from_values("filename", 1, 19, 1, 60)

    def test_none(self):
        file = """no string or comments"""
        uut = AnnotationBear(self.section, Queue())
        self.assertEmpty(file, uut)

    def test_find_start_end(self):
        text = "Finding 'between \\'escaped strings'"
        self.assertEqual(find_start_end(text, {"'": "'"}, escape=True),
                         ((8, 35),))
        text = """We don't escape/* comments\\*/"""
        self.assertEqual(find_start_end(text, {"/*": "*/"}),
                         ((15, 29),))

        text = """contains 'multiple \\' \\'strings ' , 'escaped' """
        self.assertEqual(find_start_end(text, {"'": "'"},  escape=True),
                         ((9, 33), (36, 45)))

        self.assertEqual(find_start_end(text, {"'": "'"},  escape=False),
                         ((9, 21), (23, 33), (36, 45)))

    def test_find_single_line_comments(self):
        text = "we have a comment #here and it spans upto \n end of line"
        self.assertEqual(find_singleline_comments(text, ["#"]), ((18, 42),))

        text = "we have a comment #here and it spans upto end of text"
        self.assertEqual(find_singleline_comments(text, ["#"]), ((18, 54),))

        text = "we have a #comment here\n #and here, this one spans"
        "upto end of text"
        self.assertEqual(find_singleline_comments(text, ["#"]),
                         ((10, 23), (25, 51)))

    def test_in_ranges(self):
        # test not in any range
        self.assertFalse(in_ranges(((5, 10), (20, 30), (40, 50)), (11, 19)))

        #test in range
        self.assertTrue(in_ranges(((5, 10), (20, 30), (40, 50)), (46, 54)))

        # test Same start and in range
        self.assertTrue(in_ranges(((5, 10), (20, 30), (40, 50)), (5, 9)))

        # test same start and out of range
        self.assertFalse(in_ranges(((5, 10), (20, 30), (40, 50)), (5, 11)))

    def test_calc_line_col(self):
        # no newlines
        text = "find position of 'z'"
        z_pos = text.find('z')
        self.assertEqual(calc_line_col(text, z_pos), (1, z_pos+1))

        # newline
        text = "find position of\n'z'"
        z_pos = text.find('z')
        self.assertEqual(calc_line_col(text, z_pos), (2, 2))
