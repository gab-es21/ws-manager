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

def close_registration_popup(driver):
    """Close the registration pop-up if it appears."""
    try:
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'register-popup-close-cross'))
        )
        random_sleep()
        close_button.click()
        logging.info("Registration pop-up closed successfully.")
    except (NoSuchElementException, TimeoutException):
        logging.info("Registration pop-up not found or timed out.")
    except Exception as e:
        logging.error("Error closing registration pop-up: " + str(e))

def perform_search(driver, search_query):
    """Perform a search for the given query on Zumub website."""
    random_sleep()
    try:
        # Locate the search input using its class name
        search_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'search-form'))
        )
        random_sleep()
        search_input = search_box.find_element(By.CLASS_NAME, 'txt_searchbox')
        search_input.click()
        random_sleep()
        search_input.clear()
        search_input.send_keys(search_query)
        search_input.send_keys(Keys.RETURN)
        logging.info(f"Search performed successfully for query: {search_query}")
    except Exception as e:
        logging.error("Search Error: " + str(e))

def extract_item_links(driver):
    """Extract item links from the search results on Zumub."""
    random_sleep()
    links = []
    logging.info("Starting link extraction")

    try:
        # Locate the product listing container
        product_listing = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'list-product-75'))
        )

        # Find all product items within the listing
        items = product_listing.find_elements(By.CSS_SELECTOR, '.product-detail')

        logging.info(f"Found {len(items)} items on the page.")

        for item in items:
            try:
                # Find the link element within the product item
                link_element = item.find_element(By.CSS_SELECTOR, '.product-detail a')
                href = link_element.get_attribute('href')
                product_id = href.split("/")[-1]  # Extract the unique part of the link
                
                links.append({"id": product_id, "link": href})

                # Improved logging for each product
                product_name = item.find_element(By.CSS_SELECTOR, '.product-detail p').text  # Extracting product name
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


def search_zumub(driver, brand_website, product_type):
    """Function to search for a product type on Zumub website."""
    logging.info(f"Starting search on {brand_website} for product type: {product_type}")
    driver.get(brand_website)
    random_sleep()  # Let the page load
    accept_cookies(driver)  # Accept cookies if necessary
    time.sleep(10)
    close_registration_popup(driver)  # Close the registration pop-up if it appears
    random_sleep()
    perform_search(driver, product_type)  # Perform the search
    product_links = extract_item_links(driver)  # Extract product links
    logging.info(f"Search completed for product type: {product_type} on {brand_website}")
    return product_links
