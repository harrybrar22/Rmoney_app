import os
import click

from click.types import STRING
from flask.cli import with_appcontext
from app import app
from datetime import datetime
import pandas as pd


@click.command(name = 'check')
@click.argument("start_date", type=STRING)
@click.argument("end_date", type=STRING)
@with_appcontext
def check_integrity(start_date, end_date):
    try:
        start_date_arg = datetime.strptime(start_date, '%d/%m/%Y')
        end_date_arg = datetime.strptime(start_date, '%d/%m/%Y')
        click.echo('Hello World!')
    except:
        print(dir(click))
        print("check format")
        # click.echo("check date fromat")
    file_path = os.getcwd()+"/CSV_files"
    file_list = os.listdir(file_path)
    for file in file_list:
        date = file.split(".")[0][-8:]
        file_date = datetime.strptime(date, '%d%m%Y')
        # if date_arg == file_date:
        #     df = pd.read_csv(file_path+"/"+file)
        #     print(df)
            
        
app.cli.add_command(check_integrity)

