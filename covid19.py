import pandas as pd
import numpy as np
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

        #session = HTMLSession()
        try:
            r = requests.get(url, headers=header)
        #    page = session.get(url, headers=header)
            #print(r.content)
        except OSError as err:
            print("Unable to reach www.worldometers.info/coronavirus : Error is : " + str(err))


        # news =  page.html.find('#innercontent', first=True)

        try:
            nan_tables = pd.read_html(r.content)
        except Exception as err:
            print ("Error is +", str(err))
            exit(255)
        tables = nan_tables[0].replace(np.nan, 0)
        table = tables.values
        return table

class CountryStats:
    def __init__(self, table, country_name):
        self.table=table
        self.country_name=country_name

    def get_covid19_country_stats(self):
        found = 0
        #print(table)
        for row in self.table:
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


                #print("Serious Critical: ", int(row[7]) )
                #print("----------------------------------")
                found = 1
                return(cases)


        if found != 1 :
           return "Country not affected by Covid19 or may be misspelled country name?"
fd=FetchData(url)
table=fd.get_data()

country=input("Please enter country name : ")
p = CountryStats(table,country)
print(p.get_covid19_country_stats())

