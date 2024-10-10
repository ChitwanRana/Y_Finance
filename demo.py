import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import dateutil.relativedelta as rd

# Function to get stock historical data
def get_stock_data(ticker, start_date, end_date):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)

        if hist.empty:
            raise ValueError("No data available for the given input.")

        # Calculate 5-day moving average
        hist['5-Day MA'] = hist['Close'].rolling(window=5).mean()
        return hist
    except Exception as e:
        print(f"An error occurred while fetching data for {ticker}: {e}")
        return None

# Function to filter stocks based on price range
def filter_stocks_by_price(nse_stocks, price_low, price_high):
    filtered_stocks = []
    for ticker in nse_stocks:
        try:
            ticker_input = ticker + ".NS"  # Append ".NS" to specify the NSE exchange
            stock = yf.Ticker(ticker_input)
            hist = stock.history(period="1d")  # Fetch latest closing price
            
            if not hist.empty:
                latest_close = hist['Close'].iloc[-1]
                if price_low <= latest_close <= price_high:
                    filtered_stocks.append((ticker, latest_close))
        except Exception as e:
            print(f"An error occurred while fetching data for {ticker}: {e}")
    return filtered_stocks

# Main execution
ticker_input = input("Enter the NSE stock ticker (e.g., TCS, INFY): ").upper()
ticker_input += ".NS"  # Append ".NS" to specify the NSE exchange

# Ask user for time frame selection
print("\nSelect time range option:")
print("1. 1 month")
print("2. 2 months")
print("3. 6 months")
print("4. 1 year")
print("5. 2 years")
print("6. 5 years")
print("7. Custom Date Range")
time_choice = input("Enter your choice (1-7): ")

# Calculate start and end date based on user input
end_date = datetime.now()
if time_choice == '1':
    start_date = end_date - rd.relativedelta(months=1)
elif time_choice == '2':
    start_date = end_date - rd.relativedelta(months=2)
elif time_choice == '3':
    start_date = end_date - rd.relativedelta(months=6)
elif time_choice == '4':
    start_date = end_date - rd.relativedelta(years=1)
elif time_choice == '5':
    start_date = end_date - rd.relativedelta(years=2)
elif time_choice == '6':
    start_date = end_date - rd.relativedelta(years=5)
elif time_choice == '7':
    # Custom date input for month and year only
    start_date_input = input("Enter the start month and year (YYYY-MM): ")
    start_date = pd.to_datetime(start_date_input + "-01")

    # Ask for end date or option for "today"
    print("\nSelect end date option:")
    print("1. Today")
    print("2. Custom End Date")
    end_choice = input("Enter your choice (1 or 2): ")

    if end_choice == '1':
        end_date = datetime.now()
    elif end_choice == '2':
        end_date_input = input("Enter the end month and year (YYYY-MM): ")
        end_date = pd.to_datetime(end_date_input + "-01") + rd.relativedelta(months=1) - pd.Timedelta(days=1)
    else:
        print("Invalid option, setting end date to today.")
        end_date = datetime.now()
else:
    print("Invalid option, exiting.")
    exit()

# Get file name to save data
file_name = input("Enter the name of the Excel file to save the data (e.g., 'stock_data.xlsx'): ")

# Ensure the file name ends with .xlsx
if not file_name.endswith('.xlsx'):
    file_name += '.xlsx'

# Fetch historical data for the specified stock
hist = get_stock_data(ticker_input, start_date, end_date)

if hist is not None:
    # Set display options to show all rows and columns
    pd.set_option('display.max_rows', None)  # Display all rows
    pd.set_option('display.max_columns', None)  # Display all columns

    # Print the stock's closing price and 5-day moving average
    print(hist[['Close', '5-Day MA']])

    # Plotting option
    plot_input = input("Do you want to plot the stock price and 5-day moving average? (yes/no): ").lower()

    if plot_input == "yes":
        # Plot the closing price and 5-day moving average on the same graph
        plt.figure(figsize=(10, 5))
        plt.plot(hist.index, hist['Close'], label="Closing Price", color="blue")
        plt.plot(hist.index, hist['5-Day MA'], label="5-Day Moving Average", color="orange")
        plt.title(f"{ticker_input[:-3]} Stock Price and 5-Day Moving Average")  # Remove ".NS" for title
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.xticks(rotation=90)
        plt.legend()
        plt.grid()
        plt.show()  # Ensure this line doesn't interrupt the execution flow

    # Remove timezone from the index to avoid issues with saving to Excel
    hist.index = hist.index.tz_localize(None)

    # Save the data to an Excel file
    hist.to_excel(file_name)
    print(f"Stock data with 5-Day Moving Average has been exported to {file_name}")

    # Read back the Excel file to confirm
    df = pd.read_excel(file_name)
    print(df)

