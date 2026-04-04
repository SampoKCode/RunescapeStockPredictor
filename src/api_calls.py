import requests
import json

# lowvol_list, lowprice_list, low_time, curr_low, latest_list

baseurl = "https://prices.runescape.wiki/api/v1/osrs/"
headers = {
    "User-Agent": "RunescapeFlipPredictor, Discord: Lamp#9997"
}

def get_latest_data():
    # returns json of avgHighPrice avgLowPrice lowPriceVolume
    try:
        url = baseurl + "5m"
        response = requests.get(url)
        data = response.json()
        return data
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return 0

def get_timeseries_data(id):
    # returns timeseries data of given item
    # json of 
    # data{id{avgHighPrice,highPriceVolume,avgLowPrice,lowPriceVolume}},timestamp
    try:
        url = baseurl + "timeseries?timestep=5m&id=" + str(id)
        response = requests.get(url)
        data = response.json()
        return data
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return -1
    except Exception as err:
        print(f"An error occurred: {err}")
        return -1

def main():
    # for testing the api calls
    print("hello world from api, come back for testing")

    itemid = 4151
    # get latest data, can loop over them (i think)
    json_data = get_latest_data()
    print("individual items", json_data.get("data")[str(itemid)])
    print("timestamp", json_data.get("timestamp"))

    # get data of certain item (gives the same data)
    timeseries_data = get_timeseries_data(itemid)
    print("last five minute data", timeseries_data.get("data")[364])
    print("")
    return 0

if __name__ == "__main__":
    main()