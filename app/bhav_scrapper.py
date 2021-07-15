import requests
from datetime import datetime
from bs4 import BeautifulSoup as bs
from networkdays import networkdays
from io import BytesIO
from zipfile import ZipFile


class bhav_scrapper():
    def __init__(self, start_date, end_date):
        self.fo_bhav_url = "https://archives.nseindia.com/content/historical/DERIVATIVES/{}/{}/fo{}bhav.csv.zip"
        self.holiday_url = "https://zerodha.com/z-connect/traders-zone/holidays/trading-holidays-{}-nse-bse-mcx"
        self.stock_bhav_url = "https://www1.nseindia.com/content/historical/EQUITIES/{}/{}/cm{}bhav.csv.zip"
        self.start_date = start_date
        self.end_date = end_date
        
    def get_cal(self):
        start_year = self.start_date.year
        end_year = self.end_date.year + 1
        holiday = list()
        for year in range(start_year, end_year):
            cal_scrap = requests.get(self.holiday_url.format(year))
            soup  = bs(cal_scrap.text, "html5lib")
            tables = soup.table
            all_dates = tables.find_all("td")
            for c in range(0,len(all_dates)):
                try:
                    if (start_year == 2015):
                        date_str = all_dates[c].text.strip()+","+str(year)
                    elif (start_year == 2014):
                        date_str = all_dates[c].text[:-2]+","+str(year)
                    else:
                        d1 = all_dates[c].text.split(",")[0].strip()
                        d2 = all_dates[c].text.split(",")[1].strip()
                        date_str = d1+","+d2
                    date = datetime.strptime(date_str, '%B %d,%Y')
                except:
                    continue
                if date:
                    holiday.append(date)
        trade_cal = networkdays.Networkdays(self.start_date, self.end_date, holiday)
        return trade_cal
        
    def bhav_scrap_futures(self, trade_cal):
        trade_day = sorted(trade_cal.networkdays())
        all_entries = list()
        for day in trade_day:
            month = day.strftime("%b").upper()
            date = day.strftime("%d%b%Y").upper()
            response = requests.get(self.fo_bhav_url.format(day.year, month, date), stream=True)
            file = ZipFile(BytesIO(response.content))
            csv = file.read(file.namelist()[0]).decode('UTF8')
            str_entry = csv.split("\n")[1:]
            for one in str_entry:
                all_entries.append(one)
        return all_entries
    
    def bhav_scrap_stocks(self, trade_cal):
        trade_day = sorted(trade_cal.networkdays())
        all_entries = list()        
        for day in trade_day:
            month = day.strftime("%b").upper()
            date = day.strftime("%d%b%Y").upper()
            response = requests.get(self.stock_bhav_url.format(day.year, month, date), stream=True)
            file = ZipFile(BytesIO(response.content))
            csv = file.read(file.namelist()[0]).decode('UTF8')
            str_entry = csv.split("\n")[1:]
            for one in str_entry:
                all_entries.append(one)
        return all_entries       
                                    