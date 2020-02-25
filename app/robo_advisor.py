# app/robo_advisor.py

import csv
import json
import os

from dotenv import load_dotenv


import requests

import datetime

load_dotenv()

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

#
# Info Inputs
#
api_key = API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default="OOPS")
symbol = input("PLEASE INPUT SELECTED STOCK SYMBOL:  ")
while True:
    if symbol.isdigit():
        print("SORRY, INCORRECT INPUT")
        exit()
    else:
        print("                                         ")
        print("-------------------------")
        print("REQUESTING SOME DATA FROM THE INTERNET...")
        break
        

#want a do not get if it meets certain requirements

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"

response = requests.get(request_url)
#print(type(response))
#print(response.status_code) #>200 which means it was successfull
#print(response.text) # response text is a str so we need to use the JSON module to process it into a dictionary, what we want to do is parse the response from a string into a dictionary 

if "Error Message" in response.text:
    print("OOPS,  PLEASE TRY AGAIN")
    exit()

parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]   #want to print this out instead of the hard coded Latest Day (can format f it (interpolate) or use string concatination)

tsd = parsed_response["Time Series (Daily)"]

dates = list(tsd.keys())

latest_day = dates[0] #0 is the first item in the list (assuming the latest day is first, might need to update if we dont sort )
latest_close = tsd[latest_day]["4. close"]


#VALIDATION: 

#get the high price from each day
high_prices = []
low_prices = []
closing_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))
    closing_price = tsd[date]["4. close"]    
    closing_prices.append(float(closing_price))  

#max of all high prices 
recent_high = max(high_prices)
recent_low = min(low_prices)

moving_average = sum(closing_prices)/100 #Alphavantage only gives you the last 100 days of data 
#moving average works (matches internet info) so now just write the recommendation system

now = datetime.datetime.now()

x = float(latest_close)
y = float(moving_average)

if x >= y:
    stock_rec = "BUY"
    stock_reason = "WHEN COMPARING THE LATEST CLOSING PRICE OF THE STOCK TO THE STOCK'S MOVING AVERAGE, THERE SEEMS TO BE SIGNS INDICATING A LONG TERM UPWARD TREND IN THE VALUE OF THE STOCK"
else: 
    stock_rec = "SELL"
    stock_reason = "WHEN COMPARING THE LATEST CLOSING PRICE OF THE STOCK TO THE STOCK'S MOVING AVERAGE, THERE SEEMS TO BE SIGNS INDICATING A LONG TERM DOWNWARD TREND IN THE VALUE OF THE STOCK"
    
#Info Outputs


#write it to csv , start with copy and paste from csv repo on github: 

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv") # a relative filepath

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above
    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close":daily_prices["4. close"],
            "volume":daily_prices["5. volume"]
        })

#time to write  a recommendation system - Simple Moving Averages
#idea source: https://www.investopedia.com/articles/active-trading/052014/how-use-moving-average-buy-stocks.asp
#recommendation is BUY if equal to or above the 100 Day SMA & SELL if below SMA
#reason is below SMA = long term trending downwards, above SMA = long term trending upwards

###

print("-------------------------")
print("SELECTED SYMBOL: " + symbol)
print("-------------------------")
print("REQUESTING STOCK MARKET DATA")
print("REQUEST AT: " + (now.strftime("%m/%d/%Y %H:%M%p")))
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print(f"100 DAY MOVING AVERAGE: {to_usd(float(moving_average))}")
print("RECOMMENDATION: " + stock_rec)
print("RECOMMENDATION REASON: " + stock_reason)
print("-------------------------")
print(f"WRITING DATA TO CSV FILE: {csv_file_path}...")
print("HAPPY INVESTING!")
print("-------------------------")
