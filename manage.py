import os
import pandas as pd

from app import manager, models as m
from datetime import datetime, time, timedelta
from app.bhav_scrapper import bhav_scrapper
from app.db_operation import check_symbol, check_stocks_minute

csv_files_path = os.getcwd()+"/CSV_files"
log_path = os.getcwd()+"/logs"
   
@manager.command
def check_integrity_stocks(start_date, end_date):
    files_path = csv_files_path+"/stocks"
    try:
        start_date_arg = datetime.strptime(start_date, '%d/%m/%Y')
        end_date_arg = datetime.strptime(end_date, '%d/%m/%Y')
    except:
        return "check date format"
    
    date_generated = [start_date_arg + timedelta(days=x) for x in range(0, ((end_date_arg-start_date_arg).days)+1)]
    file_list = [file for file in os.listdir(files_path) if file.split(".")[1] == "csv"]
    
    if not os.path.exists(log_path):
        os.makedirs(log_path)    
    log_file = log_path+"/stock candle missing "+str(datetime.now())+".txt"
    new_file = open(log_file,"a")  
    for file in file_list:
        date = file.split(".")[0][-8:]
        file_date = datetime.strptime(date, '%d%m%Y')
        if file_date in date_generated:
            df = pd.read_csv(files_path+"/"+file)
            df.dropna(inplace=True)
            missed_tick = []
            all_tick = [x for x in df[df.columns[0]].unique() if x.strip()!="Ticker"]
            for ticker in all_tick:
                if ticker.split(".")[1] != "NSE":
                    continue
                tick_df = df[df[df.columns[0]] == ticker]
                vol = tick_df[df.columns[7]].astype("float").sum()
                bhav_price = m.db.session.query(m.Stocks_bhav.total_trade_qty).filter_by(trading_symbol=ticker.split(".")[0], timestamp=file_date).first()
                if bhav_price and float(bhav_price[0]) != vol:
                    missed_tick.append(ticker)
                else:
                    continue
            if len(missed_tick) >= 1:
                date = file_date.strftime("%d-%m-%Y")
                print("{"+date+":"+str(missed_tick)+"}\n\n")
                new_file.write("{"+date+":"+str(missed_tick)+"}\n\n")
    new_file.close
    return "Log generated"

            
@manager.command
def check_files_stocks(start_date, end_date):
    files_path = csv_files_path+"/stocks"
    try:
        start_date_arg = datetime.strptime(start_date, '%d/%m/%Y')
        end_date_arg = datetime.strptime(end_date, '%d/%m/%Y')
    except: 
        return "check date format"
    
    scrap = bhav_scrapper(start_date_arg,end_date_arg)
    cal = scrap.get_cal()
    trade_day = cal.networkdays()
    file_list = [file for file in os.listdir(files_path) if file.split(".")[1] == "csv"]
    file_dates = list()
    for file in file_list:
        try:
            date = file.split(".")[0][-8:]
            file_date = datetime.strptime(date, '%d%m%Y')
        except:
            return "Make sure file naming is correct"
        
        if file_date:
            file_dates.append(file_date)
    
    missing_list = list_diff(trade_day,file_dates)
    
    if not os.path.exists(log_path):
        os.makedirs(log_path)    
    log_file = log_path+"/stock file missing "+str(datetime.now())+".txt"
    new_file = open(log_file,"a+")
    new_file.write(str(missing_list))
    new_file.close
    return "Log generated"

@manager.command
def insert_stock_minute(start_date, end_date):
    files_path = csv_files_path+"/stocks"
    try:
        start_date_arg = datetime.strptime(start_date, '%d/%m/%Y')
        end_date_arg = datetime.strptime(end_date, '%d/%m/%Y')
    except: 
        return "check date format"
    
    all_dates = [start_date_arg + timedelta(days=x) for x in range(0, (end_date_arg-start_date_arg).days)]
    
    file_list = [file for file in os.listdir(files_path) if file.split(".")[1] == "csv"]

    for file in file_list:
        try:
            date = file.split(".")[0][-8:]
            file_date = datetime.strptime(date, '%d%m%Y')
        except:
            return "Make sure file naming is correct"
        
        if file_date in all_dates:
            df = pd.read_csv(files_path+"/"+file, error_bad_lines=False, index_col=False, dtype='unicode')
            for index, row in df.iterrows():
                try:
                    symbol = row["Ticker"].split(".")[0]
                    datetime_str = row["Date"]+" "+row["Time"]
                    dt_table = datetime.strptime(datetime_str, "%d-%m-%Y %H:%M:%S")
                    open = float(row["Open"])
                    high = float(row["High"])
                    low = float(row["Low"])
                    close = float(row["Close"])
                    volume = float(row["Volume"])
                except:
                    continue
                cond_1 = check_symbol(symbol, m.instrument_type.equity.value)
                cond_2 = check_stocks_minute(symbol, dt_table)
                if cond_1 == True and cond_2 == False:
                    m.db.session.add(
                        m.Stocks_minute(
                            trading_symbol = symbol,
                            datetime = dt_table,
                            open = open,
                            high = high,
                            low = low,
                            close = close,
                            volume = volume
                        )
                    )
                elif cond_1 == False:
                    print("Ticker name is not correct or not in database:- ",symbol)
                    continue
                
                elif cond_2 == True:
                    print("Data is already present:- {} of time {}".format(symbol,dt_table))
                    continue
            m.db.session.commit()
    

def list_diff(trade_day,dates):
#     print("this is start")
    ab_data = list()
    for i in trade_day:
        if i not in dates:
            ab_data.append(i)
    return ab_data
    
        

if __name__ == "__main__":
    manager.run()