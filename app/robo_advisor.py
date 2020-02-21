# app/robo_advisor.py

import csv
import json
import os

from dotenv import load_dotenv


import requests

load_dotenv()

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

#included in the python language so we don't have to install anything
#
#

#

#API_KEY = os.environ["ALPHAVANTAGE_API_KEY"] - not going to use 
#API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY") - not going to use 
#API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default="OOPS") - going to use

#symbol = "TSLA" # todo: ask for a user input

#request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
#print("URL:", request_url)

#print("REQUESTING SOME DATA FROM THE INTERNET...")
#response = requests.get(request_url)
#print(type(response))
#print(response.status_code)
#print(type(response.text)) #> str

# handle response errors:
#if "Error Message" in response.text:
    #print("OOPS couldn't find that symbol, please try again")
    #exit()

#parsed_response = json.loads(response.text)
#print(type(parsed_response)) #> dict

#print(parsed_response)

#breakpoint()
#End of inclass
#2/20 going to work below here: 

#
# Info Inputs
#
api_key = API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default="OOPS")
symbol = "MSFT"  #going to ask user
request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"

response = requests.get(request_url)
#print(type(response))
#print(response.status_code) #>200 which means it was successfull
#print(response.text) # response text is a str so we need to use the JSON module to process it into a dictionary, what we want to do is parse the response from a string into a dictionary 

parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]   #want to print this out instead of the hard coded Latest Day (can format f it (interpolate) or use string concatination)

tsd = parsed_response["Time Series (Daily)"]

dates = list(tsd.keys())

latest_day = dates[0] #0 is the first item in the list (assuming the latest day is first, might need to update if we dont sort )
latest_close = tsd[latest_day]["4. close"]


#get the high price from each day
high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))

#max of all high prices 
recent_high = max(high_prices)
recent_low = min(low_prices)


#breakpoint()




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





###

print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print(f"WRITING DATA TO CSV FILE: {csv_file_path}...")
print("HAPPY INVESTING!")
print("-------------------------")

#in class 2/19
#selected_stock = input("Please Input Selected Stock Symbol")
