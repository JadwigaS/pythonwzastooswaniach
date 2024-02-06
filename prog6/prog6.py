from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import argparse 
import json

parser = argparse.ArgumentParser(description='program 6')
parser.add_argument('plik',help='plik')
args=parser.parse_args()
options = Options()
options.add_argument('--headless')

service = Service('webdriver/firefoxdriver.exe')

driver = webdriver.Firefox()

driver.get('https://2e.aonprd.com/SpellLists.aspx?Tradition=1')

main_div = driver.find_element(By.CLASS_NAME, 'main')
spells=[]
for results in main_div.find_elements(By.CSS_SELECTOR, 'h2,u'):
    #print(results.tag_name)
    spells.append(results.text.strip())
    #print('------------------')

element = driver.find_element(By.LINK_TEXT, "Divine")
element.click()
main_div = driver.find_element(By.CLASS_NAME, 'main')
for results in main_div.find_elements(By.CSS_SELECTOR, 'h2,u'):
    #print(results.tag_name)
    spells.append(results.text.strip())
    #print('------------------')

#time.sleep(1000)
driver.close()

with open(args.plik, 'w') as f:
    json.dump(spells, f, indent=4)