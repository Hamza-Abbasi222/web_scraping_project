from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_valid_url():
    """Prompt the user for a valid website URL."""
    while True:
        url = input("Enter the URL of the website you want to interact with: ").strip()
        if url.startswith(("http://", "https://")):
            return url
        else:
            print("Invalid URL. Please enter a URL starting with 'http://' or 'https://'.")

def main():
    # Get the website URL from the user
    website_url = get_valid_url()

    # Set up WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # Open the webpage
        driver.get(website_url)

        # Find an element by ID and click it
        example_button = driver.find_element(By.ID, "exampleButtonId")
        example_button.click()
        print("Clicked the example button.")

        # Wait for a few seconds
        time.sleep(2)

        # Find an input field by name and type into it
        example_input = driver.find_element(By.NAME, "exampleInputName")
        example_input.send_keys("Sample Text")
        example_input.send_keys(Keys.RETURN)
        print("Typed into the example input field.")

        # Wait for a few seconds
        time.sleep(2)

        # Find an element by class name and click it
        example_link = driver.find_element(By.CLASS_NAME, "exampleLinkClass")
        example_link.click()
        print("Clicked the example link.")

        # Wait for a few seconds
        time.sleep(2)

    finally:
        # Close the WebDriver
        driver.quit()

if __name__ == "__main__":
    main()


'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    # Open a webpage
    driver.get("https://example.com")

    # Print the title of the page
    print("Page title:", driver.title)

    # Find an element by ID and interact with it (e.g., click a button)
    example_button = driver.find_element(By.ID, "exampleButtonId")
    example_button.click()
    
    # Wait for a few seconds to observe the interaction
    time.sleep(2)

    # Find an input field by name and type into it
    example_input = driver.find_element(By.NAME, "exampleInputName")
    example_input.send_keys("Sample Text")
    example_input.send_keys(Keys.RETURN)
    
    # Wait for a few seconds to observe the interaction
    time.sleep(2)

    # Navigate to another page
    driver.get("https://example.com/anotherpage")
    print("Page title after navigation:", driver.title)
    
    # Interact with another element
    another_button = driver.find_element(By.CSS_SELECTOR, "button.anotherButtonClass")
    another_button.click()

    # Wait for a few seconds to observe the interaction
    time.sleep(2)

finally:
    # Close the WebDriver
    driver.quit()
'''
