import pandas as pd
import numpy as np
from requests_html import HTML
import requests


url = "https://www.worldometers.info/coronavirus/"

class FetchData:
    def __init__(self, url):
        self.url=url

    def get_data(self):
        table = []
        #global news
        #header = {
        #    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        #    "X-Requested-With": "XMLHttpRequest"
        #}
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        try:
            r = requests.get(url, headers=header)
            page = r.content
        except OSError as err:
            print("Unable to reach www.worldometers.info/coronavirus : Error is : " + str(err))
            exit(254)
        return page

class CountryStats:
    def __init__(self, page, country_name):
        self.page=page
        self.country_name=country_name


    def get_covid19_country_stats(self):
        try:
            nan_tables = pd.read_html(self.page)
        except Exception as err:
            print ("Error is +", str(err))
            exit(255)
        tables = nan_tables[0].replace(np.nan, 0)
        table = tables.values

        found = 0
        for row in table:
            if row[0].lower() == self.country_name.lower():
                cases = {}
                cases["Country"] = str(row[0])
                cases["Total cases"] = int(float(str(row[1]).replace('+','').replace(',','')))
                cases["Active cases"] = int(float(str(row[6]).replace('+','').replace(',','')))
                cases["Total recovered"] = int(float(str(row[5]).replace('+','').replace(',','')))
                cases["Total deaths"] = int(float(str(row[3]).replace('+','').replace(',','')))
                cases["New cases"] = int(float(str(row[2]).replace('+','').replace(',','')))
                cases["New deaths"] = int(float(str(row[4]).replace('+','').replace(',','')))
                cases["Serious Critical"] = int(float(str(row[7]).replace('+','').replace(',','')))
                if cases["Total deaths"]  > 0 :
                    cases["Mortality ratio"] = round((cases["Total deaths"] * 100 / cases["Total cases"] ),2)
                else:
                    cases["Mortality ratio"] = 0

                found = 1
                return(cases)

        if found != 1 :
           return 255

class OverallStats:
    def __init__(self, page):
        self.page=page
        cases = {}

    def get_overall_stats(self):

        html = HTML(html=self.page)
        counters = html.find('#maincounter-wrap')
        main_counter = []
        cases = {}
        for entry in counters:
            main_counter.append((int(entry.text.split('\n')[1].replace(',', ''))))

        cases["Total cases"] = main_counter[0]
        cases["Total recovered"] = main_counter[2]
        cases["Total deaths"] = main_counter[1]
        cases["Active cases"] = cases["Total cases"]  - cases["Total recovered"] - cases["Total deaths"]
        cases["Mortality ratio"] = round((cases["Total deaths"] * 100 / cases["Total cases"] ),2)
        return(cases)

fd=FetchData(url)
page=fd.get_data()

country=input("Please enter country name : ")
p1 = CountryStats(page, country)
print(p1.get_covid19_country_stats())

p2 = OverallStats(page)
print(p2.get_overall_stats())
