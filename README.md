# Inventory Hub
A high-performance web-based search engine for inventory management. Built with Litestar for the backend API and Pandas for efficient data processing. The application reads from an Excel database and provides ranked search results using a custom relevance scoring algorithm.

## 🛠️ Tech Stack:
* Language: Python 3.8+
* Web Framework: Litestar
* Data Processing: Pandas
* Template Engine: Jinja2
* Dependency Management: Poetry
* Server: Uvicorn

## ⚙️ Installation:
1. Clone repository:
 ```bash
git clone https://github.com/Emiko88/Inventory.git
cd Inventory 
```
2. Install Poetry (if not already installed):
```bash
# On Windows (PowerShell)
# First method:
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
# Second method(if 1st method doesn't work):
pip install poetry

# On macOS/Linux
curl -sSL https://install.python-poetry.org | python3 - 
```
3. Install dependencies:
 ```python
poetry install
```
4. Prepare the data file: Ensure you have an "example.xlsx" file in the root directory.

## 🖥️ Usage:
1. Activate Poetry virtual environment:
 ```bash
poetry shell
```
2. Run the server:
Use uvicorn to start the application (with auto-reload enabled for development).
```bash
# For development with auto-reload
poetry run uvicorn app:app --reload

# Or directly with uvicorn if already in poetry shell
uvicorn app:app --reload
```
3. Open the application:
Go to your browser and navigate to:
```bash
http://127.0.0.1:8000
```
4. Search
Enter a keyword (e.g., material ID, description, or part number) into the search bar.

## 📦 Project Structure:
```text
Inventory/
├── frontend/              
│   ├── index.html              # Main HTML template with search interface
│   └── style.css               # CSS styles for the web interface
├── backend/             
│   ├── app.py                  # Main application file
│   │── logic.py                # Core business logic and search algorithms
│   └── data/
│        └── inventory.xlsx     # Excel database file
├── pyproject.toml              # Poetry configuration and dependencies
├── poetry.lock 
└── README.md
```
