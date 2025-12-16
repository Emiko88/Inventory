# Inventory
A high-performance web-based search engine for inventory management. Built with Litestar for the backend API and Pandas for efficient data processing. The application reads from an Excel database and provides ranked search results using a custom relevance scoring algorithm.

🛠️ Tech Stack:
* Language: Python 3.8+
* Web Framework: Litestar
* Data Processing: Pandas
* Template Engine: Jinja2
* Server: Uvicorn

⚙️ Installation:
1. Clone repository:
 ```bash
git clone https://github.com/Emiko88/Inventory.git
cd Inventory 
```
2. Install dependencies:
 ```python
pip install litestar uvicorn pandas openpyxl jinja2
```
3. Prepare the data file: Ensure you have an "example.xlsx" file in the root directory.

🖥️ Usage:
1. Run the server:
Use uvicorn to start the application (with auto-reload enabled for development).
```bash
uvicorn app:app --reload
```
2. Open the application:
Go to your browser and navigate to:
```bash
http://127.0.0.1:8000
```
3. Search
Enter a keyword (e.g., material ID, description, or part number) into the search bar.
