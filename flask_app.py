from flask import Flask, jsonify, make_response, render_template, request
from flask_restful import Api, Resource, reqparse, url_for
from scraperMain import scrape
import pandas as pd

app = Flask('Minibar_Scraper', template_folder='templates')
api = Api(app)

#First screen with form 
@app.route('/')
def form():
    return render_template("form.html")

#Second screen to display data
@app.route('/data', methods = ['POST', 'GET'])
def data():

    #Incase user trys to access data before filling out form
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form

        #metadata from beverage in meta_list
        meta_list = queryOne(form_data['Beverage'])

        #store pricing data in addy list using metadata url 
        addy_list = queryAddy(form_data['State'], form_data['City'], form_data['Address'], meta_list[len(meta_list) - 1])
        ret_list = []
        i = 0

        #formatting data for output
        while i < (len(meta_list) - 1):
            ret_list.append(str(meta_list[i]) + ": " + str(meta_list[i + 1]))
            i = i + 2
        i = 0
        while i < (len(addy_list) - 1):
            ret_list.append(str(addy_list[i]) + ": " + str(addy_list[i + 1]))
            i = i + 2

        #passing data to data template
        return render_template('data.html', data = ret_list)
    
def queryOne(beverage):
    query_url = scrape.queryBuilder(str(beverage))
    meta_list = scrape.scrapeInitialMeta(query_url)
    retD = {}
        
    i = 0
    while i < (len(meta_list) - 1):
        retD[meta_list[i]] = meta_list[i + 1]
        i = i + 2

    return meta_list


def queryAddy(state, city, addy, queryUrl):
    queryUrl = queryUrl
    address = addy
    state = state
    city = city

    result = scrape.scrapeByAddress(state, city, address, queryUrl)
    storeNum = 1
    retList = []
    for storeData in result:
        i = 0
        retList.append("Store Number")
        retList.append(str(storeNum))
        while i < (len(storeData) - 1):
            retList.append(str(storeData[i]))
            retList.append(str(storeData[i + 1]))
            i = i + 2
        storeNum = storeNum + 1
    return retList

if __name__ == '__main__':
    app.run()