import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver

def fetch_ndtv():
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
                continue

            title = title_tag.get_text(strip=True)
            href = title_tag.get("href", "")
            if not href:
                continue

            url = href if href.startswith("http") else "https://www.ndtv.com" + href

            source_tag = li.find("a", class_="NwsLstPg_pst_lnk")
            date_tag = li.find("span", class_="NwsLstPg_pst_lnk")

            source = source_tag.get_text(strip=True) if source_tag else "NDTV"
            published_at = date_tag.get_text(strip=True) if date_tag else "N/A"

            articles.append({
                "title": title,
                "url": url,
                "source": source,
                "published_at": published_at
            })

        except Exception:
            continue

    return articles


def fetch_ht():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.set_page_load_timeout(30)

    try:
        driver.get("https://www.hindustantimes.com/trending")
        time.sleep(2)
    except Exception as e:
        print(f"[fetch_ht] Failed to load HT: {e}")
        driver.quit()
        return []

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
        except Exception:
            continue

    return articles


def fetch_toi():
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
            formatted_date = parsed_date.strftime("%Y-%m-%d")
            articles.append({
                "title": title,
                "url": url,
                "source": author,
                "published_at": formatted_date
            })
        except:
            continue
    return articles
