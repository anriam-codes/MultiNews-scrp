import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin

def fetch_ndtv():
    from bs4 import BeautifulSoup
    from selenium import webdriver
    import time

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.ndtv.com/latest")
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    articles = []

    ul_tag = soup.find("ul", class_="NwsLstPg_ul")
    if not ul_tag:
        return articles

    li_tags = ul_tag.find_all("li", class_="NwsLstPg-a-li")[:4]

    for li in li_tags:
        try:
            title_tag = li.find("a", class_="NwsLstPg_ttl-lnk")
            if not title_tag:
                print("Skipping li: no title tag")
                continue

            title = title_tag.get_text(strip=True)
            href = title_tag.get("href", "")
            if not href:
                print(f"Skipping li: no href for title '{title}'")
                continue

            url = href if href.startswith("http") else "https://www.ndtv.com" + href

            source_tag = li.find("a", class_="NwsLstPg_pst_lnk")
            date_tag = li.find("span", class_="NwsLstPg_pst_lnk")

            source = source_tag.get_text(strip=True) if source_tag else "NDTV"
            published_at = date_tag.get_text(strip=True) if date_tag else "N/A"

            articles.append({
                "title": title,
                "url": url,
                "source/post by": source,
                "published_at": published_at
            })

        except Exception as e:
            print(f"Error processing <li>: {e}")
            continue

    return articles


def fetch_hindustan_times():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.hindustantimes.com/trending")
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    articles = []
    cards = soup.find_all("div", class_="cartHolder")[:5]

    for card in cards:
        try:
            h2_tag = card.find("h2")
            title = h2_tag.get_text(strip=True) if h2_tag else "N/A"

            a_tag = card.find("a", href=True)
            url = f"https://www.hindustantimes.com{a_tag['href']}" if a_tag else "N/A"

            source_tag = card.find("div", class_="secName ftlsecName")
            source = source_tag.get_text(strip=True) if source_tag else "N/A"

            date = card.get("data-vars-story-time", "N/A")

            if title != "N/A" and url != "N/A":
                articles.append({
                    "title": title,
                    "url": url,
                    "source": source,
                    "published_at": date
                })
        except Exception as e:
            print(f"Error: {e}")
            continue

    return articles


def fetch_inshorts():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://inshorts.com/en/read")
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    articles = []
    cards = soup.find_all("div", class_="VdsPqrmJYY7F2MNUKOwQ")[:6]
    for card in cards:
        try:
            title = card.find("span", itemprop="headline").get_text(strip=True)
            url = "https://inshorts.com" + card.find("a", href=True)["href"]
            author = card.find("span", class_="author").get_text(strip=True)
            raw_date = card.find("span", class_="date").get_text(strip=True)
            parsed_date = datetime.strptime(raw_date, "%A %d %B, %Y")
            te = parsed_date.strftime("%d %b %Y").lstrip("0")
            articles.append({
                "title": title,
                "url": url,
                "source": author,
                "published_at": te
            })
        except:
            continue
    return articles