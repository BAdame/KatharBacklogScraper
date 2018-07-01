import unittest
from analyzing_rules import get_blog_quant_table, get_mentioner_names


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

    def test_get_mentioner_names_happy_case(self):
        text = '1\n2\n3\nFirst Name, [1]\n-----------\nbacklog'
        names = get_mentioner_names(text, [])
        self.assertEqual('First Name', names)

    def test_get_mentioner_names_no_separator(self):
        text = '1\n2\n3\nFirst Name, [1]\ntext\nbacklog'
        names = get_mentioner_names(text, [])
        self.assertEqual('', names)

    def test_get_mentioner_names_no_comma(self):
        text = '1\n2\n3\nFirst Name [1]\n-----------\nbacklog'
        names = get_mentioner_names(text, [])
        self.assertEqual('First Name', names)

    def test_get_mentioner_names_multiple_mentions(self):
        text = '1\n2\n3\nFirst Name, [1]\n-----------\nbacklog'
        text += '1\n2\n3\nSecond Name, [1]\n-----------\nbacklog'
        names = get_mentioner_names(text, [])
        self.assertEqual('First Name ; Second Name', names)


if __name__ == '__main__':
    unittest.main()
