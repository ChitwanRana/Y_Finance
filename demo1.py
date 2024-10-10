import requests
from bs4 import BeautifulSoup

# URL of the page to scrape
url = "https://en.wikipedia.org/wiki/List_of_companies_listed_on_the_National_Stock_Exchange_of_India"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the page content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all tables with class 'wikitable'
    tables = soup.find_all('table', class_='wikitable')

    # Initialize an empty list to store symbols
    symbols = []

    # Loop through each table and extract symbols
    for table in tables:
        for row in table.find_all('tr')[1:]:  # Skip the header row
            columns = row.find_all('td')
            if len(columns) > 1:  # Ensure there are enough columns
                # Look for the anchor tag with the symbol in the first column
                link = columns[0].find('a')  # Adjusting to the first column for the symbol
                if link and link.text:
                    symbol = link.text.strip()  # Get the text of the symbol
                    symbols.append(symbol)

    # Print the list of symbols
    print(symbols)

    # Optional: print a message if no symbols are found
    if not symbols:
        print("No symbols found.")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
