import requests
import os
from datetime import datetime

CONFIG_FILE  = "config.txt"
ARCHIVE_FILE = "news_archive.txt"
SUMMARY_FILE = "daily_summary.txt"
NEWSAPI_URL  = "https://newsapi.org/v2/everything"


def create_default_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            f.writelines([
                "api_key = YOUR_NEWSAPI_KEY_HERE\n",
                "topic   = technology\n",
                "country = us\n",
            ])
        print(f"[setup] config.txt created — add your API key and run again.")
        print(f"        Get a free key at: https://newsapi.org/register")
        return False
    return True


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    config = {}
    for line in content.strip().splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()
    return config


def fetch_headlines(api_key, topic, country):
    params = {
        "q":        topic,
        "language": "en",
        "sortBy":   "publishedAt",
        "apiKey":   api_key,
        "pageSize": 15,
    }
    try:
        response = requests.get(NEWSAPI_URL, params=params, timeout=10)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        return [
            {
                "title":  a.get("title",  "").strip(),
                "source": a.get("source", {}).get("name", "Unknown"),
                "url":    a.get("url",    ""),
            }
            for a in articles if a.get("title") and "[Removed]" not in a.get("title", "")
        ]
    except requests.exceptions.HTTPError as e:
        print(f"[error] HTTP error: {e}")
    except requests.exceptions.ConnectionError:
        print("[error] No internet connection.")
    except requests.exceptions.Timeout:
        print("[error] Request timed out.")
    except Exception as e:
        print(f"[error] {e}")
    return []


def get_saved_headlines():
    if not os.path.exists(ARCHIVE_FILE):
        return set()
    with open(ARCHIVE_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    saved = set()
    for line in lines:
        line = line.strip()
        if line.startswith("HEADLINE:"):
            saved.add(line[len("HEADLINE:"):].strip())
    return saved


def todays_section_exists():
    today = datetime.now().strftime("%Y-%m-%d")
    if not os.path.exists(ARCHIVE_FILE):
        return False
    with open(ARCHIVE_FILE, "r", encoding="utf-8") as f:
        f.seek(0)
        content = f.read()
    return f"=== {today} ===" in content


def append_to_archive(new_articles, saved_headlines):
    today = datetime.now().strftime("%Y-%m-%d")
    now   = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    fresh = [a for a in new_articles if a["title"] not in saved_headlines]
    if not fresh:
        print("[archive] No new headlines — all duplicates skipped.")
        return 0

    with open(ARCHIVE_FILE, "a", encoding="utf-8") as f:
        if not todays_section_exists():
            f.writelines([
                f"\n{'=' * 60}\n",
                f"=== {today} ===\n",
                f"{'=' * 60}\n",
            ])

        entry_lines = []
        for article in fresh:
            entry_lines.append(f"HEADLINE: {article['title']}\n")
            entry_lines.append(f"SOURCE:   {article['source']}\n")
            entry_lines.append(f"URL:      {article['url']}\n")
            entry_lines.append(f"SAVED AT: {now}\n")
            entry_lines.append("-" * 60 + "\n")
        f.writelines(entry_lines)

    return len(fresh)


def write_daily_summary(articles):
    today = datetime.now().strftime("%Y-%m-%d")
    now   = datetime.now().strftime("%H:%M:%S")

    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        f.write(f"NEWS SUMMARY — {today}\n")
        f.write(f"Generated : {now}\n")
        f.write(f"Headlines : {len(articles)}\n")
        f.write("=" * 60 + "\n\n")
        for i, article in enumerate(articles, 1):
            f.write(f"{i:02d}. {article['title']}\n")
            f.write(f"     Source : {article['source']}\n")
            f.write(f"     URL    : {article['url']}\n\n")

    with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
        f.seek(0)
        header = ""
        for _ in range(4):
            header += f.readline()
        pointer_pos = f.tell()
        print(f"\n[summary] Written to {SUMMARY_FILE}")
        print(f"[seek]    Pointer at byte {pointer_pos} after reading header:")
        print(f"          {header.strip()}")


def archive_stats():
    if not os.path.exists(ARCHIVE_FILE):
        return

    with open(ARCHIVE_FILE, "r", encoding="utf-8") as f:
        f.seek(0, 2)
        file_size = f.tell()

        f.seek(0)
        lines = f.readlines()

    days      = sum(1 for l in lines if l.startswith("=== 20"))
    headlines = sum(1 for l in lines if l.startswith("HEADLINE:"))

    print(f"\n[archive stats]")
    print(f"  file         : {ARCHIVE_FILE}")
    print(f"  size         : {file_size:,} bytes")
    print(f"  lines        : {len(lines)}")
    print(f"  days logged  : {days}")
    print(f"  total saved  : {headlines} headlines")


def main():
    print("=" * 60)
    print("  NEWS AUTOMATOR — File Operations Showcase")
    print("=" * 60 + "\n")

    if not create_default_config():
        return

    config  = load_config()
    api_key = config.get("api_key", "")
    topic   = config.get("topic",   "technology")
    country = config.get("country", "us")

    if api_key == "YOUR_NEWSAPI_KEY_HERE":
        print("[error] Set your API key in config.txt and run again.")
        return

    print(f"[fetch]   Topic='{topic}'  Country='{country}'")
    articles = fetch_headlines(api_key, topic, country)
    if not articles:
        print("[error] No articles fetched. Check your API key or connection.")
        return
    print(f"[fetch]   {len(articles)} headlines retrieved.")

    saved = get_saved_headlines()
    print(f"[archive] {len(saved)} headlines already on record.")

    new_count = append_to_archive(articles, saved)
    print(f"[archive] {new_count} new headlines saved.")

    write_daily_summary(articles)
    archive_stats()

    print(f"\n[done] Files written:")
    print(f"       {ARCHIVE_FILE}  — rolling log (append mode)")
    print(f"       {SUMMARY_FILE} — today's digest (overwrite mode)")


if __name__ == "__main__":
    main()
