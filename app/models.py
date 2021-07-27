from app import db
from enum import Enum

class instrument_type(Enum):
    equity= "EQ"
    options= "OPT"
    index= "IND"
    futures= "FUT"
    
class exchange(Enum):
    nse = "NSE"
    bse = "BSE"

class segment(Enum):
    equity = "NSE"
    options = "NFO-OPT"
    futures = "NFO-FUT"

class option_type(Enum):
    ce = "CE"
    pe = "PE"
    null = "null"

class Instrument(db.Model):
    __tablename__ = 'instrument'
    trading_symbol = db.Column(db.String(255), primary_key=True)
    type = db.Column(db.Enum(instrument_type), nullable=False)
    # stocks_rel = db.relationship("Stock")
    # futures_rel = db.relationship("Futures")
    # options_rel = db.relationship("Options")
    # index_rel = db.relationship("Index")
    # stock_min_rel = db.relationship("Stock_minute")
    # options_min_rel = db.relationship("Options_minute")
    # futures_min_rel = db.relationship("Future_minute")
    # index_min_rel = db.relationship("Index_minute")
    # stock_bhav_rel = db.relationship("")        
        

class Stocks(db.Model):
    __tablename__ = 'stocks'
    trading_symbol = db.Column(db.String(255), db.ForeignKey('instrument.trading_symbol'), primary_key=True)
    company_name = db.Column(db.String(255), nullable=False)
    tick_size = db.Column(db.Float, default=0.05)
    lot_size = db.Column(db.Integer, default=1)
    exchange = db.Column(db.Enum(exchange))
    listed_at = db.Column(db.DateTime)
    

class Futures(db.Model):
    __tablename__ = 'futures'
    trading_symbol = db.Column(db.String(255), db.ForeignKey('instrument.trading_symbol'), primary_key=True)
    underlying_symbol = db.Column(db.String(255))
    tick_size = db.Column(db.Float, default=0.05)
    lot_size = db.Column(db.Integer, default=1)
    segment = db.Column(db.Enum(segment))
    exchange = db.Column(db.Enum(exchange))
    listed_at = db.Column(db.DateTime)
    expiry_date = db.Column(db.Date)

class Options(db.Model):
    __tablename__ = 'options'
    trading_symbol = db.Column(db.String(255), db.ForeignKey('instrument.trading_symbol'), primary_key=True)
    underlying_symbol = db.Column(db.String(255))
    strike = db.Column(db.Float)
    right = db.Column(db.Enum(option_type))
    tick_size = db.Column(db.Float, default=0.05)
    lot_size = db.Column(db.Integer, default=1)
    segment = db.Column(db.Enum(segment))
    exchange = db.Column(db.Enum(exchange))
    listed_at = db.Column(db.DateTime)
    expiry_date = db.Column(db.Date)
    
class Index(db.Model):
    __tablename__ = "index"
    trading_symbol = db.Column(db.String(255), db.ForeignKey('instrument.trading_symbol'), primary_key=True)
    tick_size = db.Column(db.Float, default=0.05)
    exchange = db.Column(db.Enum(exchange))

class Stocks_minute(db.Model):
    __tablename__ = "stocks_minute"
    trading_symbol = db.Column(db.String(255), db.ForeignKey('instrument.trading_symbol'), primary_key=True)
    datetime = db.Column(db.DateTime, primary_key=True)
    open = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    close = db.Column(db.Float)
    volume = db.Column(db.Integer)
    
class Options_minute(db.Model):
    __tablename__ = "options_minute"
    trading_symbol = db.Column(db.String(255), db.ForeignKey('instrument.trading_symbol'), primary_key=True)
    datetime = db.Column(db.DateTime, primary_key=True)
    open = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    close = db.Column(db.Float)
    volume = db.Column(db.Integer)
    open_interest = db.Column(db.Integer)

class Futures_minute(db.Model):
    __tablename__ = "futures_minute"
    trading_symbol = db.Column(db.String(255), db.ForeignKey('instrument.trading_symbol'), primary_key=True)
    datetime = db.Column(db.DateTime, primary_key=True)
    open = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    close = db.Column(db.Float)
    volume = db.Column(db.Integer)
    open_interest = db.Column(db.Integer)

class Index_minute(db.Model):
    __tablename__ = "index_minute"
    trading_symbol = db.Column(db.String(255), db.ForeignKey('instrument.trading_symbol'), primary_key=True)
    datetime = db.Column(db.DateTime, primary_key=True)
    open = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    close = db.Column(db.Float)
    
class Stocks_bhav(db.Model):
    __tablename__ = "stocks_bhav"
    trading_symbol = db.Column(db.String(255), db.ForeignKey('instrument.trading_symbol'), primary_key=True)
    open = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    close = db.Column(db.Float)
    last = db.Column(db.Float)
    prev_close = db.Column(db.Float)
    total_trade_qty = db.Column(db.BigInteger)
    total_trade_val = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, primary_key=True)
    total_trades = db.Column(db.Integer)
    isin = db.Column(db.String(255))
    
class Futures_opt_bhav(db.Model):
    __tablename__ = "futures_opt_bhav"
    trading_symbol = db.Column(db.String(255), db.ForeignKey('instrument.trading_symbol'), primary_key=True)
    expiry_date = db.Column(db.Date)
    strike_pr = db.Column(db.Float)
    option_typ = db.Column(db.Enum(option_type))
    open = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    close = db.Column(db.Float)
    settle_pr = db.Column(db.Float)
    contracts = db.Column(db.Float)
    val_inlakh = db.Column(db.Float)
    open_int = db.Column(db.Integer)
    chg_in_oi = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, primary_key=True)
    