# DittoAi
## Overview
This repository contains a Python-based data retrieval application that interacts with a public REST API (PokeAPI) to extract, parse, and format complex statistical data. 

While the dataset utilizes gaming statistics, the core purpose of this project was to build hands-on experience with fundamental IT and software engineering concepts. It demonstrates the ability to programmatically query external web services, handle JSON payloads, and sanitize data for end-user readability—skills directly applicable to querying threat intelligence feeds, managing IT automation scripts, or handling structured database records.

## Key Features
* **REST API Integration:** Sends automated HTTP GET requests to fetch live data from an external server.
* **JSON Parsing:** Unpacks and navigates deeply nested JSON dictionaries to extract specific target variables (e.g., stats, attributes).
* **Data Formatting:** Converts raw, machine-readable text into a clean, human-readable terminal output.
* **Error Handling:** Implements exception handling to gracefully manage invalid user inputs or failed web requests without crashing the application.

## Technologies Used
* **Language:** Python 3
* **Libraries:** `requests` (for HTTP routing), `json` (for data parsing)
* **Architecture:** Procedural scripting and API integration

## How to Run Locally
1. Ensure Python 3.x is installed on your machine.
2. Clone this repository to your local environment.
3. Install the required requests library by running: `pip install requests`
4. Execute the script from your terminal: `python main.py` (replace 'main.py' with your actual file name)
5. Follow the on-screen prompts to query specific entity statistics.
