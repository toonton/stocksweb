import yfinance as yf
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
def set_url_stock(user_input):
    try:
        url = 'https://finance.yahoo.com/quote/'+ user_input +'/analysis'
        print(url)
        stock = yf.Ticker(user_input)
        dict_info = stock.info
        return url, dict_info
    except:
        print('error in set_url')
def get_Next5Year(url):
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})    
        page = urlopen(req)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        stockstring = soup.get_text()
        first_index = stockstring.find('Next 5 Years (per annum)') + 25
        Next5Year = stockstring[first_index:first_index + 5:1]
        return float(Next5Year)
        
def get_NextYear(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})    
    page = urlopen(req)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    stockstring = soup.get_text()
    first_index = (stockstring.find('% Current Year')) + 15
    NextQtr = stockstring[first_index:first_index + 5:1]
    if NextQtr[4] == '%':
        NextQtr = NextQtr[0:4:1]
        return float(NextQtr)
    else:
        return float(NextQtr)

def get_dividend(dict_info):
    try:
        return float(dict_info['dividendRate'])
    except:
        return 0
def get_eps(dict_info):
    try:
        return float(dict_info['trailingEps'])
    except:
        pass

def calculate_P(Next5Year, dict_info):
    return ((get_eps(dict_info) * (((Next5Year* 0.01)+1)**5)) * (Next5Year*2))

def calculate_F(url, dict_info):
    int1 = 1 + ((18 - get_dividend(dict_info))/100)
    return (calculate_P(url, dict_info) / (int1**5))

def calc_P_1Year(url, dict_info):
    return ((get_eps(dict_info) * (((get_NextYear(url)* 0.01)+1)**3)) * (get_NextYear(url)*2))

#def calc_F_1Year(url, dict_info):
 #   int1 = 1 + ((18 - get_dividend(dict_info))/100)
 #   return (calc_P_1Year(url, dict_info) / (int1**3))

def calulate_F_fairvalue(url, dict_info):
    try:
        if dict_info['marketCap'] > 150000000000:
            return calculate_F(url, dict_info) * 0.7
        elif dict_info['marketCap'] < 50000000000:
            return calculate_F(url, dict_info) * 0.5
        else:
            return calculate_F(url, dict_info) * 0.6
    except:
        pass

def calulate_P_fairvalue(url, dict_info):
    try:
        if dict_info['marketCap'] > 150000000000:
            return calculate_P(url, dict_info) * 0.7
        elif dict_info['marketCap'] < 50000000000:
            return calculate_P(url, dict_info) * 0.5
        else:
            return calculate_P(url, dict_info) * 0.6
    except:
        pass

def calc_ROE():
    pass
def calculate_whentosell(url, dict_info):
    P = ((get_eps(dict_info) * (((get_Next5Year(url)* 0.01)+1)**0.25)) * (get_Next5Year(url)*2))
    


