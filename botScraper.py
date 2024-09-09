from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Chrome Driver config
service = Service(executable_path='executables/chromedriver-mac-arm64/chromedriver')
options = Options()
#options.binary_location = r'executables/chrome-mac-arm64/ChromeTest.app' # Comment this line if you're using MacOs
options.add_argument("--disable-extensions")
options.add_argument("--disable-popup-blocking") # Evades popups
#options.add_argument("--headless")  # Launch the browser without graphical interface (for use on servers)
options.add_argument("--start-maximized") # Specify launch options and resolution to assure consistency on results
options.add_argument("--window-size=1920x1080")

# Reads the selected csv and takes the info on the columns
df = pd.read_csv('testlista2.csv')

searchQueries = df.iloc[:, 0].tolist()
productPrices = df.iloc[:, 1].tolist()

# Initialize Chromedriver
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://google.com")

# Creates two lists to store all data and a list to store our prices
rows = []
ourPrices =[]

# Iterates over every search row
for query, csvPrice in zip(searchQueries, productPrices):
    try:
        # Search for the product and goes to the shopping page
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'gLFyf')))
        inputSearch = driver.find_element(By.CLASS_NAME, 'gLFyf')
        inputSearch.clear()
        inputSearch.send_keys(query + Keys.ENTER)

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@jsname='bVqjv' and text()='Shopping']")))
        shoppingLink = driver.find_element(By.XPATH, "//div[@jsname='bVqjv' and text()='Shopping']")
        shoppingLink.click()

        # Extracts product, price and shop info
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//h3[@class='tAxDx']")))
        productElements = driver.find_elements(By.XPATH, "//h3[@class='tAxDx']")
        priceElements = driver.find_elements(By.XPATH, "//span[@class='a8Pemb OFFNJ']")
        storeElements = driver.find_elements(By.CLASS_NAME, 'aULzUe')

        # Add scrap results to the dataframe
        for product, price, store in zip(productElements, priceElements, storeElements):
            productName = product.text
            productPrice = price.text
            storeName = store.text

            rows.append({
                "searchQuery": query,
                "productName": productName,
                "productPrice": productPrice,
                "storeName": storeName
            })
  
        # Adds our info on "ourPrices" list
        ourPrices.append({
            "searchQuery": query,
            "productName": query,
            "productPrice": csvPrice,
            "storeName": "ourStore"
        })

    except Exception as e:
        print(f"Ocurrió un error con la búsqueda '{query}': {e}")
        continue

    # Waits before searching for the next row
    time.sleep(2)

# Closes browser
driver.quit()

# Turns the lists into dataframes
scrapedData = pd.DataFrame(rows)
ourPrices = pd.DataFrame(ourPrices)

# Saves the dataframe as a CSV and downloads it automatically
from datetime import datetime, timedelta
relativeDate = datetime.now().strftime("%y%m%d_%H%M")
scrapedData.to_csv("generatedFiles/scrapedData.csv", index=False)