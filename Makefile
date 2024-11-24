# Define default variables
FLASK_APP=app.py
FLASK_ENV=development
PORT=5000
HOST=0.0.0.0

# Default target: run the Flask app
run:
	FLASK_APP=$(FLASK_APP) FLASK_ENV=$(FLASK_ENV) flask run --host=$(HOST) --port=$(PORT)

# Install dependencies
install:
	pip install -r requirements.txt

# Clean up Python cache
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Help target: display usage
help:
	@echo "Makefile targets:"
	@echo "  run         - Run the Flask app (default target)"
	@echo "  install     - Install dependencies from requirements.txt"
	@echo "  clean       - Remove Python cache files"
	@echo "  help        - Display this help message"

# Set the default target
.DEFAULT_GOAL := run
