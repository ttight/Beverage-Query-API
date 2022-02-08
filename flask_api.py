from flask import Flask, jsonify, make_response, render_template, request
from flask_restful import Api, Resource, reqparse, url_for
from scraperMain import scrape
import pandas as pd

app = Flask('Minibar_Scraper', template_folder='/Users/ttight/Desktop/Proj /templates')
api = Api(app)

#Query for product metadata
class queryProdMeta(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('query', required=True)
        args = parser.parse_args()

        query = args['query']
        query_url = scrape.queryBuilder(str(query))
        meta_list = scrape.scrapeInitialMeta(query_url)
        retD = {}
        
        i = 0
        while i < (len(meta_list) - 1):
            retD[meta_list[i]] = meta_list[i + 1]
            i = i + 2

        return make_response(jsonify(retD), 200) 


#Query for address *requires url from json in metadata scrape
class queryAddy(Resource):
    def get(self):
        retD = {}
        parser = reqparse.RequestParser()
        parser.add_argument('state', required=True)
        parser.add_argument('city', required=True)
        parser.add_argument('address', required=True)
        parser.add_argument('queryUrl', required=True)
        args = parser.parse_args()

        queryUrl = args['queryUrl']
        address = args['address']
        state = args['state']
        city = args['city']

        result = scrape.scrapeByAddress(state, city, address, queryUrl)
        storeNum = 0

        for storeData in result:
            i = 0
            retD[storeNum] = {}
            while i < (len(storeData) - 1):
                retD[storeNum][str(storeData[i])] = storeData[i + 1]
                i = i + 2
            storeNum = storeNum + 1
        return make_response(jsonify(retD), 200) 

#URL endpoints 
api.add_resource(queryProdMeta, '/metaQuery')
api.add_resource(queryAddy, '/addyQuery')

if __name__ == '__main__':
    app.run()