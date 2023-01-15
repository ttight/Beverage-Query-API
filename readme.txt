PROJECT: Build a scraper that allows a user to query basic procuct metadata
for beverages.

This repo containes 6 Files: Below is a description of their function


scraperMain: This file contains the class scraper, which containes methods to 
extract the relevant data from minibar given the beverage and address as inputs

addressCookieBulder: This file contains the class cookieMaker, which given
an address will build the cookie specific to minibars cookie requirements 
using google maps api, then reurn that cookie in its JSON format

flask_app: This file implements flask to show the two HTML templates,
take in input, and then utilize scrapermain to compute the desired data,
then shows the data. 

flask_api: This file is similar to flask_app, however it allows for 
two endpoints /metaQuery and /addyQuery and which take in the same
beverage and address input within the url to produce the JSON format
of the desired data.

form.html: This is a HTML template to display the form and take inputs
used in flask_app 

data.html: This is a HTML template to display the data retreived in
flask_app using the inputs from form.html


Notes:

    - One shortcoming of this project is that minibar only shows the first three 
    (theoretically most relevant) stores that carry the product. This is because
    minabar requires the user to click the show more stores button to reveal
    the new data in the HTML for the other stores. Therefore, the scraper
    will only show a max of 3 stores for each product. 

    - If minibar does not have any stores that sell a product partered with them
    then the scraper will not show anything in regards to product price and availability.

