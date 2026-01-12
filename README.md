# 🔄 Pealim-to-Anki ETL Pipeline

> An automated ETL (Extract, Transform, Load) pipeline that crawls Hebrew language data from [Pealim.com](https://pealim.com) and transforms it into flashcard-ready Anki notes for language learning.

[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![ETL Pipeline](https://img.shields.io/badge/pipeline-ETL-orange.svg)](https://en.wikipedia.org/wiki/Extract,_transform,_load)

## 📋 Project Overview

This ETL pipeline automates the extraction of Hebrew verb conjugations, noun declensions, adjectives, and prepositions from Pealim.com's comprehensive Hebrew dictionary. The data is then transformed into a structured format and loaded into Anki-compatible flashcards for efficient language learning.

### 🎯 Key Features

- **Automated Web Scraping**: Extracts conjugation tables and declension data from Pealim.com
- **Multi-Part-of-Speech Support**: Handles verbs, nouns, adjectives, and prepositions
- **HTML Template System**: Uses customizable HTML frames for different word types
- **Anki-Ready Output**: Generates tab-separated files compatible with Anki import
- **Error Handling**: Gracefully handles missing pages and edge cases
- **Robots.txt Compliant**: Respects website crawling policies

## 🏗️ ETL Architecture

### Extract
- **Source**: Pealim.com Hebrew dictionary (https://www.pealim.com/dict/{id}/)
- **Method**: HTTP requests using `requests` library
- **Parser**: BeautifulSoup4 for HTML parsing
- **Data Points**: Word meanings, conjugation tables, grammatical metadata

### Transform
- **Parsing Logic**: Extracts specific HTML elements based on part of speech
- **Template Matching**: Maps conjugation data to pre-defined HTML frames
- **Data Cleaning**: Removes unnecessary HTML attributes and formatting
- **Structure**: Converts nested HTML tables into linearized flashcard format

### Load
- **Output Format**: Tab-separated values (TSV)
- **File Structure**: `Hebrew.txt` with front/back card content
- **Encoding**: UTF-8 for proper Hebrew character support
- **Anki Import**: Direct import via Anki's import feature

## 📊 Data Flow

```
Pealim.com Dictionary
        ↓
   HTTP Request
        ↓
   HTML Response
        ↓
BeautifulSoup Parser
        ↓
Extract Conjugations
        ↓
  Match to Template
        ↓
  Format for Anki
        ↓
   Write to File
        ↓
   Hebrew.txt (TSV)
        ↓
   Import to Anki
```

## 🚀 Installation

### Prerequisites
- Python 3.6 or higher
- pip package manager

### Dependencies
```bash
pip install requests beautifulsoup4
```

### Clone Repository
```bash
git clone https://github.com/js4484821266/pealim-to-anki.git
cd pealim-to-anki
```

## 💻 Usage

### Basic Usage
```bash
python anki.py
```

The script will:
1. Check robots.txt compliance
2. Iterate through dictionary entries (configurable range)
3. Extract and transform each entry
4. Generate `Hebrew.txt` with flashcard data

### Configuration
Edit `anki.py` to modify the range of dictionary entries:
```python
for wsn in range(9123, 9125):  # Modify range as needed
```

### Output Format
Each line in `Hebrew.txt` contains:
```
[Front of Card]	[Back of Card]
```

Example:
```
09124<br>Verb<br>to write	[conjugation table HTML]
```

## 📁 Project Structure

```
pealim-to-anki/
├── anki.py                    # Main ETL script
├── frame-Verb.html            # Template for verb conjugations
├── frame-Noun.html            # Template for noun declensions
├── frame-Adjective.html       # Template for adjectives
├── frame-Preposition.html     # Template for prepositions
├── samples/                   # Sample HTML files for testing
├── Hebrew.txt                 # Generated output file
└── README.md                  # This file
```

## 🔧 Technical Details

### Supported Parts of Speech
- **Verbs**: Full conjugation tables (past, present, future, imperative)
- **Nouns**: Gender and number declensions
- **Adjectives**: Gender and number forms
- **Prepositions**: Prepositional forms

### HTML Template System
The pipeline uses predefined HTML frames that match the structure of Pealim.com's output:
- Each part of speech has a corresponding template
- Templates contain placeholder divs with specific IDs
- The scraper populates these divs with extracted data

### Error Handling
- Skips entries with HTTP errors (404, etc.)
- Handles missing conjugation tables gracefully
- Continues processing even if individual entries fail

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

- Add support for more parts of speech
- Improve error handling and logging
- Add unit tests
- Optimize scraping performance
- Enhance output formatting options

## ⚠️ Ethical Considerations

This project:
- Respects robots.txt directives
- Implements rate limiting to avoid overwhelming the source server
- Is intended for personal educational use
- Credits Pealim.com as the data source

Please use this tool responsibly and in accordance with Pealim.com's terms of service.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Pealim.com**: For providing comprehensive Hebrew language resources
- **Anki**: For the spaced repetition flashcard system
- The open-source community for the tools that make this pipeline possible

## 📞 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Note**: This is an educational ETL project demonstrating web scraping, data transformation, and integration with learning tools. Always respect the source website's terms of service and rate limits.
