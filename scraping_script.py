import requests
from bs4 import BeautifulSoup
import pandas as pd

def main():
    # Step 1: Send a request to the website
    url = 'http://books.toscrape.com/'
    response = requests.get(url)
    response.raise_for_status()  # Check that the request was successful

    # Step 2: Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Step 3: Extract data
    books = soup.find_all('article', class_='product_pod')
    titles = [book.h3.a['title'] for book in books]
    prices = [book.find('p', class_='price_color').text for book in books]

    # Step 4: Create a pandas DataFrame
    data = {'Title': titles, 'Price': prices}
    df = pd.DataFrame(data)

    # Step 5: Export the data to CSV
    df.to_csv('books.csv', index=False)

    print('Data has been successfully scraped and saved to books.csv')

if __name__ == '__main__':
    main()
