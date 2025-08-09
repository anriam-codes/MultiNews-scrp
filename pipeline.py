from fetch import fetch_ndtv, fetch_hindustan_times, fetch_inshorts
import json

def run_pipeline():
    data = {
        "ndtv": fetch_ndtv(),
        "hindustantimes": fetch_hindustan_times(),
        "inshorts": fetch_inshorts()
    }

    print(json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    run_pipeline()
