#!/usr/bin/env python3

import os
import re
import sys

from time import sleep
from pathlib import Path
from collections import namedtuple
from bible_gateway_scraper import SessionManager, VerseExtractor


file_path = Path(__file__)
root_path = file_path.parent.parent


Book = namedtuple("Book", ["name", "chapters"])


books_data = [
    ("Genesis", 50), ("Exodus", 40), ("Leviticus", 27), ("Numbers", 36),
    ("Deuteronomy", 34), ("Joshua", 24), ("Judges", 21), ("Ruth", 4),
    ("I Samuel", 31), ("II Samuel", 24), ("I Kings", 22), ("II Kings", 25),
    ("I Chronicles", 29), ("II Chronicles", 36), ("Ezra", 10), ("Nehemiah", 13),
    ("Esther", 10), ("Job", 42), ("Psalms", 150), ("Proverbs", 31),
    ("Ecclesiastes", 12), ("Song of Solomon", 8), ("Isaiah", 66), ("Jeremiah", 52),
    ("Lamentations", 5), ("Ezekiel", 48), ("Daniel", 12), ("Hosea", 14),
    ("Joel", 3), ("Amos", 9), ("Obadiah", 1), ("Jonah", 4), ("Micah", 7),
    ("Nahum", 3), ("Habakkuk", 3), ("Zephaniah", 3), ("Haggai", 2),
    ("Zechariah", 14), ("Malachi", 4), ("Matthew", 28), ("Mark", 16),
    ("Luke", 24), ("John", 21), ("Acts", 28), ("Romans", 16),
    ("I Corinthians", 16), ("II Corinthians", 13), ("Galatians", 6),
    ("Ephesians", 6), ("Philippians", 4), ("Colossians", 4),
    ("I Thessalonians", 5), ("II Thessalonians", 3), ("I Timothy", 6),
    ("II Timothy", 4), ("Titus", 3), ("Philemon", 1), ("Hebrews", 13),
    ("James", 5), ("I Peter", 5), ("II Peter", 3), ("I John", 5),
    ("II John", 1), ("III John", 1), ("Jude", 1), ("Revelation", 22)
]


books = [Book(name, chapters) for name, chapters in books_data]


def create_book_dir(books: Book):
    for book in books:
        book_number = books.index(book) + 1
        book_number = str(book_number) if book_number >= 10 else "0" + str(book_number)        
        book_dir_name = f"{book_number}-{book.name.lower().replace(' ', '-')}"
        os.makedirs(root_path / book_dir_name, exist_ok=True)


def main():    
    base_url = "https://www.biblegateway.com"
    session_manager = SessionManager(base_url)

    create_book_dir(books)

    for book in books:

        book_number = books.index(book) + 1
        book_number = f"0{book_number}" if book_number < 10 else str(book_number)
        book_name_cleaned = book.name.lower().replace(" ", "-")
        book_dir_name = f"{book_number}-{book_name_cleaned}"

        for chapter in range(1, book.chapters + 1):
            chapter_number = f"0{chapter}" if chapter < 10 else str(chapter)
            file_name = f"{book_name_cleaned}-{chapter_number}.txt"
            print(file_name)
    
            book_name_encoded = book.name.replace(" ", "%20")
            page_path = f"/passage/?search={book_name_encoded}%20{chapter}&version=KJV"
            
            page_content = session_manager.fetch_page(page_path)
            
            # Extract verses
            extractor = VerseExtractor(page_content)
            container = extractor.get_text_container()
            
            if container:
                verses = []
                
                first_verse = extractor.extract_first_verse(container)
                if first_verse:
                    verses.append(first_verse)
                    
                verses.extend(extractor.extract_all_verses(container))
                

                # Process the verses (e.g., save to file, print, etc.)
                print(f"Book: {book.name}, Chapter: {chapter}")
                file_path = root_path / book_dir_name / file_name
                if not file_path.exists() or file_path.stat().st_size == 0:
                    for verse in verses:
                        cleaned_verse = re.sub(r"^\d+\s*", "", verse)
                        print(cleaned_verse)
                        
                        with open(file_path, "a") as file:
                            if verse == verses[-1]:
                                file.write(cleaned_verse)
                            else:
                                file.write(cleaned_verse + "\n")
                    else:
                        print(f"File {file_name} is not empty. Skipping.")
            else:
                print(f"No verses found for {book.name} Chapter {chapter}!")


if __name__ == "__main__":
    main()
    