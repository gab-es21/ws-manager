import time
import random
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def random_sleep():
    """Sleep for a random duration to mimic human behavior."""
    time.sleep(random.uniform(0.1, 0.8))

def accept_cookies(driver):
    """Accept cookies on the website."""
    try:
        cookies_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll'))
        )
        random_sleep()
        cookies_button.click()
        logging.info("Cookies accepted successfully.")
    except (NoSuchElementException, TimeoutException):
        logging.warning("Cookies acceptance button not found.")
    except Exception as e:
        logging.error("Cookies Error: " + str(e))

def perform_search(driver, search_query):
    """Perform a search for the given query on Prozis website."""
    random_sleep()
    try:
        # Locate the search input using its ID
        search_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'quick-search_query'))  # Use ID to find the search box
        )
        search_input.clear()
        search_input.send_keys(search_query)
        search_input.send_keys(Keys.RETURN)
        logging.info(f"Search performed successfully for query: {search_query}")
    except Exception as e:
        logging.error("Search Error: " + str(e))

def extract_item_links(driver):
    """Extract item links from the search results."""
    random_sleep()
    links = []
    logging.info("Starting link extraction")
    
    try:
        # Correctly using CSS_SELECTOR to target elements
        items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.col.list-item'))  # Adjusting the selector based on actual class name for product items
        )
        logging.info(f"Found {len(items)} items on the page.")
        
        for item in items:
            try:
                # Adjusted to target the correct <a> tag with the class 'click-layer'
                link_element = item.find_element(By.CSS_SELECTOR, 'a.click-layer')
                href = link_element.get_attribute('href')
                product_id = href.split("/")[-1]  # Extract the unique part of the link
                links.append({"id": product_id, "link": href})
                
                # Improved logging for each product
                product_name = link_element.get_attribute('aria-label')  # Extracting product name from the aria-label attribute
                logging.info(f"Product found: {product_name}, Link: {href}")
                print(f"Detected product: {product_name}, Link: {href}")  # Print each detected product for immediate feedback

            except NoSuchElementException:
                logging.warning("Link element not found in item.")
            except Exception as e:
                logging.error(f"Error processing item: {str(e)}")
                
    except TimeoutException:
        logging.error("Timeout while waiting for items to load.")
    except Exception as e:
        logging.error("Links Error: " + str(e))

    return links

def search_prozis(driver, brand_website, product_type):
    """Function to search for a product type on Prozis website."""
    logging.info(f"Starting search on {brand_website} for product type: {product_type}")
    driver.get(brand_website)
    random_sleep()  # Let the page load
    accept_cookies(driver)  # Accept cookies if necessary
    perform_search(driver, product_type)  # Perform the search
    product_links = extract_item_links(driver)  # Extract product links
    logging.info(f"Search completed for product type: {product_type} on {brand_website}")
    return product_links
