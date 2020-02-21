# app/robo_advisor.py

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

#API_KEY = os.environ["ALPHAVANTAGE_API_KEY"]
#API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default="OOPS")

symbol = "TSLA" # todo: ask for a user input

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
print("URL:", request_url)

print("REQUESTING SOME DATA FROM THE INTERNET...")
response = requests.get(request_url)
print(type(response))
print(response.status_code)
print(type(response.text)) #> str

# handle response errors:
if "Error Message" in response.text:
    print("OOPS couldn't find that symbol, please try again")
    exit()

parsed_response = json.loads(response.text)
print(type(parsed_response)) #> dict

print(parsed_response)

#breakpoint()





print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print("LATEST DAY: 2018-02-20")
print("LATEST CLOSE: $100,000.00")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

#in class 2/19
#selected_stock = input("Please Input Selected Stock Symbol")