# Load NSE stock tickers (for example purpose, using a hardcoded list)
nse_stocks = [
    'TCS',          # Tata Consultancy Services
    'INFY',         # Infosys
    'RELIANCE',     # Reliance Industries
    'HDFCBANK',     # HDFC Bank
    'ICICIBANK',    # ICICI Bank
    'SBIN',         # State Bank of India
    'HINDUNILVR',   # Hindustan Unilever
    'TITAN',        # Titan Company
    'LT',           # Larsen & Toubro
    'AXISBANK',     # Axis Bank
    'KOTAKBANK',    # Kotak Mahindra Bank
    'MARUTI',       # Maruti Suzuki
    'BHARTIARTL',   # Bharti Airtel
    'ADANIGREEN',   # Adani Green Energy
    'BAJFINANCE',   # Bajaj Finance
    'WIPRO',        # Wipro
    'TATAMOTORS',   # Tata Motors
    'SUNPHARMA',    # Sun Pharmaceutical Industries
    'ONGC',         # Oil and Natural Gas Corporation
    'HCLTECH',      # HCL Technologies
    'ULTRACEMCO',   # UltraTech Cement
    'POWERGRID',    # Power Grid Corporation of India
    'ITC',          # ITC Limited
    'JSWSTEEL',     # JSW Steel
    'CIPLA',        # Cipla Limited
    'NTPC',         # NTPC Limited
    'INDUSINDBK',   # IndusInd Bank
    'TECHM',        # Tech Mahindra
    'GRASIM',       # Grasim Industries
    'SHREECEM',     # Shree Cement
    'TATASTEEL',    # Tata Steel
    'HDFCLIFE',     # HDFC Life Insurance
    'LTI',          # Larsen & Toubro Infotech
    'TATACONSUMER', # Tata Consumer Products
    'DIVISLAB',     # Divi's Laboratories
    'DABUR',        # Dabur India
    'HINDALCO',     # Hindalco Industries
    'NMDC',         # NMDC Limited
    'MINDTREE',     # Mindtree
    'PIIND',        # PI Industries
    'ABB',          # ABB India
    'BOSCHLTD',     # Bosch Limited
    'HAVELLS',      # Havells India
    'JSWENERGY',    # JSW Energy
    'MRF',          # MRF Limited
    'INDIAMART',    # IndiaMART InterMESH
    'SYNGENE',      # Syngene International
    'ADANIPORTS',   # Adani Ports and SEZ
    'AMBUJACEM',    # Ambuja Cements
    'BERGEPAINT',   # Berger Paints India
    'COLPAL',       # Colgate-Palmolive (India)
    'RECLTD',       # Rural Electrification Corporation
    'MGL',          # Mahanagar Gas
    'COALINDIA',    # Coal India Limited
    'KNRCON',       # KNR Constructions
    'LUXIND',       # Lux Industries
    'NATIONALUM',   # National Aluminium Company
    'PFC',          # Power Finance Corporation
    'SBI LIFE',     # SBI Life Insurance
    'TATAELXSI',    # Tata Elxsi
    'VOLTAS',       # Voltas Limited
     'LTI'
    # Example BSE Stocks
    'HINDPETRO',    # Hindustan Petroleum Corporation
    'TATAMETALI',   # Tata Metaliks
    'BHEL',         # Bharat Heavy Electricals Limited
    'LUPIN',        # Lupin Limited
    'HDFC',         # HDFC Limited
]


# Ask user for the price range
price_low = float(input("Enter the lower price range: "))
price_high = float(input("Enter the upper price range: "))

# Filter stocks by the specified price range
filtered_stocks = filter_stocks_by_price(nse_stocks, price_low, price_high)

# Print the filtered stocks
if filtered_stocks:
    print("\nStocks within the specified price range:")
    for stock in filtered_stocks:
        print(f"Ticker: {stock[0]}, Closing Price: {stock[1]:.2f}")
else:
    print("No stocks found within the specified price range.")
