import json
import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get paths from environment variables
FIREBASE_CREDENTIALS_PATH = os.getenv('FIREBASE_CREDENTIALS_PATH')
PRODUCT_TYPES_JSON_PATH = os.getenv('PRODUCT_TYPES_JSON_PATH')

# Initialize Firebase Admin SDK
cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

def insert_or_update_product_types(product_types_file):
    """
    Reads the JSON file and inserts or updates data in the 'product_types' collection in Firestore.
    """
    try:
        # Read the product types JSON file
        with open(product_types_file, 'r') as f:
            product_types = json.load(f)
        
        # Reference to the 'product_types' collection
        product_types_ref = db.collection('product_types')

        for product_type in product_types:
            product_type_id = product_type.get('id')
            if product_type_id:
                # Reference to the specific document
                doc_ref = product_types_ref.document(product_type_id)
                doc = doc_ref.get()
                
                if doc.exists:
                    # Document exists, check for differences
                    existing_data = doc.to_dict()
                    if existing_data != product_type:
                        # Update the document if there are differences
                        doc_ref.set(product_type)  # `set()` will update the whole document
                        print(f"Updated product type: {product_type_id}")
                    else:
                        print(f"Product type already exists with the same data: {product_type_id}")
                else:
                    # Document does not exist, add a new one
                    doc_ref.set(product_type)
                    print(f"Inserted new product type: {product_type_id}")
            else:
                print("Skipping entry without 'id':", product_type)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    insert_or_update_product_types(PRODUCT_TYPES_JSON_PATH)
