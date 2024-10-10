import yfinance as yf

def filter_delisted_companies(stock_list):
    listed_companies = []
    delisted_companies = []
    
    for ticker in stock_list:
        try:
            ticker_input = ticker + ".NS"
            stock = yf.Ticker(ticker_input)
            hist = stock.history(period="1d")  # Fetch latest data
            
            if hist.empty:
                delisted_companies.append(ticker)
            else:
                listed_companies.append(ticker)
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
    
    return listed_companies, delisted_companies

# Stock list with possible delisted companies
nse_stocks = [
    'TCS', 'INFY', 'RELIANCE', 'HDFCBANK', 'ICICIBANK', 'SBIN', 'HINDUNILVR',
    'TITAN', 'LT', 'AXISBANK', 'KOTAKBANK', 'MARUTI', 'BHARTIARTL',
    'ADANIGREEN', 'BAJFINANCE', 'WIPRO', 'TATAMOTORS', 'SUNPHARMA', 'ONGC',
    'HCLTECH', 'ULTRACEMCO', 'POWERGRID', 'ITC', 'JSWSTEEL', 'CIPLA', 'NTPC',
    'INDUSINDBK', 'TECHM', 'GRASIM', 'SHREECEM', 'TATASTEEL', 'HDFCLIFE',
    'LTI', 'TATACONSUMER', 'DIVISLAB', 'DABUR', 'HINDALCO', 'NMDC', 'MINDTREE',
    'PIIND', 'ABB', 'BOSCHLTD', 'HAVELLS', 'JSWENERGY', 'MRF', 'INDIAMART',
    'SYNGENE', 'ADANIPORTS', 'AMBUJACEM', 'BERGEPAINT', 'COLPAL', 'RECLTD',
    'MGL', 'COALINDIA', 'KNRCON', 'LUXIND', 'NATIONALUM', 'PFC', 'SBILIFE',
    'TATAELXSI', 'VOLTAS', 'HINDPETRO', 'TATAMETALI', 'BHEL', 'LUPIN', 'HDFC'
]

# Run the filter
listed_companies, delisted_companies = filter_delisted_companies(nse_stocks)

print("Listed companies:", listed_companies)
print("Possibly delisted companies:", delisted_companies)
