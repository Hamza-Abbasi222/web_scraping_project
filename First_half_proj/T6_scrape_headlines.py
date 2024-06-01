# T6_scrape_headlines.py

import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_valid_url():
    """Prompt the user for a valid website URL."""
    while True:
        url = input("Enter the URL of the website you want to scrape headlines from: ").strip() #https://phonepcr.com/
        if url.startswith(("http://", "https://")):
            return url
        else:
            print("Invalid URL. Please enter a URL starting with 'http://' or 'https://'.")

def get_html_tag_and_class():
    """Prompt the user for the HTML tag and class used for the headlines."""
    tag = input("Enter the HTML tag used for the headlines (e.g., 'h1', 'h2', 'div'): ").strip() #h2
    class_name = input("Enter the class name used for the headlines (leave blank if not applicable): ").strip() #"mt-3"
    return tag, class_name

def scrape_headlines(url, tag, class_name):
    """Scrape headlines from the provided URL using Beautiful Soup."""
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    if class_name:
        headlines = soup.find_all(tag, class_=class_name)
    else:
        headlines = soup.find_all(tag)

    return [headline.get_text(strip=True) for headline in headlines]

def main():
    # Get the website URL from the user
    website_url = get_valid_url()

    # Get the HTML tag and class name for headlines
    tag, class_name = get_html_tag_and_class()

    # Scrape the headlines
    headlines = scrape_headlines(website_url, tag, class_name)

    if headlines:
        # Store the headlines in a Pandas DataFrame
        df = pd.DataFrame(headlines, columns=["Headline"])

        # Export the DataFrame to a CSV file
        df.to_csv("headlines.csv", index=False)
        print("Headlines have been exported to 'headlines.csv'.")
    else:
        print("No headlines found with the provided tag and class.")

if __name__ == "__main__":
    main()
