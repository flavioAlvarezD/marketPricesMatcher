import re
import pandas as pd
from botScraper import scrapedData, ourPrices
from datetime import datetime

relativeDate = datetime.now().strftime("%y%m%d_%H%M")

# Creates a function using a regular expression to take only the numbers and decimal point from a value
def regExPrice(price):
    match = re.search(r'[\d,]+(?:\.\d*)?', price)
    if match:
        regExPrice = match.group().replace(',', '')
        return float(regExPrice)
    return None

# Creates a list of undesired terms on both the Product title and the price, to remove them from the list
undesiredProductName = '|'.join(["refurbished", "reusado", "usado", "usada", "reacondicionado", "reacondicionada", "seminuevo"])
scrapedData = scrapedData[~scrapedData['productName'].str.contains(undesiredProductName, case=False, na=False)]

scrapedData['productPrice'] = scrapedData['productPrice'].astype(str)
undesiredPriceTerms = '|'.join(["mensuales", "mensualidades", "meses", "pagos"])
scrapedData = scrapedData[~scrapedData['productPrice'].str.contains(undesiredPriceTerms, case=False, na=False)]

# Uses the regex function to extract the prices and convert them to floats. Along with transforming the remaining columns to strings
# Adittionaly it sends a dropna, since for some reason it doesn't consider some fields as NaN until they're turned into strings
scrapedData['productPrice'] = scrapedData['productPrice'].apply(regExPrice)
scrapedData[['searchQuery', 'productName', 'storeName']] = scrapedData[['searchQuery', 'productName', 'storeName']].astype(str)
scrapedData.dropna(inplace=True)


# Defines percentiles and cleans outliers
lowerB = scrapedData['productPrice'].quantile(0.40)
upperB = scrapedData['productPrice'].quantile(1)

scrapedData = scrapedData.groupby('searchQuery').apply(lambda x: x[(x['productPrice'] >= lowerB) & (x['productPrice'] <= upperB)]).reset_index(drop=True)

# Concatenates the prices from our store. This is done until this point because the outlier removal could erase this prices
scrapedData = pd.concat([scrapedData, ourPrices], ignore_index=True)


# Finds our price on the list for each product and creates a column for it
scrapedData['ourStorePrice'] = scrapedData.apply(lambda row: scrapedData[(scrapedData['searchQuery'] == row['searchQuery']) & (scrapedData['storeName'] == 'ourStore')]['productPrice'].values[0], axis=1).round(2)


# Sorts the values and finds the average price and the store rank for each one of them
scrapedData = scrapedData.sort_values(by=['searchQuery', 'productPrice'])
scrapedData['marketRank'] = scrapedData.groupby('searchQuery').cumcount() + 1
scrapedData['avgMarketPrice'] = scrapedData.groupby('searchQuery')['productPrice'].transform('mean').round(2)


# Creates a column to put ourStore rank on the market
scrapedData['ourStoreRank'] = scrapedData.apply(lambda row: scrapedData[(scrapedData['searchQuery'] == row['searchQuery']) & (scrapedData['storeName'] == 'ourStore')]['marketRank'].values[0], axis=1)
# Determinates if ourStore had the lowest price on the market
scrapedData['didWeWon'] = scrapedData['ourStoreRank'] == 1
# Creates a column for price, store and title for the store with the lowest price
scrapedData['bestPrice'] = scrapedData.apply(lambda row: scrapedData[(scrapedData['searchQuery'] == row['searchQuery']) & (scrapedData['marketRank'] == 1)]['productPrice'].values[0], axis=1).round(2)
scrapedData['winnerStore'] = scrapedData.apply(lambda row: scrapedData[(scrapedData['searchQuery'] == row['searchQuery']) & (scrapedData['marketRank'] == 1)]['storeName'].values[0], axis=1)
scrapedData['winnerTitle'] = scrapedData.apply(lambda row: scrapedData[(scrapedData['searchQuery'] == row['searchQuery']) & (scrapedData['marketRank'] == 1)]['productName'].values[0], axis=1)

# Lefts only one row for each product
scrapedData = scrapedData.drop_duplicates('searchQuery')

scrapedData['priceDifference'] = (scrapedData['ourStorePrice'] - scrapedData['bestPrice']).round(2)

# Deletes unnecessary columns
dataSummary = scrapedData.drop(columns=['marketRank', 'storeName', 'productName', 'productPrice'])
dataSummary.rename(columns={'searchQuery': 'productName'}, inplace=True)

# Saves the dataframe as a CSV
dataSummary.to_csv("generatedFiles/dataSummary.csv", index=False)
