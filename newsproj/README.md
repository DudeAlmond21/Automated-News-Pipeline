# News Automator

Fetches top news headlines via NewsAPI and maintains a persistent
rolling archive with duplicate detection.

## Setup

1. Get a free API key at https://newsapi.org/register
2. Install dependencies:
   pip install -r requirements.txt
3. Add your key to config.txt:
   api_key = your_actual_key_here
4. Run:
   python news.py

## Config options (config.txt)

| Key     | Description                        | Example       |
|---------|------------------------------------|---------------|
| api_key | Your NewsAPI key                   | abc123...     |
| topic   | Search keyword for headlines       | technology    |
| country | Two-letter country code            | us / in / gb  |

## Output files

| File              | Description                              |
|-------------------|------------------------------------------|
| news_archive.txt  | Rolling log — headlines appended daily   |
| daily_summary.txt | Today's digest — overwritten each run    |

## File operations used

| Operation          | Where                                         |
|--------------------|-----------------------------------------------|
| read()             | Load full config.txt into string              |
| readlines()        | Load all archive lines for dedup check        |
| readline()         | Read header lines from summary after seek     |
| write()            | Write summary header and each article entry   |
| writelines()       | Batch-write archive section header and entries|
| seek(0)            | Rewind archive to scan for today's section    |
| seek(0, 2)         | Jump to end of archive to measure file size   |
| tell()             | Report current file pointer position          |
| append mode ("a")  | Add new entries without overwriting archive   |
| write mode ("w")   | Overwrite summary file each run               |
