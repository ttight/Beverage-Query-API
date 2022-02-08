from bs4 import BeautifulSoup
from urllib import request
import lxml.html
from lxml import html
from addressCookieBuilder import cookieMaker
import requests

#This class contains all of the scraping functions
class scrape: 
    def __init__(self) -> None:
        pass

    prod_url_hold = ""

    def scrapeInitialMeta(url):
        retStrList = []
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

        page_request = request.Request(url , headers= headers)
        page = request.urlopen(page_request)

        soup = BeautifulSoup(page, 'html.parser')

        #finding all items with from their class tag name in the search page
        product_text_list = soup.find_all("li",{"class": "ProductTile_element__KRgs2"})

        #Arbitrarily picking the first element that comes up in the sarch page 
        selected_product_text = product_text_list[0]

        #Extracting the url to the product page for that product
        data_url_tag = str(selected_product_text).split("data-url=")[1]
        prod_url = data_url_tag.split("\"")[1]

        #Begin scraping the prod page for that item
        prod_page_request = request.Request(prod_url, headers = headers)
        prod_page = request.urlopen(prod_page_request)
        prod_soup = BeautifulSoup(prod_page, 'html.parser')
        
        retStrList.append("Description")
        retStrList.append(str(scrape.findDiscription(prod_soup)))

        #After extracting the description find stats takes into account the variety of types of potential stats
        Stat_list = scrape.findStats(prod_soup)

        for stat in Stat_list:
            retStrList.append(str(stat))
        
        prod_url_hold = prod_url

        #return product selected url
        retStrList.append("Product Page Url")
        retStrList.append(prod_url)

        #Returns a list with all of the data we're looking for
        return (retStrList)

    def queryBuilder(UserInput):
        query_split = UserInput.split()
        query = ""
        for i in range(len(query_split)):
            if i < len(query_split) - 1:
               query += query_split[i] + "+"
            else:
               query += query_split[i]
        return ("https://minibardelivery.com/store/search/" + query + "?q=" + query)



    def get_product_text_name(prod_text):
        prod_text = str(prod_text)
        prod_text = prod_text.split("li aria-label=")[1]
        prod_text = prod_text.split("\"")[1]
        return(prod_text)
    
    def findStats(prod_soup):
        x = prod_soup.find_all("tr", {"class": "ProductProperties_tr__T3nDP"})
        ret_list = []
        i = 0
        for stat_item in x:
            stat_item = str(stat_item)
            start = stat_item.find("itemprop=\"name\"") + 16
            end = stat_item.find("</th>") 
            start2= stat_item.find("value") + 7
            end2 = stat_item.find("</td>")
            Str = stat_item[start:end] + ": " + stat_item[start2:end2]
            ret_list.append(stat_item[start:end])
            ret_list.append(stat_item[start2:end2])
        return(ret_list)
    
    def findDiscription(prod_soup):
        x = prod_soup.find("pre",{"itemprop": "description"})
        x = str(x).split("itemprop=")[1]
        start = x.find(">") + 1
        end = x.find("</pre>")
        return(x[start:end])

    def scrapeByAddress(state, city, address, url):
        my_built_cookie = cookieMaker.generate_cookie(state, address, city)
        cookies_address = dict(name = "mb_address", value = my_built_cookie)

        response = requests.get(url = url, cookies = cookies_address)
        cookies_jar = requests.cookies.RequestsCookieJar()
        cookies_jar.set('mb_address', my_built_cookie, domain='minibardelivery.com', path='/')

        response = requests.get(url, cookies=cookies_jar)

        tree = lxml.html.fromstring(response.text)

        items = tree.find_class("OfferItem_itemContent__xneaF")
        return (scrape.scrapeItemsFromAddressPage(items))

    def scrapeItemsFromAddressPage(items):
        bigList = []
        for item in items:
            retList = []
            item = str(html.tostring(item))
            startName = item.find("itemprop=\"name\">") + 16
            endName = item.find("</h2")
            name = item[startName:endName]
            startPrice = item.find("\"price\">") + 8
            endPrice = startPrice + 8
            closeToPrice = item[startPrice:endPrice]
            endIndex = closeToPrice.find(".") + 3
            price = closeToPrice[0:endIndex]
            startDel = item.find("Delivery:")
            endDel = startDel + 40
            closeToDel = item[startDel:endDel]
            endIndex2 = closeToDel.find("</span") 
            delivery = closeToDel[10:endIndex2]
            startDist = item.find("TNKKc") + 7
            endDist = startDist + 10
            closeToDist = item[startDist:endDist]
            endIndex3 = closeToDist.find("</s")
            dist = closeToDist[0:endIndex3]
            if delivery.find("<div") > 0:
                delivery = "N/A"
            if dist.find("class") > 0:
                dist = "N/A"

            retList.append("Store Name")
            retList.append(str(name))
            retList.append("Price")
            retList.append(str(price))
            retList.append("Delivery")
            retList.append(str(delivery))
            retList.append("Distance")
            retList.append(str(dist))
            bigList.append(retList)

        
        return (bigList)
    
