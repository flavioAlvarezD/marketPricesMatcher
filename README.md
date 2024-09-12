                         _.:::MARKET PRICES MATCHER:::._

        1.- ABOUT THIS PROJECT
To be brief; this heatmap shows the ocurrences on sinister claims for an insurance company, along with their costs.

It uses flask as framework, selenium for data scraping and pandas for an easy data work and plotly for building nice graphics.

The index.html file contains the <style> CSS inside of it.

Now lets put ourselves in the situation:
Let's suposse we have an ecommerce. It really doesn't matter what is about. But I did this project with a videogame electronics store in mind.
We need at all times to be aware of the competitiveness of our prices. If there's a rank of stores based on prices, what place in said rank should be assigned to our store?
How many of our products have the best price on the market
How much is the price difference between the products that are not the best price on the market? and those that are

Why I did the matcher this way?
There's just a couple of things I would like to clarify:
1.- This bot only takes the info from the results on the first page from google shopping, for each product. Yes I can add the pagination function. But I realized almost every publication on the following pages is not relevant for this project.
2.- Yes I could've had formuled the google shopping url using the product name and ask Selenium to go directly into the search, instead of writing it on the search bar every single time. However; this inmediatly triggers the antibot captchas. So no, this is a bad idea



        2.- INSTALL AND RUN

You obviously need to have python3 installed on your device.
>I recommend to create a virtual environment before installing any library
    python -m venv matcher

    -Then you can activate the environment using the command
        matcher\Scripts\activate (for Windows) OR source matcher/bin/activate (for MacOs)

    -I also advice you to make sure you're not on the global environment by writing
        pip list

>If the list contains little to no libraries, then you're good to go. Install the libraries:
    pip install flask pandas requests plotly folium branca
 I recommend to install them one by one instead of all at the same time 

>Once installed, you can run the program by writing on your terminal:
    pyton app.py
 Or by pressing the play button if you're using VSC 

>Launch your web browser and enter the ip adress the terminal gave you



        3.- HOW TO USE THE HEATMAP
It's pretty straightforward; you just have to choose the incident type you wanna check on, 
the part of the city that interests you and the criteria you wish the "heat" to be based on.
If you chose "ocurrences" then the map will be colored by the number of times that incident has happened in that specific zone in the city.
If you select "Total Cost" then it will show how much money the company has spend on that kind of incident.

You can take the color line on the upper right side of the map as a reference. So you are aware of "how much" certain color means
And also see how the numbers change according to your election.



        4.- ROOM FOR IMPROVEMENT
This, more than an improvement is an alternative. As I said before, this app could support data from other industries and from different sources.
So yeah, you could use API's to call data on real time, pull data from a cloud database, or even use Web Scraping to build your dataset.
OBVIOUSLY you'll have to change the input and the column names. But that's an easy task.

Also the colorline bar could be placed outside the map, so it doesn't merge with the map colors. I'll make that change sometime in the future...



        5.- ABOUT ME
Hey there! Flavio Álvarez here. I'm a Data Scientist currently living in Mexico, with a good mileage and knowledge about Ecommerce.
I like videogames (as almost every other programmer, how unique), motorcycles, and I really love listening to 2000's rock.
You cand reach me on these links:
https://github.com/flavioAlvarezD
https://www.linkedin.com/in/flavio-alvarez-dorantes/

And thank you for reading this :D
