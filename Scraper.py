from bs4 import BeautifulSoup 
import requests

url="https://www.leedsunited.com/en/matches/mens-team/fixtures"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

print(soup.prettify())