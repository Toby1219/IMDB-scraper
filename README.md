**Imports and Dependencies:**

Utilizes libraries like playwright, dataclasses, fake_useragent, and pandas.
Data Class:

**Movies:** Defines the structure for storing movie data including attributes like Movie_Id, Movie_Name, Movie_type, Release_Date, Rating, etc.
BotOne Class:

**Initialization:**
Initializes with parameters for movie date range, movie type, and genre.
Constructs the URL for scraping based on these parameters.

**Methods:**
formart_pram: Formats movie type and genre for URL construction.

parseUrl: Constructs the IMDb search URL.

start_browser: Launches the browser and navigates to the constructed URL.

current_total_item: Retrieves the total number of items listed on the page.

scroll: Scrolls through the page to load more items.

extractor: Extracts data from the specified item using the provided selector.

Parse_html: Parses the HTML content of the page to extract movie details and stores them in the Movies data class.

writer: Writes the extracted data to CSV, Excel, and JSON files.

main: Executes the scraping process by calling the above methods in sequence.

**Execution:**

If the script is run directly, it creates an instance of BotOne with specific parameters and calls the main method to start the scraping process.
