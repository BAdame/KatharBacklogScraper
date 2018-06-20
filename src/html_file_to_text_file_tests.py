import unittest
from html_file_to_text_file import remove_content_block_by_type, remove_content_block_by_element


class TestRendering(unittest.TestCase):
    '''
    Tests for different edge cases in rendering
    '''
    def test_valid_tag_not_removed(self):
        html = '1<TYPE>valid \n <TEXT>\nZZZ\n</TEXT>2'
        self.assertEqual(html, remove_content_block_by_type(html, 'type'))


    def test_one_to_remove(self):
        html = '1<TYPE>EX-99.2 \n <TEXT>\nZZZ\n</TEXT>2'
        self.assertEqual('12', remove_content_block_by_type(html, 'EX-99.2'))


    def test_two_to_remove(self):
        html = '1<TYPE>type \n <TEXT>\nZZZ\n</TEXT>2<TYPE>type \n <TEXT>\nZZZ\n</TEXT>3'
        self.assertEqual('123', remove_content_block_by_type(html, 'type'))


    def test_two_to_remove_element(self):
        html = '1<TYPE>type <PDF>\nZZZ\n</PDF>2<PDF>type \n </PDF>3'
        self.assertEqual('1<TYPE>type 23', remove_content_block_by_element(html, 'PDF'))


    def test_one_to_remove_element(self):
        html = '1<PDF>slkafjkljsaf</PDF>2'
        self.assertEqual('12', remove_content_block_by_element(html, 'PDF'))


if __name__ == '__main__':
    unittest.main()
