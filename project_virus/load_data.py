import requests
import json
import numpy
from datetime import date, timedelta
import pandas as pd

url = "https://covid-19-statistics.p.rapidapi.com/reports"

headers = {
    'x-rapidapi-host': "covid-19-statistics.p.rapidapi.com",
    'x-rapidapi-key': "5490de1e46mshe03fcf8c16e772fp1dfbd6jsn5b14620daf5f"
    }

def get_death_count(country, region, date):
    querystring = {"region_province":region,"iso":country,"date":date}
    response = requests.request("GET", url, headers=headers, params=querystring)
    if(len(json.loads(response.text)["data"]) == 0):
        return 0
    else:
        return json.loads(response.text)["data"][0]["deaths"]

def get_all_dates():
    sdate = date(2020, 3, 1)
    edate = date(2020, 5, 30)
    delta = edate - sdate
    return [(sdate + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(delta.days + 1)]

def get_confirmed_count(country, date):
    querystring = {"iso":country,"date":date}
    response = requests.request("GET", url, headers=headers, params=querystring)
    if(len(json.loads(response.text)["data"]) == 0):
        return 0
    else:
        j = json.loads(response.text)["data"]
        return sum(state["confirmed"] for state in j)

if __name__ == "__main__":
    result_list = [get_death_count("USA","New York",d) for d in get_all_dates()]
    statistics_dates = get_all_dates()
    result_list2 = [get_confirmed_count("USA",d) for d in get_all_dates()]
    data_dict1 = {"dates":statistics_dates, "deaths in NY":result_list}
    data_dict2 = {"dates":statistics_dates, "confirmed in USA":result_list2}
    df1 = pd.DataFrame(data_dict1)
    df2 = pd.DataFrame(data_dict2)
    df1.to_csv("New_York_deaths.csv")
    df2.to_csv("USA_confirmed.csv")

