# ws-manager

This project is a Django-based web application for managing brands and their information, integrated with Firebase Firestore for data storage and Selenium for web scraping.

- [ws-manager](#ws-manager)
    - [Project Structure](#project-structure)
    - [Activating Virtual Environment](#activating-virtual-environment)
    - [Creating requirements.txt](#creating-requirementstxt)
    - [Populating the Database](#populating-the-database)
    - [Automating Link Searches](#automating-link-searches)
    - [Installing Dependencies from requirements.txt](#installing-dependencies-from-requirementstxt)

### Project Structure

The project is divided into multiple folders for specific functionalities, each serving a unique role in the application workflow:

- **01_manage**: Contains scripts for setting up the initial database with brands and product types. These scripts are typically run once during the setup phase or when adding new brands or product types to track. Specifically:
  - **populate_brands.py**: Reads from `config/brands.json` and inserts the brand data (e.g., Prozis, MyProtein, Zumub) into the Firebase Firestore.
  - **populate_product_types.py**: Reads from `config/product_types.json` and adds product categories (e.g., Caseine, Whey, Vegan Protein, Creatine) to the database.

- **02_link_search**: Contains the scripts that automate the process of scraping websites for product links based on the brands and product types specified in the database. These scripts are generally run periodically (weekly, bi-weekly, or occasionally) because product catalogs do not change daily. Key components:
  - **general_link_search.py**: The main script that coordinates the search across different brands, using the `brand_modules` library for brand-specific logic.

- **brand_modules**: This folder contains the individual modules for each brand, encapsulating the specific steps needed to scrape product links from their respective websites. For example:
  - **myprotein.py**: Handles scraping product links from MyProtein.
  - **prozis.py**: Implements the scraping logic for Prozis.
  - **zumub.py**: Contains the logic for extracting links from Zumub.

- **03_get_macros**: A folder dedicated to extracting nutritional information (macros) for products. Like **02_link_search**, this process doesn’t need to run every day. It typically runs on the same schedule as the link search scripts, either weekly or bi-weekly, depending on the frequency of product updates.

- **04_get_prices**: This folder contains scripts that track product prices on a daily basis. Keeping this data updated daily ensures we have the latest price information and can maintain a complete track record of price changes over time.

### Activating Virtual Environment

To activate the virtual environment on Windows, run:

```bash
env-ws-manager\Scripts\activate
```

This command should be run from your project directory where the virtual environment was created. Once activated, you'll see ```(env-ws-manager)``` in your command prompt.

### Creating requirements.txt
To ensure all project dependencies are captured and can be easily installed in other environments, generate a ```requirements.txt``` file. This file lists all the Python packages that your project depends on.

Run the following command to create or update the ```requirements.txt``` file:

```bash
pip freeze > requirements.txt
```

This command captures the current state of your virtual environment's installed packages and their versions, writing them to the ```requirements.txt``` file.

### Populating the Database
The **01_manage** folder contains two key scripts for populating the Firebase Firestore database with brand and product type information:

1. **populate_brands.py** : This script reads from ```config/brands.json```, which contains a sample list of brands (e.g., Prozis, MyProtein, Zumub) and inserts the data into Firestore. It is used to initialize or reset the brands data in the database.

2. **populate_product_types.py** : This script reads from ```config/product_types.json```, which contains a list of product types (e.g., Caseine, Whey, Vegan Protein, Creatine) and populates the database with product categories.

These scripts ensure that the required data structure for brands and product types is properly set up in Firestore.

### Automating Link Searches
The **02_link_search** folder contains the script ```general_link_search.py```, which automates web scraping to search for product links for each brand. It gathers product links for the product types specified in the database. Each brand requires a different scraping strategy, so the brand-specific logic is handled in separate modules within the brand_modules directory.

The brand_modules folder contains:

- **myprotein.py** : Contains the logic and steps needed to extract product links from the MyProtein website.
- **prozis.py** : Contains the scraping logic for Prozis, including steps to handle their search functionality.
- **zumub.py** : Handles Zumub’s search process and product link extraction.
These modules implement the specific steps needed to navigate each website's structure and retrieve the relevant product links.

### Installing Dependencies from requirements.txt
If you or someone else needs to set up the project in a new environment, you can quickly install all the required packages by running:

```bash
pip install -r requirements.txt
```

This command installs all the dependencies listed in ```requirements.txt```, ensuring that the project has all necessary packages to run properly.