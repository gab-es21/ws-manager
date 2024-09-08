import os
import time
import logging
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

# Import brand-specific search functions
from brand_modules.prozis import search_prozis
from brand_modules.myprotein import search_myprotein
from brand_modules.zumub import search_zumub

# Setup logging
logging.basicConfig(filename='search_log.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

# Get paths from environment variables
FIREBASE_CREDENTIALS_PATH = os.getenv('FIREBASE_CREDENTIALS_PATH')

# Initialize Firebase Admin SDK
cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

def init_webdriver(browser='chrome', width=1920, height=1080, headless=False):
    """Initialize WebDriver with the option to set resolution and headless mode."""
    if browser == 'chrome':
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--incognito")  # Open Chrome in incognito mode
        options.add_argument(f"--window-size={width},{height}")  # Set screen resolution

        if headless:
            options.add_argument("--headless")  # Open Chrome in headless mode

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    else:
        raise ValueError("Unsupported browser. Use 'chrome'.")

    return driver

# Dictionary mapping brand ID to corresponding search function
search_functions = {
    "Prozis": search_prozis,
    "MyProtein": search_myprotein,
    "Zumub": search_zumub,
}

# Function to save or update product links in Firestore
def save_or_update_product_links_to_firestore(brand_name, product_links):
    """Saves or updates product links in Firestore under a new collection with today's date and brand name."""
    today = datetime.now().strftime('%Y-%m-%d')
    collection_name = f"product_links/{today}/{brand_name}"
    
    for product in product_links:
        product_id = product["id"]
        product_link = product["link"]
        
        # Check if the product document already exists
        product_doc = db.collection(collection_name).document(product_id).get()

        if product_doc.exists:
            # Check if the existing link is different from the current one
            existing_link = product_doc.to_dict().get('link')
            if existing_link != product_link:
                # Update the product link if it's different
                db.collection(collection_name).document(product_id).update({
                    "link": product_link
                })
                logging.info(f"Updated product link for ID {product_id}: {product_link}")
                print(f"Updated product link for ID {product_id}: {product_link}")
            else:
                logging.info(f"Product {product_id} already exists with the same link. No update needed.")
                print(f"Product {product_id} already exists with the same link. No update needed.")
        else:
            # Add new product if it doesn't exist
            db.collection(collection_name).document(product_id).set({
                "link": product_link
            })
            logging.info(f"Added new product link to Firestore: {product_link} with ID: {product_id}")
            print(f"Added new product link to Firestore: {product_link} with ID: {product_id}")

# Main function to loop through all brands and product types
def main():
    # Initialize WebDriver
    driver = init_webdriver(browser='chrome')

    try:
        # Fetch brand links from Firestore
        brands_ref = db.collection('brands')
        brands = [doc.to_dict() for doc in brands_ref.stream()]

        # Fetch product types from Firestore
        product_types_ref = db.collection('product_types')
        product_types = [doc.to_dict()['label'] for doc in product_types_ref.stream()]

        for brand in brands:
            brand_name = brand['name']
            brand_website = brand['website']
            logging.info(f"Searching on {brand_name} website ({brand_website})...")
            print(f"Starting search on {brand_name} website ({brand_website})...")

            # Get the corresponding search function for the brand
            search_function = search_functions.get(brand_name)

            if search_function:
                for product_type in product_types:
                    try:
                        logging.info(f"Searching for {product_type} on {brand_name}...")
                        print(f"Searching for {product_type} on {brand_name}...")
                        
                        product_links = search_function(driver, brand_website, product_type)
                        
                        # Save or update the product links in Firestore
                        save_or_update_product_links_to_firestore(brand_name, product_links)
                    
                    except Exception as e:
                        logging.error(f"Error searching for {product_type} on {brand_name}: {e}")
                        print(f"Error searching for {product_type} on {brand_name}: {e}")
                        continue  # Continue to the next product type
                
            else:
                logging.warning(f"No search function defined for brand: {brand_name}")
                print(f"No search function defined for brand: {brand_name}")

    except Exception as e:
        logging.critical(f"Critical error in main process: {e}")
        print(f"Critical error in main process: {e}")
    finally:
        driver.quit()
        logging.info("WebDriver closed.")
        print("WebDriver closed.")

if __name__ == "__main__":
    main()
