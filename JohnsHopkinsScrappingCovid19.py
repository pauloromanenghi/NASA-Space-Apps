from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import date
import json
import time
import os
import re
import requests

# Chrome preference
chrome_prefs = {}

options = Options()
options.headless = True
options.add_argument('--no-sandbox') 
options.add_argument('--disable-gpu')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")
options.experimental_options["prefs"] = chrome_prefs

# Start webdriver -- headless mode
driver = webdriver.Chrome(executable_path="./drivers/chromedriver", options=options)

# Url
base_url = 'https://www.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6'

waitTime = 50

def wait(value = 3):
    time.sleep(value)
 
 
def loadTotalConfirmed():
    try:

        element = WebDriverWait(driver, waitTime).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='ember27']//div[@class='flex-vertical flex-fix allow-shrink']"))).text
        
        return element.split('\n')[1].strip().replace(",", ".")

    except Exception as error:
        raise Exception("[TOTAL_CONFIRMED_CASES] - Error:%s" % error)


def loadConfirmedCasesByCountry():
    try:

        element = WebDriverWait(driver, waitTime).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='ember34']//nav[@class='feature-list']")))

        wait(10)

        data = element.find_elements_by_tag_name("h5")

        confirmedCases = []
        for country in data:
            
            casesInformation = country.text.split(' ')

            confirmedCases.append({
                'country': casesInformation[1].strip(),
                'confirmed': casesInformation[0].strip().replace(",", ".")
            })

        return confirmedCases

    except Exception as error:
        raise Exception("[CONFIRMED_CASES_BY_COUNTRY] - Error:%s" % error)


def loadGlobalDeathsByCountry():
    try:

        element = WebDriverWait(driver, waitTime).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='ember111']//nav[@class='feature-list']")))

        wait(10)

        data = element.find_elements_by_xpath("//div[@id='ember111']//nav[@class='feature-list']//div[contains(@class,'flex-fluid list-item-content overflow-hidden')]")

        deathsCases = []
        for country in data:

            casesInformation = country.text.replace("deaths", "").split('\n')

            deathsCases.append({
                'country': casesInformation[1].strip(),
                'deaths': casesInformation[0].strip().replace(",", ".")
            })

        return deathsCases

    except Exception as error:
        raise Exception("[GLOBAL_DEATHS_BY_COUNTRY] - Error:%s" % error)


def loadTotalRecovered():
    try:

        element = WebDriverWait(driver, waitTime).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='ember118']//div[@class='flex-vertical flex-fix allow-shrink']"))).text
        
        return element.split('\n')[1].strip().replace(",", ".")

    except Exception as error:
        raise Exception("[TOTAL_RECOVERED_CASES] - Error:%s" % error)


def loadGlobalRecoveredByCountry():
    try:

        WebDriverWait(driver, waitTime).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='ember240']//div[3]//a[1]"))).click()

        wait(5)
        
        element = WebDriverWait(driver, waitTime).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='ember125']//nav[@class='feature-list']")))

        wait(5)

        data = element.find_elements_by_xpath("//div[@id='ember125']//nav[@class='feature-list']//div[contains(@class,'flex-fluid list-item-content overflow-hidden')]")

        recoveredCases = []
        for country in data:

            casesInformation = country.text.replace("recovered", "").split('\n')
            recoveredCases.append({
                'country': casesInformation[1].strip(),
                'recovered': casesInformation[0].strip().replace(",", ".")
            })

        return recoveredCases

    except Exception as error:
        raise Exception("[GLOBAL_RECOVERED_BY_COUNTRY] - Error:%s" % error)

def main():

    try:

        print('Loading')

        driver.get(base_url)

        totalConfirmed = loadTotalConfirmed()
        confirmedCasesByCountry = loadConfirmedCasesByCountry()
        globalDeathsByCountry = loadGlobalDeathsByCountry()
        recoveredByCountry = loadGlobalRecoveredByCountry()
        totalRecovered = loadTotalRecovered()

        result = {
            'total_confirmed': totalConfirmed,
            'total_recovered': totalRecovered,
            'confirmed_by_country': confirmedCasesByCountry,
            'global_deaths_by_country': globalDeathsByCountry,
            'recovered_by_country': recoveredByCountry
        }

        print(result)

    except Exception as error:
        raise Exception(error)

    except KeyboardInterrupt as error:
        raise Exception("Process has been cancelled by user")




if __name__ == '__main__':

    try:

        main()

    except Exception as error:
        print(error)
    finally:
        driver.quit()