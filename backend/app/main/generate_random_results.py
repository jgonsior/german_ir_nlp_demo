from bs4 import BeautifulSoup
from random import randint
import re

FILENAME = '../data/deharrypotter_pages_current.xml'


class Randomizer:
    def __init__(self):

        with open(FILENAME) as f:
            soup = BeautifulSoup(f, 'xml')


        self.pages = soup.find_all('page')

    def preprocess(self, text):
        """
        some preprocessing because of the characters in xml file
        """
        replace_seq = [('\n', ' '), ("'''", ''), ('  ', ' ')]
        for r1, r2 in replace_seq:
            text = text.replace(r1, r2)

        remove_seq = [('[[', ']]'), ('{{', '}}'), ('<', '>'), ('==', '=='), ('|', '|')]
        for start_c, end_c in remove_seq:
            text = self.remove_between_regex(text, start_c, end_c)

        return text.strip().split('. ')


    def remove_between_regex(self, text, start_c, end_c):
        """
        Removes text between the given start and end characters (inclusive) using regular expressions.
        """
        pattern = re.escape(start_c) + r".*?" + re.escape(end_c)
        return re.sub(pattern, "", text)

    def get_result(self):
        """
        returns preprocessed text of a random page
        """
        page = self.pages[randint(0, len(self.pages)-1)].text
        sentences = self.preprocess(page)
        return sentences[randint(0, len(sentences)-1)]
