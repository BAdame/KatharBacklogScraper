from bs4 import BeautifulSoup
import html2text


class Renderer:
    def __init__(self):
        h2t = html2text.HTML2Text()
        self.h2t = h2t
        h2t.body_width = 0 # No wrap
        h2t.ignore_emphasis = True
        h2t.ignore_links = True
        h2t.ignore_images = True
        h2t.ignore_tables = False
        h2t.mark_code = False
        h2t.pad_tables = False
        h2t.skip_internal_links = True
        h2t.unicode_snob

    def html_to_text_bs(self, html):
        # BS doesn't handle newlines properly, this hack seems to fix it.
        data_file_html_dom_object = BeautifulSoup(html, 'lxml')
        data_file_raw_text = "\n".join([text.replace("\n", " ") for text in data_file_html_dom_object.stripped_strings])
        return data_file_raw_text.encode('ascii', 'ignore').decode('ascii').lower()

    def html_to_text_h2t(self, html):
        # html2text always appends an extra newlines, remove them
        return self.h2t.handle(html)[0 : -1]
