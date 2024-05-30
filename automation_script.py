import requests
from bs4 import BeautifulSoup
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def fetch_data(url):
    """Fetch data from the specified URL and return a BeautifulSoup object."""
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def extract_available_features(soup):
    """Extract available features from the BeautifulSoup object."""
    available_features = []
    articles = soup.find_all('article', class_='product_pod')
    if articles:
        first_article = articles[0]
        available_features = [tag.name for tag in first_article.find_all(recursive=False)]
    return available_features

def process_data(soup, features):
    """Process the BeautifulSoup object to extract specified features and return a pandas DataFrame."""
    # Define a mapping of feature names to BeautifulSoup selectors
    feature_selectors = {
        'title': ('article.product_pod h3 a', 'title'),
        'price': ('article.product_pod p.price_color', 'text'),
        'availability': ('article.product_pod p.availability', 'text')
    }
    
    # Validate requested features
    invalid_features = [feature for feature in features if feature not in feature_selectors]
    if invalid_features:
        raise ValueError(f"Invalid features requested: {', '.join(invalid_features)}. Valid features are: {', '.join(feature_selectors.keys())}")
    
    if len(features) < 3:
        raise ValueError("You must request at least 3 features.")
    
    data = {feature: [] for feature in features}
    
    for feature in features:
        selector, attr = feature_selectors[feature]
        elements = soup.select(selector)
        
        if attr == 'text':
            data[feature] = [element.get_text(strip=True) for element in elements]
        else:
            data[feature] = [element[attr] for element in elements]
    
    # Create a DataFrame
    df = pd.DataFrame(data)
    
    # Additional cleaning for price if it is one of the requested features
    if 'price' in features:
        df['price'] = df['price'].apply(lambda x: ''.join([char for char in x if char.isdigit() or char == '.']))
        df['price'] = df['price'].astype(float)
    
    return df

def generate_reports(df):
    """Generate reports in CSV, Excel, and PDF formats from the DataFrame."""
    # CSV and Excel reports
    df.to_csv('extracted_data.csv', index=False)
    df.to_excel('extracted_data.xlsx', index=False)
    
    # PDF report
    c = canvas.Canvas('extracted_data.pdf', pagesize=letter)
    text = df.to_string(index=False)
    c.drawString(100, 750, text)
    c.save()
    
    print('Reports have been successfully generated: extracted_data.csv, extracted_data.xlsx, and extracted_data.pdf')

def main():
    url = input("Enter the URL to scrape: ").strip() #http://books.toscrape.com/

    soup = fetch_data(url)
    available_features = extract_available_features(soup)
    
    print("Available features on the website:")
    for feature in available_features:
        print(feature)
    
    features_input = input("Enter the features to extract (comma-separated, choose from the available features): ").strip().split(',')
    features = [feature.strip() for feature in features_input]

    # Validate and process user-selected features
    try:
        df = process_data(soup, features)
        generate_reports(df)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
