
##### MODULES
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

##### START SELENIUM
chrome_path = "C:\\Program Files\\Chromedriver\\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)
driver.get("https://apps.nd.gov/sc/busnsrch/busnSearch.htm?results=false")

##### DEF FNs and BUILD LISTS
businesses = ['start']
alphabet = ['A', 'B', 'C', 'D', 'E']
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
        # See how many LLCS on page
        links = driver.find_elements_by_link_text("LLC")
        length = len(links)

        # Iterate through the list with indexing
        i = 0
        while i < length:
            time.sleep(1)
            driver.find_elements_by_link_text("LLC")[i].click()
            time.sleep(1)
            busn_name = driver.find_element_by_xpath("//*[@id='BusnSrchFM']/div[1]/h3").text
            businesses.append(busn_name)
            founded = driver.find_element_by_xpath("//*[@id='BusnSrchFM']/div[1]/table/tbody/tr/td[1]/ol/li[4]").text
            print(founded)
            driver.find_element_by_xpath("//*[@id='BusnSrchFM']/div[1]/p/a").click()
            i = i + 1

        # Click 'Next' button
        time.sleep(1)
        driver.find_element_by_link_text("Next").click()

    driver.find_element_by_xpath("//*[@id='BusnSrchFM']/div[1]/p[2]/a").click()
    time.sleep(5)

