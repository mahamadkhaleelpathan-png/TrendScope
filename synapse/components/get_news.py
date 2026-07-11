import re
import os
import html
import feedparser
import requests
from datetime import datetime
from bs4 import BeautifulSoup


class NewsScraper:
    def __init__(self, feeds=None):
        self.feeds = feeds or []
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def extract(self, date=None):
        seen_urls = set()
        results = []
        for feed_url in self.feeds:
            scrape_count = 0
            try:
                resp = requests.get(feed_url, headers=self.headers, timeout=10)
                if resp.status_code != 200:
                    continue
                parsed = feedparser.parse(resp.content)
                for entry in parsed.entries:
                    link = entry.get("link", "")
                    if not link or link in seen_urls:
                        continue
                    article_date = self._parse_date(entry.get("published", ""))
                    if date and article_date and article_date[:10] != date:
                        continue
                    title = entry.get("title", "")
                    summary_basic = self._clean_html(entry.get("summary", ""))

                    content_parts = []
                    for c in entry.get("content", []):
                        if isinstance(c, dict) and "value" in c:
                            content_parts.append(c["value"])
                    full_rss_content = summary_basic
                    if content_parts:
                        full_rss = self._clean_html("\n".join(content_parts))
                        if len(full_rss) > len(full_rss_content):
                            full_rss_content = full_rss

                    source = entry.get("source", {}).get("title", "") if isinstance(entry.get("source"), dict) else ""
                    if not source and hasattr(entry, "feed") and hasattr(entry.feed, "title"):
                        source = entry.feed.title

                    media_content = entry.get("media_content", [])
                    rss_image = ""
                    if media_content and isinstance(media_content, list) and len(media_content) > 0:
                        rss_image = media_content[0].get("url", "")
                    if not rss_image:
                        media_thumbnail = entry.get("media_thumbnail", [])
                        if media_thumbnail and isinstance(media_thumbnail, list):
                            rss_image = media_thumbnail[0].get("url", "")

                    seen_urls.add(link)
                    article_content, og_image, og_author = None, None, None
                    should_scrape = (
                        "news.google.com/rss/articles" not in link
                        and scrape_count < 3
                        and len(full_rss_content) < 500
                    )
                    if should_scrape:
                        article_content, og_image, og_author = self._scrape_article(link)
                        if article_content:
                            scrape_count += 1
                    final_content = article_content or full_rss_content or summary_basic
                    final_img = og_image or rss_image or ""
                    final_author = og_author or source or ""

                    results.append({
                        "title": title or "No Title",
                        "url": link,
                        "content": final_content,
                        "author": final_author,
                        "image_url": final_img,
                        "date": article_date or date,
                    })
            except Exception:
                continue
        return results

    def _scrape_article(self, url):
        if not url or "news.google.com/rss/articles" in url:
            return None, None, None
        try:
            resp = requests.get(url, headers=self.headers, timeout=6)
            if resp.status_code != 200 or len(resp.text) < 1000:
                return None, None, None
            soup = BeautifulSoup(resp.text, "html.parser")

            og_image = ""
            for attr in ({"property": "og:image"}, {"name": "og:image"}, {"property": "og:image:url"}, {"name": "twitter:image"}):
                tag = soup.find("meta", attrs=attr)
                if tag and tag.get("content"):
                    og_image = tag["content"]
                    break

            og_author = ""
            for attr in ({"name": "author"}, {"property": "article:author"}, {"name": "twitter:creator"}):
                tag = soup.find("meta", attrs=attr)
                if tag and tag.get("content"):
                    og_author = tag["content"]
                    break
            if not og_author:
                for sel in ("a[rel=author]", "[class*=byline]", "[class*=author]", "[class*=byline] a"):
                    el = soup.select_one(sel)
                    if el:
                        og_author = el.get_text(strip=True)
                        break

            content_el = None
            for sel in [
                "article", "[role=main]", "main",
                ".post-content", ".article-content", ".entry-content",
                ".story-body", ".article-body", ".story-content",
                "#article-body", "#story-body",
                ".content__article-body", "[itemprop=articleBody]",
                ".caas-body", ".article__content",
            ]:
                el = soup.select_one(sel)
                if el and len(el.get_text(strip=True)) > 200:
                    content_el = el
                    break

            if content_el:
                for tag in content_el.find_all(["script", "style", "nav", "aside", "footer", "header", "figure", ".ad", ".advertisement", ".social-share", "[class*=share]", "[class*=ad]", "[class*=related]"]):
                    tag.decompose()
                paragraphs = content_el.find_all("p")
                text = "\n\n".join(p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20)
                if len(text) > 150:
                    return text, og_image, og_author

            all_ps = soup.find_all("p")
            body_ps = [p.get_text(strip=True) for p in all_ps if len(p.get_text(strip=True)) > 40]
            if body_ps:
                return "\n\n".join(body_ps[:30]), og_image, og_author

            return None, og_image, og_author
        except Exception:
            return None, None, None

    def _clean_html(self, text):
        if not text:
            return ""
        decoded = html.unescape(text)
        soup = BeautifulSoup(decoded, "html.parser")
        cleaned = soup.get_text(separator=" ", strip=True)
        return re.sub(r"\s+", " ", cleaned).strip()

    def _parse_date(self, date_str):
        if not date_str:
            return None
        for fmt in ("%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S %Z",
                    "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ",
                    "%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S.%fZ"):
            try:
                return datetime.strptime(date_str.strip(), fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
        return None
