import googlemaps

class cookieMaker():
    def __init__(self) -> None:
        pass
    def generate_cookie(state, address, city):

        #My gmaps API key 
        gmaps_key = googlemaps.Client("API KEY HERE")

        #This is a part of the cookia data that minibar saves, but doesn't actually effect the scraping data
        fakeLocal_id = "0435b4ab-1b89-41c2-8506-14b922cfe2df"

        gmaps_input_address = address + ", " + city + " " + state

        g = gmaps_key.geocode(gmaps_input_address)

        lat = g[0]["geometry"]["location"]["lat"]
        long = g[0]["geometry"]["location"]["lng"]
        place = g[0]["place_id"]
        formatted_address = g[0]["address_components"][0]["long_name"] + " " + g[0]["address_components"][1]["long_name"]
        areaCode = g[0]["address_components"][6]["long_name"]

        #building JSON String
        Json_location_str = "{\"address1\":\"" + formatted_address + "\",\"city\":\"" + city + "\",\"place_id\":\"" + place + "\",\"latitude\":" + str(lat) + ",\"local_id\":\"" + fakeLocal_id+ "\",\"longitude\":" + str(long) + ",\"state\":\"" + state + "\",\"zip_code\":\"" + areaCode + "\"}"

        return (Json_location_str)
