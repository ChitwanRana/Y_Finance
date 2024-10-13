import yfinance as yf
import concurrent.futures

# Function to get the latest close price of a stock
def get_latest_close_price(ticker):
    try:
        stock = yf.Ticker(ticker + ".NS")
        hist = stock.history(period="1d")
        
        # Check if data is available
        if not hist.empty:
            latest_close_price = hist['Close'].iloc[-1]
            return ticker, latest_close_price
        else:
            print(f"No trading data found for {ticker}")
            return ticker, None
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return ticker, None

# Function to filter stocks based on a price range using concurrent futures for parallel fetching
def filter_stocks_by_price_concurrent(nse_stocks, price_low, price_high):
    filtered_stocks = []
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_latest_close_price, ticker) for ticker in nse_stocks]
        
        for future in concurrent.futures.as_completed(futures):
            ticker, latest_close = future.result()
            
            # Filter the stocks by price range
            if latest_close is not None and price_low <= latest_close <= price_high:
                filtered_stocks.append((ticker, latest_close))
    
    return filtered_stocks

# Example usage
if __name__ == "__main__":
    nse_stocks = ['RELIANCE', 'TCS', 'INFY', 'HDFCBANK']  # List of NSE stock tickers
    price_low = 1000  # Lower bound for price filtering
    price_high = 4000  # Upper bound for price filtering

    # Fetching filtered stocks based on the price range
    filtered_stocks = filter_stocks_by_price_concurrent(nse_stocks, price_low, price_high)
    
    # Display the filtered stocks
    for ticker, price in filtered_stocks:
        print(f"{ticker}: {price}")
