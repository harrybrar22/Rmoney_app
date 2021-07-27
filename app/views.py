from app import app
from app.get_data import get_stock_bhavcopy
from app.get_data import get_fut_opt_bhavcopy

@app.route('/')
def hello_world():
    return "Hello"

@app.route('/api/v1/bhav_copy/equity/<start_date>/<end_date>')
def bhav_equity(start_date, end_date):
    get_stock_bhavcopy(start_date, end_date)
    return "Data is inserted"

@app.route('/api/v1/bhav_copy/fut_opt/<start_date>/<end_date>')
def bhav_fut_opt(start_date, end_date):
    get_fut_opt_bhavcopy(start_date, end_date)
    return "Data is inserted"

@app.route('/api/v1/check_integrity')
def check_intregrity():
    return "integrity checked"