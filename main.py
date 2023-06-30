
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

formLink = "https://forms.gle/uBiqK4N67g6Lk9Th7"
searchLink = "https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22mapBounds%22%3A%7B%22north%22%3A37.85841972721125%2C%22east%22%3A-122.27831927661133%2C%22south%22%3A37.69207060712121%2C%22west%22%3A-122.58833972338867%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22mp%22%3A%7B%22max%22%3A2200%7D%2C%22price%22%3A%7B%22max%22%3A434447%7D%2C%22beds%22%3A%7B%22min%22%3A2%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22pagination%22%3A%7B%7D%7D"

response = requests.get(searchLink, headers={
"Accept-Language":"en-US,en;q=0.5",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0"
})
webpage = response.text
soup = BeautifulSoup(webpage, "html.parser")
estate_prices = soup.find_all('span', {'data-test':"property-card-price"})
estate_addrs = soup.find_all("address")
estate_links = soup.select('a[class*="StyledPropertyCardDataArea"]')
estates = []

if len(estate_prices) == len(estate_addrs) == len(estate_links):
    for i in range(len(estate_prices)):
        estates.append((estate_addrs[i].text, estate_prices[i].text, estate_links[i].get("href")))
else:
    print("List lengths don't match!")

print(estates)

driver = webdriver.Chrome()
driver.get(formLink)


for estate in estates:
    driver.implicitly_wait(1)
    time.sleep(2)
    address_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_field.send_keys(estate[0])

    price_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_field.send_keys(estate[1])

    link_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_field.send_keys(estate[2])

    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_button.click()

    time.sleep(2)

    next_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    next_button.click()


input()
