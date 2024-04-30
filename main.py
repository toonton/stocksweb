from flask import Flask, render_template, request
import flet as ft
from functions import *
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        stock_value = request.form['stock']
        return process_stock(stock_value)
    return render_template('index.html')

def process_stock(stock_value):
    url, dict_info = set_url_stock(stock_value)
    Next5Year = get_Next5Year(url)
    GreenP = str(round(calculate_P(Next5Year, dict_info), 2))
    GreenF = str(round(calculate_F(Next5Year, dict_info), 2))
    RedP = str(float(GreenP)*0.5)
    RedF = str(float(GreenF)*0.5)
    Greenresult = 'P1: ' + GreenF + '\nP2: ' +  GreenP
    Orangeresult = 'P1: ' + str(round(calulate_F_fairvalue(Next5Year, dict_info),2)) + '\nP2: ' + str(round(calulate_P_fairvalue(Next5Year, dict_info), 2))
    Redresult = 'P1: ' + RedF + '\nP2: ' +  RedP
    return render_template('result.html', Greenresult=Greenresult, Orangeresult=Orangeresult, Redresult=Redresult)

if __name__ == '__main__':
    app.run(debug=True)
