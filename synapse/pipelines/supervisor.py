from synapse.components.get_news import NewsScraper


def run_weekly_pipeline(dates=None, feeds=None):
    if dates is None:
        return []
    scraper = NewsScraper(feeds=feeds)
    all_articles = []
    seen_titles = set()
    for d in dates:
        articles = scraper.extract(d)
        for a in articles:
            title_key = (a.get("title", "") or "").strip().lower()
            if title_key and title_key not in seen_titles:
                seen_titles.add(title_key)
                a["date_group"] = d
                if " - " in a.get("title", ""):
                    a["title"] = a["title"].rsplit(" - ", 1)[0]
                if " | " in a.get("title", ""):
                    a["title"] = a["title"].rsplit(" | ", 1)[0]
                all_articles.append(a)
    return all_articles
