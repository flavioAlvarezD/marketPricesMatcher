                         _.:::MARKET PRICES MATCHER:::._

                         IMPORTANT
Here's a video showing how the webscraper works just in case the code can't be used in the future by a newer Chrome version. 


        1.- ABOUT THIS PROJECT
It uses flask as framework, selenium for data scraping and pandas for an easy data work and plotly to help me build nice graphics.

The index.html file contains the <style> CSS inside of it.

Now lets put ourselves in the situation:
Let's suposse we have an ecommerce. It really doesn't matter what is about. But I did this project with a videogame ecommerce store in mind.
We need at all times to be aware of the competitiveness of our prices. If there was a rank of stores based on their prices, what place in said rank should be assigned to our store?
How many of our products have the best price on the market?
How much is the price difference between our producta and those that have the best price?
Well, my Price Matcher solves all of this questions in a nice dashboard

Why did I make the matcher this way?
There's a couple of things I would like to clarify:
1.- This bot only takes the info from the results on the first page from google shopping, for each product. Yes I can add a pagination. But I realized almost every publication on the following pages is not relevant enough for the project goal.
2.- Yes I could've had formuled the google shopping url using the product name and ask Selenium to go directly into the search instead of writing it on the search bar every single time. However; this inmediatly triggers the antibot captchas. So no, this is a bad idea.
3.- You are free to change the percentage defined to clean outliers. I you notice that the final table is showing products that are way too cheap; then you can increase the 'lowerB' percentage in the 'dataCleansing.py' file. Or the other way around if you think there should be more products taken into account when doing the analysis, then reduce this same variable.


        2.- INSTALLING AND RUN
You obviously need to have python3 installed on your device.
>I recommend to create a virtual environment before installing any library
    python -m venv webScraper

    -Then you can activate the environment using the command
        webScraper\Scripts\activate (for Windows) OR source webScraper/bin/activate (for MacOs)

    -I also advice you to make sure you're not on the global environment by writing
        pip list

>If the list contains little to no modules, then you're good to go. Install the modules:
    pip install selenium, pandas, ipython, plotly, flask, -U kaleido, openpyxl
 I recommend to install them one by one instead of all at the same time

You will also need to have installed Chrome for testing with the corresponding Chromedriver version.
I've uploaded the same version I used for develop this matcher on Windows and MacOs, on this MEGA folder: https://mega.nz/folder/18pREIaY#8-nQC4buxAqe4DktWMTr4w
The code is written and tested by default in MacOs. And this folder also has the windows version for both apps. It has some comments on the parts you need to change if you wish to run it on Windows, but be warned; it might not work for you. There's a Known Issue with Windows searching for a non existent usb drive that could left the app loading forever.

In any case, once you extract the zip files, you'll need to put both folders inside the 'executables' folder. and verify the botscraper.py is referencing correctly the chromedriver and the chrome browser as well (it should be).

>Once installed and verified, you can run the program by writing on your terminal:
    pyton app.py
 Or by pressing the play button if you're using VSC 

>Launch your web browser and enter the ip adress the terminal gave you


        3.- HOW TO USE THE APP
Well now let's go ahead with the fun part; you just need an excel file with two columns:
  -The first one will have the names from all the products you wish to search
  -Second one should have the respective prices (only numbers please)
The header's name for the columns does not matter. But it should have one since the bot starts searching from the second row.
From now on; the info from the file you uploaded will be considered and labeled 'ourStore'

Then you just upload the file and wait for the Chrome browser to launch itself and you can enjoy watching how it works for you. You can also uncomment the line 17 I put on 'botScraper.py' if you do not want to see the browser.
Once the scraping is completed, you'll see how the testing browser closes itself and a nice dashboard is generated on the same page of your main browser (where you uploaded your file)

Fisrst thing you'll notice is a pie chart that's gonna tell you the percentage of products where you had the best price on the market. Then a couple of panels tellign you the average rank in the market you got with your prices. And how much was the average difference between the best price and your's.
What's showed next is a table called 'Data Summary'. Each row for each product you uploaded. I'll explain to you what every column is talking about:
productName: The name you uploaded and was used as query for the bot
ourStorePrice: The price you uploaded and was used to make the comparison
avgMarketPrice: The average price from all the publications retrieved on Google Shopping
ourStoreRank: If you ordered them from the cheapest to the most expensive. What place our store would be ranked?
didWeWon: Did we have the best price on the market? This is a boolean
bestPrice: Pretty self explanatory
winnerStore: Which store offered the best price. If it were you, then a 'ourStore' label should be there
winnerTitle: What was the title the best store put to it's product. Useful in case the best price is the wrong product
priceDifference: That was the difference between the best price and yours

You can check up the full raw scraped data on the 'generatedFiles' folder under the name 'scrapedData.csv'. And the summarized data under the name 'dataSummary.csv'


        4.- ROOM FOR IMPROVEMENT
I have lots of ideas to improve this project. However I'm already applying some of them on other projects from this same portfolio (which you are very welcome to look up). And some others would lead me to have even more ideas. So I'll end up never never uploading anything here if I apply every idea that I got while doing this project.
Here are some of this ideas:
1.- Add a pagination function for google shopping so I get even more publications
2.- Extracting the url from the publications
3.- Enter to each one of the publications and extract even more data
4.- Use chatGPT or Gemini to have a better filtering of the products based on their name (This one, I actually did it for a work project!)
5.- Download automatically the generated files such as the raw scraped data and the data summary showed at the end
6.- Option to upload a CSV or Excel file, as well to download them on the same format
7.- Option to write the name from 'ourStore' and find them on the data scraped. As well as notice if there's a difference between our actual prices an the ones Google Shopping is showing



        5.- ABOUT ME
Hey there! Flavio Álvarez here. I'm a Bussiness Intelligence Engineer currently living in Mexico, with a good mileage and knowledge about Ecommerce.
I like videogames (as almost every other programmer, how unique), motorcycles, and I really love listening to 2000's rock.
You cand reach me on these links:
https://github.com/flavioAlvarezD
https://www.linkedin.com/in/flavio-alvarez-dorantes/

And thank you for reading this :D
