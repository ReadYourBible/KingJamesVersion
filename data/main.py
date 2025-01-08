#!/usr/bin/env python3

from bible_gateway_scraper import SessionManager, VerseExtractor

def main():
	# Initialize the session and fetch the page
	base_url = "https://www.biblegateway.com"
	path = f"/passage/?search=Revelation%201&version=KJV"
	session_manager = SessionManager(base_url)
	page_content = session_manager.fetch_page(path)
	
	# Extract verses
	extractor = VerseExtractor(page_content)
	container = extractor.get_text_container()
	
	if container:
		verses = []
		
		# Extract the first verse
		first_verse = extractor.extract_first_verse(container)
		if first_verse:
			verses.append(first_verse)
			
		# Extract the rest of the verses
		verses.extend(extractor.extract_all_verses(container))
		
		# Print or process the verses
		for verse in verses:
			print(verse)
	else:
		print("No verses found!")
		
if __name__ == "__main__":
	main()
	