def clean_articles(articles):
    cleaned = []
    for a in articles:
        cleaned.append({
            "source": a["source"],
            "title": a["title"].strip(),
            "url": a["url"].strip()
        })
    return cleaned
