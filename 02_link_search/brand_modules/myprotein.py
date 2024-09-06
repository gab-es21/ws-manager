import time
import random
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def random_sleep(min_time=0.1, max_time=0.8):
    """Sleep for a random duration to mimic human behavior."""
    time.sleep(random.uniform(min_time, max_time))

def accept_cookies(driver):
    """Accept cookies on the MyProtein website."""
    try:
        cookies_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))
        )
        random_sleep()
        cookies_button.click()
        logging.info("Cookies accepted successfully.")
    except (NoSuchElementException, TimeoutException):
        logging.warning("Cookies acceptance button not found or timed out.")
    except Exception as e:
        logging.error("Cookies Error: " + str(e))

def close_registration_popup(driver):
    """Close the registration pop-up if it appears."""
    try:
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.emailReengagement_close_button'))
        )
        random_sleep()
        close_button.click()
        logging.info("Registration pop-up closed successfully.")
    except (NoSuchElementException, TimeoutException):
        logging.info("Registration pop-up not found or timed out.")
    except Exception as e:
        logging.error("Error closing registration pop-up: " + str(e))

def open_search(driver):
    """Open the search input field on MyProtein website."""
    try:
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.headerSearch_toggleForm'))
        )
        random_sleep()
        search_button.click()
        logging.info("Search input field opened successfully.")
    except (NoSuchElementException, TimeoutException):
        logging.warning("Search input button not found or timed out.")
    except Exception as e:
        logging.error("Error opening search input: " + str(e))

def perform_search(driver, search_query):
    """Perform a search for the given query on MyProtein website."""
    random_sleep()
    try:
        open_search(driver)  # Open search field before entering text

        # Locate the search input using its NAME attribute
        search_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'search'))  # Use NAME to find the search box
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
        # Locate the product list container
        product_list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.productListProducts_products'))
        )
        
        # Find all product items within the list
        items = product_list.find_elements(By.CSS_SELECTOR, 'li.productListProducts_product')
        logging.info(f"Found {len(items)} items on the page.")
        
        for item in items:
            try:
                # Find the link element within the product item
                link_element = item.find_element(By.CSS_SELECTOR, 'a.productBlock_link')
                href = link_element.get_attribute('href')
                product_id = href.split("/")[-2]  # Extract the unique part of the link
                links.append({"id": product_id, "link": href})
                
                # Improved logging for each product
                product_name = link_element.text.strip() or link_element.get_attribute('aria-label')  # Extracting product name
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

def search_myprotein(driver, brand_website, product_type):
    """Function to search for a product type on MyProtein website."""
    logging.info(f"Starting search on {brand_website} for product type: {product_type}")
    driver.get(brand_website)
    random_sleep()  # Let the page load
    accept_cookies(driver)  # Accept cookies if necessary
    close_registration_popup(driver)  # Close the registration pop-up if it appears
    perform_search(driver, product_type)  # Perform the search
    product_links = extract_item_links(driver)  # Extract product links
    logging.info(f"Search completed for product type: {product_type} on {brand_website}")
    return product_links
