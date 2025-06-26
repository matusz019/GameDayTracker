from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

url = "https://www.leedsunited.com/en/matches/mens-team/fixtures"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    page.wait_for_timeout(5000)  # wait for content to load
    html = page.content()
    browser.close()

# Parse with BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Find all fixture cards
fixtures = soup.find_all("div", class_="fixtureCardSecondSlot_mainInfoContainer__kOyRu")

for fixture in fixtures:
    location_div = fixture.find("span", class_="fixtureCardSecondSlot_matchLocation__ZNvqU")
    
    if location_div and "Elland Road" in location_div.text:
        print(location_div.text)
        print("Match found")