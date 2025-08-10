from fetch import fetch_ndtv, fetch_ht, fetch_toi
from transform import normalize_date

def run_pipeline():
    data = {
        "ndtv": fetch_ndtv(),
        "ht": fetch_ht(),
        "toi": fetch_toi()
    }

    for source in data:
        for article in data[source]:
            article["published_at"] = normalize_date(article["published_at"])

    return data

if __name__ == "__main__":
    from pprint import pprint
    pprint(run_pipeline())
