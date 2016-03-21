import unittest

from bears.general.AnnotationBear import (find_start_end,
                                          find_singleline_comments,
                                          in_ranges,
                                          calc_line_col)


class AnnotationBearTest(unittest.TestCase):

    def setUp(self):
        pass

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
