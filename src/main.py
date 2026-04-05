import api_calls
import json
import time


# buylimit, names come from mapping.json

### numerical calculations

def apply_tax(high_price):
    GE_TAX = 0.02
    # apply GE tax to sold item
    return high_price*(1-GE_TAX)+1

def buylimit_formula(buylimit,daily_vol,BL_coef):
    # formula for giving weighting for better buylimit/dailyvol ratios
    # gives numbers 0...1 based on whether
    # buylimit/dailyvol = BL_coef is close or not,
    # punishing undershots more than overshots
    return (1/(abs(1-buylimit/daily_vol*BL_coef)+1))

### actual result parsing for flipping purposes

def volatile_maximised_candidates():
    # TODO This returns a list of id's that have had substantial
    # selling activity in the past hour (comparing 24h and 1h data)
    # TODO api calls (other page) , algorithm for comparing 24h and 1h
    return 0


def profit_maximised_candidates(return_amt, mode="roi"):
    # Does the preparsing of possible items 
    # based on ROI and and difference between daily avg 
    # and current price
    # TODO make two modes "roi"(current) and "money"(overall money-amount)
    # where money will not care about roi (as long as it is positive)
    # "money" will be sorted by individual profit margins

    # get a list of id's that pass the following checks:
    # - GE tax corrected 5m ROI is ok, push out all below 0%
    # - daily low avg is a certain percentage higher than curr low
    latest_data = api_calls.get_latest_data()
    daily_data = api_calls.get_daily_data()
    candidate_list = {} # {id: [roi,price_dip]}
    ROI_TARGET = 0
    DIP_TARGET = 0
    VOLATILE_ITEM_SIFTER = 10
    
    for id,metrics in latest_data.get("data").items():
        try:
            latest_high = metrics["avgHighPrice"]
            latest_low = metrics["avgLowPrice"]
            daily_low = daily_data.get("data")[id]["avgLowPrice"]
            daily_high = daily_data.get("data")[id]["avgHighPrice"]
        except KeyError:
            continue
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
            candidate_list[id] = [round(roi,4),round(dip_percent,4)]
    timestamp = latest_data.get("timestamp")
    # for each id and take return_amt of the best
    sorted_c_list = sorted(candidate_list.items(),key=lambda item: item[1][1],reverse=True)
    cut_list = dict(sorted_c_list[VOLATILE_ITEM_SIFTER:return_amt+VOLATILE_ITEM_SIFTER])
    return cut_list, timestamp

def evaluation():
    # returns {id: [roi, price_dip, low_time_diff, 
    # buylimit_coef, price_times_limit]}
    # the closer to 1 buylimit_coef is, the better.
    # NOTE: this looks only at low prices, i.e. instasell prices,
    # selling the items is another calculators job.
    CANDIDATE_AMT = 10
    ### index enums
    NAME_E = 0
    LIMIT_E = 1
    ROI_E = 0
    PRICE_DIP_E = 1
    LOW_TIME_DIFF_E = 2
    BUYLIMIT_COEF_E = 3
    PRICE_TIMES_LIMIT_E = 4
    # what is the "ideal amount of "buylimit/volume"
    BUYLIMIT_COEF = 50 
    CURR_TIME = int(time.time())

    with open("name_limit_list.json","r") as file:
        name_limit_list = json.load(file)
    candidate_list, latest_time = profit_maximised_candidates(CANDIDATE_AMT)
    

    for id in candidate_list.keys():
        daily_volume = 0
        low_price = 2147483647 # lower is better, start at max cash
        buylimit = name_limit_list.get(id)[LIMIT_E]
        time_diff = 10000000 # lower is better, giga number by default
        latest_price = None
        
        # calculate lowest time and compare it to current unix time
        # add up the volumes to get daily volume for each item
        timeseries_data = api_calls.get_timeseries_data(id)
        for data_point in timeseries_data.get("data"):
            curr_timediff = CURR_TIME-data_point["timestamp"]
            curr_lowprice = data_point["avgLowPrice"]
            if curr_lowprice != None and curr_lowprice < low_price:
                low_price = curr_lowprice
                time_diff = curr_timediff
            latest_price = curr_lowprice
            daily_volume += data_point["lowPriceVolume"]
        candidate_list.get(id).append(time_diff)
        buylimit_coef = buylimit_formula(buylimit,daily_volume,BUYLIMIT_COEF)
        candidate_list.get(id).append(buylimit_coef)
        candidate_list.get(id).append(buylimit*latest_price)
        
    
    # testing suite
    # returns {id: [roi, price_dip, low_time_diff, 
    # buylimit_coef, price_times_limit]}
    for id, values in candidate_list.items():
        # Safely extract with a default of None if index is out of bounds
        roi           = values[0] if len(values) > 0 else None
        price_dip     = values[1] if len(values) > 1 else None
        time_diff     = values[2] if len(values) > 2 else None
        buylimit_coef = values[3] if len(values) > 3 else None
        investment    = values[4] if len(values) > 4 else None
        name_entry = name_limit_list.get(id)
        name = name_entry[NAME_E] if name_entry else "N/A"

        print(f"name: {name}")
        print(f"ROI: {f'{roi*100}%' if roi is not None else 'N/A'}")
        print(f"PriceDip: {f'{price_dip*100}%' if price_dip is not None else 'N/A'}")

        time_str = f"{time_diff // 60} minutes" if time_diff is not None else "N/A"
        print(f"Time since lowest price: {time_str}")

        print(f"Buylimit coefficent: {buylimit_coef if buylimit_coef is not None else 'N/A'}")
        print(f"Investment amount: {f'{investment} GP' if investment is not None else 'N/A'}")
    


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