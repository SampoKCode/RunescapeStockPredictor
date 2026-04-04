import api_calls


# buylimit, names and daily volume calc come locally


### lists for parsing timeseries data

def low_volume_list(timeseries_data):
    return 0

def low_price_list(timeseries_data):
    return 0

### numerical calculations

def daily_volume(lowvol_list):
    # add up daily volume from list
    return 0

def buylimit_amt(daily_vol,buylimit):
    # divide daily vol by buylimit
    return 0

def expected_value(lowvol_list,lowprice_list,daily_vol):
    # calculate expected value
    return 0

def avg_dip_percent(ev,curr_low):
    # calculate avg dip %
    return ev/curr_low-1

def daily_low_diff(sys_time,low_time):
    # calc time differential between when price was lowest
    # and now
    return 0

### actual result parsing

def get_candidates_list(latest_list,name_list,return_amt):
    # calculate latest 5m hi-lo * volume/buylimit
    # for each id and take return_amt of the best
    return 0

def evaluation():
    # evaluate the best items to buy, do all of the 
    # screenings to get best items in order
    return 0

def main():
    print("hello world, testing the eval process here")
    return 0


if __name__ == "__main__":
    main()