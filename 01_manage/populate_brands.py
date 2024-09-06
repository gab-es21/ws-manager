import json
import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get paths from environment variables
FIREBASE_CREDENTIALS_PATH = os.getenv('FIREBASE_CREDENTIALS_PATH')
BRANDS_JSON_PATH = os.getenv('BRANDS_JSON_PATH')

# Initialize Firebase Admin SDK
cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)  # Use the path from the .env file
firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

def read_json_and_insert_to_firestore(json_file):
    """
    Reads the JSON file and inserts or updates data in the 'brands' collection in Firestore.
    """
    try:
        # Read the JSON file
        with open(json_file, 'r') as f:
            brands = json.load(f)
        
        # Reference to the 'brands' collection
        brands_ref = db.collection('brands')

        # Process each brand in the JSON file
        for brand in brands:
            brand_id = brand.get('id')
            if brand_id:
                # Reference to the specific document
                doc_ref = brands_ref.document(brand_id)
                doc = doc_ref.get()
                
                if doc.exists:
                    # Document exists, check for differences
                    existing_data = doc.to_dict()
                    if existing_data['name'] != brand['name'] or existing_data['website'] != brand['website']:
                        # Update the document if there are differences
                        doc_ref.update({
                            'name': brand['name'],
                            'website': brand['website']
                        })
                        print(f"Updated brand: {brand_id}")
                    else:
                        print(f"Brand already exists with the same data: {brand_id}")
                else:
                    # Document does not exist, add a new one
                    doc_ref.set({
                        'name': brand['name'],
                        'website': brand['website']
                    })
                    print(f"Inserted new brand: {brand_id}")

            else:
                print("Skipping entry without 'id':", brand)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    read_json_and_insert_to_firestore(BRANDS_JSON_PATH)
