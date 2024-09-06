# Makefile for Firestore population scripts

# Define the Python interpreter and environment activation
VENV_PATH = env-ws-manager\Scripts\activate  # For Windows
PYTHON = .\env-ws-manager\Scripts\python  # Use the Python from the virtual environment

# Default target
.DEFAULT_GOAL := help

# Help command to list all available make commands using Python
.PHONY: help
help:  ## 		Show this help message
	@$(PYTHON) -c "import re; [print('  {0:20} {1}'.format(*re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line).groups())) for line in open('Makefile') if re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)]"

# Environment activation step (not used directly, just a reminder)
.PHONY: env_act
env_act: 
	@echo "Activate virtual environment by running: call $(VENV_PATH)"

# Command to populate brands collection
.PHONY: populate_brands
populate_brands: env_act ## 		Populate the brands collection in Firestore
	@cd 01_manage && python populate_brands.py

# Command to populate product types collection
.PHONY: populate_product_types
populate_product_types:  ## 	Populate the product types collection in Firestore
	@cd 01_manage && python populate_product_types.py

# Command to populate all collections
.PHONY: populate_all
populate_all: populate_brands populate_product_types  ## 		Populate all collections in Firestore
	@echo "All collections have been populated."

.PHONY: link_search
link_search: env_act ## 		Get links for products
	@cd 02_link_search && python general_link_search.py

