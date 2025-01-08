from bs4 import BeautifulSoup
import requests

class SessionManager:
    """Handles HTTP sessions and requests."""
    def __init__(self, base_url):
        self.session = requests.Session()
        self.base_url = base_url

    def fetch_page(self, path):
        response = self.session.get(f"{self.base_url}{path}")
        response.raise_for_status()
        return response.text


class VerseExtractor:
    """Extracts verses from the HTML content."""
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, "html.parser")

    def get_text_container(self):
        """Find the main container div for the verses."""
        return self.soup.find("div", class_="version-KJV result-text-style-normal text-html")

    def extract_first_verse(self, container):
        """Extract the first verse using chapternum."""
        chapter_num = container.find("span", class_="chapternum")
        if chapter_num:
            return chapter_num.find_parent("span").get_text(separator=" ", strip=True)
        return None

    def extract_all_verses(self, container):
        """Extract all verses except the first."""
        verses = []
        for span in container.find_all("span", class_="text"):
            verse_number = span.find("sup", class_="versenum")
            verse_text = span.get_text(separator=" ", strip=True)
            if verse_number:
                verses.append(
                    f"{verse_number.text.strip()} {verse_text[len(verse_number.text.strip()):].strip()}"
                )
        return verses
