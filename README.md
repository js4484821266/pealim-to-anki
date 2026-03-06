# Pealim-to-Anki

A simple web scraper that extracts Hebrew word data from [Pealim.com](https://pealim.com) and converts it into Anki flashcards.

## What it does

This script scrapes Hebrew verb conjugations, noun declensions, adjectives, and prepositions from Pealim.com and creates a text file that can be imported into Anki for language learning.

## Requirements

- Python 3.6+

Install dependencies:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install requests beautifulsoup4
```

## Usage
```bash
python anki.py
```

This will create a `Hebrew.txt` file with tab-separated flashcard data that can be imported into Anki.

## Performance Improvement

For portfolio context, the average runtime was reduced from **2 minutes 54.49 seconds** to **17.97 seconds** (**89.70% faster**).

You can edit the range in `anki.py` to specify which dictionary entries to scrape:
```python
for wsn in range(9123, 9125):  # Change these numbers
```

## Files
- `anki.py` - Main script
- `frame-Verb.html` - Template for verbs
- `frame-Noun.html` - Template for nouns
- `frame-Adjective.html` - Template for adjectives
- `frame-Preposition.html` - Template for prepositions
- `Hebrew.txt` - Generated output file (created when you run the script, not tracked in git)

## Notes

- The script checks `robots.txt` before scraping using `urllib.robotparser`
- If `robots.txt` cannot be loaded or disallows access, the script skips that URL
- Rate limiting: 1 second delay between requests to avoid server overload
- Output is tab-separated format ready for Anki import
- For personal educational use only - please respect Pealim.com's terms of service

## License

MIT License

## Credits

- Data source: [Pealim.com](https://pealim.com)
- Anki flashcard system
