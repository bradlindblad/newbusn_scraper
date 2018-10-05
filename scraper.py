

##### MODULES
import time
from datetime import datetime
from datetime import timedelta
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

##### START SELENIUM
chrome_path = "C:\\users\\lindblb\\desktop\\newbusn_scraper\\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)
driver.get("https://apps.nd.gov/sc/busnsrch/busnSearch.htm?results=false")

##### DEF FNs and BUILD LISTS

with open('search_terms.txt') as f:
    alphabet = f.read().splitlines()

start = {'Name': [],
         'Founded': [],
         'Phone': [],
         'Town': []}
businesses = pd.DataFrame(start)

def hasXpath(text):
    try:
        driver.find_element_by_link_text(text)
        return True
    except:
        return False


##### START LETTER LOOP
for letter in alphabet:

    # ITERATION FOR EACH LETTER OF ALPHABET

    search_box = driver.find_element_by_xpath("//*[@id='searchName']")
    search_box.click()
    search_box.clear()
    search_box.send_keys(letter)
    search_box.send_keys(Keys.RETURN)


##### START PAGE LOOP
    while hasXpath("Next") is True:

        #### P A G E ####
        # See how many partnerships on page
        links = driver.find_elements_by_link_text("Partnership")
        length = len(links)

        # Iterate through the list with indexing
        i = 0
        while i < length:
            time.sleep(1)
            driver.find_elements_by_link_text("Partnership")[i].click()
            time.sleep(1)
            phone = driver.find_element_by_xpath("//*[@id='BusnSrchFM']/div[1]/table/tbody/tr/td[2]/ol/li[1]").text
            busn_name = driver.find_element_by_xpath("//*[@id='BusnSrchFM']/div[1]/h3").text
            founded = driver.find_element_by_xpath("//*[@id='BusnSrchFM']/div[1]/table/tbody/tr/td[1]/ol/li[4]").text
            founded = founded.replace('Original File Date:', '')
            founded = founded.replace(' ', '')
            founded = datetime.strptime(founded, '%m/%d/%Y')

            town = driver.find_element_by_xpath("//*[@id='BusnSrchFM']/div[1]/div[1]/span[2]").text
            town = town.split(',')
            town = town[0]
            if 'PO' in town:  # sometimes in the principal office section there's an extra row (span) for PO box, this checks that
                town = driver.find_element_by_xpath("//*[@id='BusnSrchFM']/div[1]/div[1]/span[3]").text
                town = town.split(',')
                town = town[0]

            print(busn_name)
            driver.find_element_by_xpath("//*[@id='BusnSrchFM']/div[1]/p/a").click()

            # Add to DataFrame
            businesses = businesses.append({'Name': busn_name,
                                            'Founded': founded,
                                            'Phone': phone,
                                            'Town': town}, ignore_index=True)

            i = i + 1

        # Click 'Next' button
        time.sleep(1)
        driver.find_element_by_link_text("Next").click()

    driver.find_element_by_xpath("//*[@id='BusnSrchFM']/div[1]/p[2]/a").click()
    time.sleep(5)

    # Only keep recent filings
    d = datetime.today() - timedelta(days=60)  # date 60 days ago
    businesses = businesses[(businesses['Founded'] > d)]

