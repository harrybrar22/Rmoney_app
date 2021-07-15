from app import models as m
from datetime import datetime
from datetime import datetime
from app.bhav_scrapper import bhav_scrapper


def get_stock_bhavcopy(start_date,end_date):
    try:
        start_date = datetime.strptime(start_date, '%d-%m-%Y')
        end_date = datetime.strptime(end_date, '%d-%m-%Y')
    except:
        return "Check date format"

    bhav = bhav_scrapper(start_date, end_date)
    calender = bhav.get_cal()
    all_entries = bhav.bhav_scrap_stocks(calender)
    parse_put_stock_bhav(all_entries)
    return "Data inserted"

def get_fut_opt_bhavcopy(start_date, end_date):
    try:
        start_date_c = datetime.strptime(start_date, '%d-%m-%Y')
        end_date_c = datetime.strptime(end_date, '%d-%m-%Y')
    except:
        return "Check date format"

    if start_date_c.year < 2014:
        return "Please enter 2014 or latest date"
    
    if start_date_c > end_date_c:
        return "INCORRECT DATE RANGE"
    
    bhav = bhav_scrapper(start_date_c, end_date_c)
    calender = bhav.get_cal()
    all_entries = bhav.bhav_scrap_futures(calender)
    parse_put_fo_bhav(all_entries)
    return "Data inserted"
    

def parse_put_stock_bhav(bhav_copy):   
    for entry in bhav_copy:  
        row = entry.split(",")[:]
        
        if "" in row:
            row.remove("")
        
        if not row:
            continue

        if row[1] and row[1] != "EQ":
            continue 
        
        try:
            tstamp= datetime.strptime(row[10], "%d-%b-%Y")
        except:
            try:
                tstamp= datetime.strptime(row[10], "%d-%b-%y")
            except:
                continue
         
        data_exists = m.db.session.query(
            m.db.session.query(m.Stocks_bhav).filter_by(trading_symbol=row[0], timestamp = tstamp).exists()
            ).scalar()
        
        if data_exists == True:
            continue
        else:
            symbol_exists = m.db.session.query(
                m.db.session.query(m.Instrument).filter_by(trading_symbol=row[0]).exists()
                ).scalar()

            if symbol_exists == False:
                add_symbol = m.Instrument(
                    trading_symbol = row[0],
                    type = m.instrument_type.equity.value
                )
                m.db.session.add(add_symbol)
            else:
                pass
            
            print(row)
            data = m.Stocks_bhav(
                trading_symbol = row[0],
                open = float(row[2]),
                high = float(row[3]),
                low = float(row[4]),
                close = float(row[5]),
                last = float(row[6]),
                prev_close = float(row[7]),
                total_trade_qty = int(row[8]),
                total_trade_val = float(row[9]),
                timestamp = tstamp,
                total_trades = int(row[11]),
                isin = row[12]
            )
            m.db.session.add(data)
    m.db.session.commit()
    
   
def parse_put_fo_bhav(bhav_copy):
    for entry in bhav_copy:
        row = entry.split(",")[:]
        
        if "" in row:
            row.remove("")
        
        if not row:
            continue 
        
        data_exists = m.db.session.query(
            m.db.session.query(m.Futures_opt_bhav).filter_by(trading_symbol=row[0], timestamp = datetime.strptime(row[10], "%d-%b-%Y")).exists()
            ).scalar()
        
        if data_exists == True:
            continue
        else:
            symbol_exists = m.db.session.query(
                m.db.session.query(m.Instrument).filter_by(trading_symbol=row[0]).exists()
                ).scalar()

            if symbol_exists == False:
                add_symbol = m.Instrument(
                    trading_symbol = row[0],
                    type = m.instrument_type
                )
                m.db.session.add(add_symbol)
            else:
                pass
            
            
            data = m.Futures_opt_bhav(
                trading_symbol = row[1],
                expiry_date = datetime.strptime(row[2], "%d-%b-%Y"),
                strike_pr = int(row[3]),
                option_type = m.option_type,
                open = float(row[2]),
                high = float(row[3]),
                low = float(row[4]),
                close = float(row[5]),
                last = float(row[6]),
                prev_close = float(row[7]),
                total_trade_qty = int(row[8]),
                total_trade_val = float(row[9]),
                timestamp = datetime.strptime(row[10], "%d-%b-%Y"),
                total_trades = int(row[11]),
                isin = row[12]
            )
        #     m.db.session.add(data)
    # m.db.session.commit()
            
            
    
    

