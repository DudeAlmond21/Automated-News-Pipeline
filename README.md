# Automated News Pipeline — Python

## Overview

This project is an **Automated News Pipeline** developed in **Python** that fetches the latest news headlines from the NewsAPI, removes duplicates using a persistent archive system, and generates a clean daily news summary automatically.

The script is designed to run without human interaction and demonstrates practical scripting concepts such as:

* File handling
* File pointer manipulation
* API integration
* Data processing
* Duplicate detection
* Error handling
* Automation workflows

The system maintains a growing archive of previously stored headlines while ensuring duplicate headlines are never added again.

---

## Features

* Fetches latest news headlines from NewsAPI
* Reads configuration from `config.txt`
* Automatically removes duplicate headlines
* Maintains a persistent news archive
* Generates a fresh daily summary file every run
* Uses file pointer manipulation with `seek()`
* Measures archive file size using `tell()`
* Handles API errors gracefully
* Fully automated and scheduler-friendly

---

## Technologies Used

* Python
* NewsAPI
* File Handling
* REST API Integration

---

## Project Workflow

### 1. Configuration Loading

The script reads:

* API Key
* Preferred news topic

from `config.txt` using:

```python id="6f2m1q"
f.read()
```

---

### 2. News Fetching

The script connects to the **NewsAPI** and retrieves:

* Latest 15 headlines
* Based on the configured topic

This demonstrates:

* External API communication
* Automated data retrieval

---

### 3. Duplicate Detection System

The script opens `news_archive.txt` using:

```python id="q2k7pv"
f.readlines()
```

It then:

* Loads all previously stored headlines
* Creates a set of archived titles
* Compares newly fetched headlines against existing ones
* Skips duplicates automatically

The script also demonstrates:

```python id="f5v8xc"
seek(0)
```

to rewind the file pointer before scanning the archive.

---

### 4. Writing and Updating Files

#### Archive Update

New headlines are appended using:

```python id="q0t5zr"
f.writelines()
```

#### Daily Summary

A fresh `daily_summary.txt` file is generated every run using:

```python id="v9c2ne"
f.write()
```

---

### 5. File Pointer Operations

The project demonstrates advanced file handling concepts:

* `seek(0)` → Rewind file pointer
* `seek(0, 2)` → Move pointer to end of file
* `tell()` → Measure archive size in bytes

---

## Project Structure

```bash id="e1w9mz"
├── main.py
├── config.txt
├── news_archive.txt
├── daily_summary.txt
├── requirements.txt
└── README.md
```

---

## Installation

Install required dependencies:

```bash id="r7n4vb"
pip install requests
```

---

## Configuration

Create a `config.txt` file:

```txt id="n6x2kt"
YOUR_NEWS_API_KEY
technology
```

Format:

1. First line → NewsAPI key
2. Second line → Preferred topic

---

## How to Run

Run the script:

```bash id="m8d4sy"
python main.py
```

The script will:

1. Fetch latest headlines
2. Remove duplicates
3. Update archive
4. Generate a daily summary

---

## Output Files

### `news_archive.txt`

* Permanent archive
* Stores all unique headlines
* Prevents duplicate entries

### `daily_summary.txt`

* Fresh summary generated every run
* Contains only newly fetched headlines

---

## Concepts Demonstrated

* Python scripting
* File handling
* File pointer manipulation
* API integration
* Data automation
* Duplicate filtering
* Error handling
* Batch writing operations

---

## Applications

* Automated news monitoring
* Daily digest systems
* Data collection pipelines
* Content aggregation systems
* File handling practice projects

---

## Future Improvements

* Add email notifications
* Add Telegram/Discord integration
* Support multiple topics
* Store data in a database
* Add scheduling with cron jobs or Task Scheduler
* Build a web dashboard

---

## License

This project is licensed under the MIT License.
