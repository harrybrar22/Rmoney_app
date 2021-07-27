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
         
        ticker = "STK_"+row[0]

        data_exists = m.db.session.query(
            m.db.session.query(m.Stocks_bhav).filter_by(trading_symbol=ticker, timestamp = tstamp).exists()
            ).scalar()
        
        if data_exists == True:
            continue
        else:
            symbol_exists = m.db.session.query(
                m.db.session.query(m.Instrument).filter_by(trading_symbol=ticker).exists()
                ).scalar()

            if symbol_exists == False:
                add_symbol = m.Instrument(
                    trading_symbol = ticker,
                    type = m.instrument_type.equity.value
                )
                m.db.session.add(add_symbol)
                m.db.session.commit()
            else:
                pass
            
            data = m.Stocks_bhav(
                trading_symbol = ticker,
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

        # STOCK FUTURE symbol:- FUTSTK_"symbol"_expiry(DD-MM-YYYY)
        # INDEX FUTURE symbol:- FUTIDX_"symbol"_expiry(DD-MM-YYYY)
        # STOCK OPTION symbol:- OPTSTK_"symbol"_expiry(DD-MM-YYYY)_strike(in paisa)_optiontype(CE/PE)
        # INDEX OPTION symbol:- OPTIDX_"symbol"_expiry(DD-MM-YYYY)_strike(in paisa)_optiontype(CE/PE)
        
        exp_date = datetime.strptime(row[2], "%d-%b-%Y")
        ex_date = exp_date.strftime("%d-%m-%Y")
        inst_type = row[0].strip()
        if inst_type == "FUTSTK":
            Ticker = "FUTSTK_"+row[1]+"_"+ex_date
        elif inst_type == "FUTIDX":
            Ticker = "FUTIDX_"+row[1]+"_"+ex_date
        elif inst_type == "OPTSTK":
            Ticker = "OPTSTK_"+row[1]+"_"+ex_date+"_"+row[3]+"_"+row[4]
        elif inst_type == "OPTIDX":
            Ticker = "OPTIDX_"+row[1]+"_"+ex_date+"_"+row[3]+"_"+row[4]
        else:
            continue        
        
        data_exists = m.db.session.query(
            m.db.session.query(m.Futures_opt_bhav).filter_by(trading_symbol=Ticker, timestamp = datetime.strptime(row[14], "%d-%b-%Y")).exists()
            ).scalar()

        if data_exists == True:
            continue
        else:
            symbol_exists = m.db.session.query(
                m.db.session.query(m.Instrument).filter_by(trading_symbol=Ticker).exists()
                ).scalar()
            
            if symbol_exists == True:
                continue
            
            if row[4] == "PE":
                options = m.option_type.pe.value
            elif row[4] == "CE":
                options = m.option_type.ce.value
            else:
                options = m.option_type.null.value

            add_symbol = m.Instrument(
                trading_symbol = Ticker,
                type = m.instrument_type.futures.value
            )
            m.db.session.add(add_symbol)
            m.db.session.commit()
            data = m.Futures_opt_bhav(
                trading_symbol = Ticker,
                expiry_date = datetime.strptime(row[2], "%d-%b-%Y"),
                strike_pr = float(row[3]),
                option_typ = options,
                open = float(row[5]),
                high = float(row[6]),
                low = float(row[7]),
                close = float(row[8]),
                settle_pr = float(row[9]),
                contracts = int(row[10]),
                val_inlakh = float(row[11]),
                open_int = int(row[12]),
                chg_in_oi = int(row[13]),
                timestamp = datetime.strptime(row[14], "%d-%b-%Y")
            )
            m.db.session.add(data)    
            m.db.session.commit()
    return True
            
