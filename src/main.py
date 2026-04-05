import api_calls
import json


# buylimit, names come from mapping.json

### numerical calculations

def buylimit_amt(daily_vol,buylimit):
    # divide daily vol by buylimit
    return 0

def apply_tax(high_price):
    GE_TAX = 0.02
    # apply GE tax to sold item
    return high_price*(1-GE_TAX)+1

### actual result parsing

def get_candidates_data(name_limit_list,return_amt):
    # TODO cut based on ROI and return amt
    # TODO add ROI and price dip to candidate info
    
    # get a list of id's that pass the following checks:
    # - GE tax corrected 5m ROI is ok, push out all below 0%
    # - daily low avg is a certain percentage higher than curr low
    latest_data = api_calls.get_latest_data()
    daily_data = api_calls.get_daily_data()
    candidate_list = [] # list of id's
    ROI_TARGET = 0
    DIP_TARGET = 0
    
    for id,metrics in latest_data.get("data").items():
        try:
            latest_high = metrics["avgHighPrice"]
            latest_low = metrics["avgLowPrice"]
            daily_low = daily_data.get("data")[id]["avgLowPrice"]
            daily_high = daily_data.get("data")[id]["avgHighPrice"]
        except KeyError:
            continue
        # latest_high_vol = metrics["highPriceVolume"]
        # latest_low_vol = metrics["lowPriceVolume"]
        # If no perfect 5m data or daily data to flip on
        if (latest_high == None or 
            latest_low == None or
            daily_low == None or
            daily_high == None):
            continue
        # calculate latest ROI = hi/(hi-lo-hi//(1-ge_tax)+1) 
        roi = (apply_tax(latest_high)-latest_low)/apply_tax(latest_high)
        dip_percent = (apply_tax(daily_high)-daily_low)/2/latest_low
        if roi > ROI_TARGET and dip_percent > DIP_TARGET:
            candidate_list.append(id)
    timestamp = latest_data.get("timestamp")
    # for each id and take return_amt of the best
    # return candidate_list, timestamp
    return candidate_list, timestamp

def evaluation():
    # TODO 1. buylimit/daily_vol will affect how easily this
    # item will be bought, closer to 0 is better
    # (TODO daily_vol calculation based on the timeseries)
    # TODO 2. Time between daily low and current low
    CANDIDATE_AMT = 20
    ### index enums
    NAME = 0
    LIMIT = 1
    with open("name_limit_list.json","r") as file:
        name_limit_list = json.load(file)
    candidate_list, latest_time = get_candidates_data(CANDIDATE_AMT)
    for id in candidate_list:
        print(name_limit_list.get(id))



    # this function uses the timeseries api, relies on 
    # get_candidates_data to give best candidates
    # evaluate the best items to buy, do all of the 
    # screenings to get best items in order
    return 0

def main():
    print("hello world, testing the eval process here")
    evaluation()
    return 0


if __name__ == "__main__":
    main()