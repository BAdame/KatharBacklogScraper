import unittest
from analyzing_rules import get_blog_quant_table


class TestRendering(unittest.TestCase):

    def test_blog_quant_two_digits_does_not_match(self):
        text = 'backlog in 20, more'
        self.assertEqual(0, get_blog_quant_table(text, [0]))


    def test_blog_quant_table_out_of_range_no_match(self):
        text = 'backlog 1234567890 1234567890'
        self.assertEqual(0, get_blog_quant_table(text, [0], 20))


    def test_blog_quant_table_year_does_not_match(self):
        text = 'backlog in 2000, more'
        self.assertEqual(0, get_blog_quant_table(text, [0]))


    def test_blog_quant_table_three_digits_matches(self):
        text = 'backlog was 300.'
        self.assertEqual(1, get_blog_quant_table(text, [0]))


    '''
    Tests for different edge cases in rendering
    '''
    def test_blog_quant_table_four_digits_matches(self):
        text = 'backlog was 1,300.'
        self.assertEqual(1, get_blog_quant_table(text, [0]))


    '''
    Tests for different edge cases in rendering
    '''
    def test_blog_quant_table_seven_digits_matches(self):
        text = 'backlog was 1,111,300 .'
        self.assertEqual(1, get_blog_quant_table(text, [0]))


if __name__ == '__main__':
    unittest.main()
