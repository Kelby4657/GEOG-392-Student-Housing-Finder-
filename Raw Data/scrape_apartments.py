import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

START_URL = "https://www.apartments.com/college-station-tx/"
MAX_RESULTS = 150

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless=new")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def extract_price(card):
    selectors = [
        "p.property-pricing",
        "span.property-rent",
        "div.price-range",
        "span.altRentDisplay"
    ]
    for sel in selectors:
        try:
            els = card.find_elements(By.CSS_SELECTOR, sel)
            if els:
                txt = els[0].text.strip()
                if txt:
                    return txt
        except:
            pass

    # fallback
    for line in card.text.splitlines():
        if "$" in line or "Call for" in line:
            return line.strip()

    return ""


def extract_beds(card):
    """
    Beds on the summary card typically appear in a line like:
    '1–4 Beds | 515–1,200 sq ft'
    """
    try:
        text = card.text.splitlines()
        for line in text:
            if "Bed" in line:
                # example line: "1–4 Beds | 515–1,200 sq ft"
                beds = line.split("|")[0].strip()
                return beds
    except:
        pass
    return ""


def extract_url(card):
    try:
        link = card.find_element(By.CSS_SELECTOR, "a.property-link")
        return link.get_attribute("href")
    except:
        return ""


def scrape_page(driver):
    time.sleep(3)
    data = []

    cards = driver.find_elements(By.CSS_SELECTOR, "li.mortar-wrapper")

    for card in cards:
        # NAME
        try:
            name = card.find_element(By.CSS_SELECTOR, "span.js-placardTitle.title").text
        except:
            name = ""

        # ADDRESS
        try:
            address = card.find_element(By.CSS_SELECTOR, "div.property-address").text
        except:
            address = ""

        price = extract_price(card)
        beds = extract_beds(card)
        url = extract_url(card)

        if name or address:
            data.append({
                "name": name.strip(),
                "address": address.strip(),
                "price": price.strip(),
                "beds": beds.strip(),
                "url": url.strip()
            })

    return data


def go_to_next_page(driver):
    try:
        next_btn = driver.find_element(By.CSS_SELECTOR, "a.next")
        if "disabled" in next_btn.get_attribute("class").lower():
            return False
        next_btn.click()
        return True
    except:
        return False


def main():
    driver = get_driver()
    driver.get(START_URL)

    all_rows = []

    while True:
        rows = scrape_page(driver)
        for r in rows:
            if len(all_rows) < MAX_RESULTS:
                all_rows.append(r)

        print(f"Collected {len(all_rows)} unique properties...")

        if len(all_rows) >= MAX_RESULTS:
            print("Reached maximum limit.")
            break

        if not go_to_next_page(driver):
            break

    driver.quit()

    with open("apartments.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "address", "price", "beds", "url"])
        writer.writeheader()
        writer.writerows(all_rows)

    print("\nSaved apartments.csv")

if __name__ == "__main__":
    main()
