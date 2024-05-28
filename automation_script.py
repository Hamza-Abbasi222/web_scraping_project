import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_data(url):
    """Fetch data from the specified URL and return a BeautifulSoup object."""
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def process_data(soup):
    """Process the BeautifulSoup object to extract book data and return a pandas DataFrame."""
    books = soup.find_all('article', class_='product_pod')
    titles = [book.h3.a['title'] for book in books]
    prices = [book.find('p', class_='price_color').text for book in books]
    
    # Create a DataFrame
    data = {'Title': titles, 'Price': prices}
    df = pd.DataFrame(data)
    
    # Clean the data (remove currency symbols and convert prices to float)
    df['Price'] = df['Price'].str.replace('£', '').astype(float)
    return df

def generate_reports(df):
    """Generate reports in CSV and Excel formats from the DataFrame."""
    df.to_csv('books.csv', index=False)
    df.to_excel('books.xlsx', index=False)
    print('Reports have been successfully generated: books.csv and books.xlsx')

def main():
    url = 'http://books.toscrape.com/'
    soup = fetch_data(url)
    df = process_data(soup)
    generate_reports(df)

if __name__ == '__main__':
    main()
