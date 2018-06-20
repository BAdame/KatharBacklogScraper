import re
import unittest
from html_to_text import Renderer

def render(html):
    '''
    convenience method for changing the renderer in test
    '''
    return Renderer().html_to_text_h2t(html)

class TestRendering(unittest.TestCase):
    '''
    Tests for different edge cases in rendering
    '''
    def test_text_newlines_noNewlinesInOutput(self):
        html = '1\n2'
        self.assertEqual(render(html), '1 2')

    def test_list_noNewlines_newlinesInOutput(self):
        html = '<ul><li>1</li><li>2</li></ul>'
        matches = re.findall('1[^\n]*\n[^2]*2', render(html))
        print(render(html))
        self.assertEqual(len(matches), 1)

    def test_list_withNewlines_newlinesInOutput(self):
        html = '<ul>\n<li>1</li>\n<li>2</li>\n</ul>'
        matches = re.findall('1[^\n]*\n[^2]*2', render(html))
        print(render(html))
        self.assertEqual(len(matches), 1)

    def test_font_noNewlines_noNewlinesInOutput(self):
        html = '<font>1</font><font>2</font>'
        self.assertEqual(render(html), '12')

    def test_font_withNewlines_noNewlinesInOutput(self):
        html = '<font>1</font>\n<font>2</font>'
        self.assertEqual(render(html), '1 2')

    def test_emChar_noNewlines_noNewlinesInOutput(self):
        html = '1&#151;2'
        # Make sure special characters don't insert newlines
        matches = re.findall('1[^\n]{1,5}2', render(html))
        self.assertEqual(len(matches), 1)

    def test_table_withNewlines_newlinesBetweenRowsAndNotCells(self):
        html = '<table><tr>\n<td>11</td>\n<td>12</td>\n</tr>\n<tr><td>21</td>\n<td>22</td></tr></table>'
        # '11' and '12' should be on the same line, '21' and '22' should be on the next line
        matches = re.findall('11[^\n0-9]+12[^\n]+\n[^n0-9]+21[^\n0-9]+22', render(html))
        print(render(html))
        self.assertEqual(len(matches), 1)

    def test_table_noNewlines_newlinesBetweenRowsAndNotCells(self):
        html = '<table><tr><td>11</td><td>12</td></tr><tr><td>21</td><td>22</td></tr></table>'
        # '11' and '12' should be on the same line, '21' and '22' should be on the next line
        matches = re.findall('11[^\n0-9]+12[^\n]+\n[^n0-9]+21[^\n0-9]+22', render(html))
        self.assertEqual(len(matches), 1)

    def test_sup_noNewlines_noNewlinesInOutput(self):
        html = '<p>1<sup>2</sup></p>'
        self.assertEqual(render(html), '12')


if __name__ == '__main__':
    unittest.main()
