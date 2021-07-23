from datetime import datetime
from app import models as m

def check_symbol(symbol, type):
    exists = m.db.session.query(
            m.db.session.query(m.Instrument).filter_by(trading_symbol=symbol, type=type).exists()
            ).scalar()
    return exists

def insert_symbol(symbol, type):
    add_symbol = m.Instrument(
            trading_symbol = symbol,
            type = type
        )
    m.db.session.add(add_symbol)
    m.db.session.commit()
    return True

def check_stocks_minute(symbol, timestamp):
    data_exists = m.db.session.query(
            m.db.session.query(m.Stocks_minute).filter_by(trading_symbol=symbol, datetime = timestamp).exists()
            ).scalar()
    return data_exists


    