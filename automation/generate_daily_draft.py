import datetime as dt
import html
import json
import os
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
FEEDS_FILE = ROOT / "automation" / "sources.json"
POSTS_FILE = ROOT / "daily-posts.js"
OPENAI_URL = "https://api.openai.com/v1/chat/completions"


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def text_content(value):
    parser = TextExtractor()
    parser.feed(value or "")
    return re.sub(r"\s+", " ", html.unescape(" ".join(parser.parts))).strip()


def child_text(element, names):
    for child in element.iter():
        name = child.tag.rsplit("}", 1)[-1].lower()
        if name in names and child.text:
            return child.text
    return ""


def parse_date(value):
    if not value:
        return None
    try:
        parsed = parsedate_to_datetime(value)
    except (TypeError, ValueError, OverflowError):
        try:
            parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def feed_items(feed):
    request = urllib.request.Request(
        feed["url"], headers={"User-Agent": "NasirYouthDailyDraft/1.0"}
    )
    with urllib.request.urlopen(request, timeout=25) as response:
        root = ET.fromstring(response.read())

    items = []
    for element in root.iter():
        if element.tag.rsplit("}", 1)[-1].lower() not in {"item", "entry"}:
            continue
        title = child_text(element, {"title"})
        link = child_text(element, {"link"})
        if not link:
            for child in element:
                if child.tag.rsplit("}", 1)[-1].lower() == "link":
                    link = child.attrib.get("href", "")
                    if link:
                        break
        summary = child_text(element, {"description", "summary", "content"})
        published = child_text(element, {"pubdate", "published", "updated", "date"})
        published_at = parse_date(published)
        if title and link and published_at:
            items.append({
                "publisher": feed["name"],
                "title": text_content(title),
                "summary": text_content(summary)[:1800],
                "url": link.strip(),
                "published_at": published_at.isoformat(),
            })
    return items


def load_posts():
    content = POSTS_FILE.read_text(encoding="utf-8").strip()
    prefix = "window.dailyPosts = "
    if not content.startswith(prefix) or not content.endswith(";"):
        raise ValueError("daily-posts.js has an unexpected format")
    return json.loads(content[len(prefix):-1])


def make_draft(items, today):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Set the OPENAI_API_KEY GitHub Actions secret first")
    model = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")
    numbered_items = [
        {**item, "source_id": index + 1}
        for index, item in enumerate(items)
    ]
    prompt = {
        "task": "Write one concise, source-based community news draft for the Nasir Youth Community website.",
        "rules": [
            "Use only facts explicitly present in the supplied feed titles and summaries.",
            "Do not invent quotes, numbers, dates, causes, locations, or eyewitness accounts.",
            "Attribute claims to the named publisher and clearly state uncertainty or disagreement.",
            "Do not imply that an RSS summary is independently verified or that you read the full article.",
            "Return valid JSON only, with title, excerpt, body (an array of short paragraphs), and source_ids (the integer IDs of only the items used).",
            "Keep the excerpt under 240 characters and body to 2-4 short paragraphs.",
            "Do not return URLs or sources; source references are added from the supplied feed items.",
            "If the feed items do not support a useful factual story, return {\"skip\": true}.",
        ],
        "date": today.isoformat(),
        "items": numbered_items,
    }
    request_body = json.dumps({
        "model": model,
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": "You are a cautious community newsroom assistant. Never fabricate reporting."},
            {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)},
        ],
    }).encode("utf-8")
    request = urllib.request.Request(
        OPENAI_URL,
        data=request_body,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        payload = json.loads(response.read())
    return json.loads(payload["choices"][0]["message"]["content"])


def main():
    today = dt.datetime.now(dt.timezone.utc).date()
    config = json.loads(FEEDS_FILE.read_text(encoding="utf-8"))
    feeds = config.get("feeds", [])
    if not feeds:
        raise ValueError("Add trusted RSS feed names and URLs to automation/sources.json")

    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=3)
    items = []
    for feed in feeds:
        items.extend(item for item in feed_items(feed) if parse_date(item["published_at"]) >= cutoff)
    items.sort(key=lambda item: item["published_at"], reverse=True)
    items = items[:12]
    if not items:
        raise ValueError("No feed items from the last 3 days; no draft was generated")

    posts = load_posts()
    if any(post.get("pubDate") == today.strftime("%b %d, %Y") for post in posts):
        print("A draft for today already exists; nothing to do.")
        return

    draft = make_draft(items, today)
    if draft.get("skip") is True:
        print("The supplied feed items did not support a safe factual draft.")
        return
    for key in ("title", "excerpt", "body"):
        if key not in draft:
            raise ValueError(f"AI response is missing {key}")
    if not isinstance(draft["body"], list) or not draft["body"]:
        raise ValueError("AI response body must be a non-empty paragraph array")
    source_ids = draft.get("source_ids")
    valid_source_ids = {item["source_id"] for item in numbered_items}
    if (
        not isinstance(source_ids, list)
        or not source_ids
        or any(type(source_id) is not int for source_id in source_ids)
        or not set(source_ids).issubset(valid_source_ids)
    ):
        raise ValueError("AI response must cite valid source_ids from the supplied feed items")

    sources = [
        {"label": f"{item['publisher']} - {item['title']}", "url": item["url"]}
        for item in numbered_items
        if item["source_id"] in source_ids
    ]
    post = {
        "id": int(today.strftime("%Y%m%d")),
        "category": "News",
        "date": today.strftime("%b %d, %Y"),
        "pubDate": today.strftime("%b %d, %Y"),
        "title": str(draft["title"])[:140],
        "excerpt": str(draft["excerpt"])[:240],
        "glyph": "+",
        "tone": "tone-orange",
        "featured": False,
        "verification": "Reported",
        "body": [str(paragraph) for paragraph in draft["body"][:4]],
        "sources": sources,
    }
    posts.insert(0, post)
    POSTS_FILE.write_text(
        "window.dailyPosts = " + json.dumps(posts, ensure_ascii=True, indent=2) + ";\n",
        encoding="utf-8",
    )
    print(f"Generated draft for review: {post['title']}")


if __name__ == "__main__":
    try:
        main()
    except (KeyError, ValueError, urllib.error.URLError, ET.ParseError) as error:
        print(f"Daily draft failed: {error}", file=sys.stderr)
        raise SystemExit(1)