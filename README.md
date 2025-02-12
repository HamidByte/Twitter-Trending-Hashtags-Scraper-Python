# Twitter Trending Topics/Hashtags Scraper

This Python script scrapes the trending topics from the website trends24.in and generates hashtags from the trends. It supports filtering for English-only trends and ensures that the generated hashtags fit within Twitter's character limits.

## Requirements

- Python 3.x
- Selenium
- BeautifulSoup
- WebDriver Manager
- Regular expressions (for filtering)

You can install the required packages using pip:
```bash
pip install selenium beautifulsoup4 webdriver-manager
```

## Usage

1. Run the script:

```bash
python t3_scraper.py
```

2. The script will:

- Open the trends24.in website.
- Accept the cookie consent (if prompted).
- Navigate to the "Table" section to gather trending topics.
- Extract the trending topics along with additional information such as rank, position, count, and duration.
- Optionally filter only English topics (if `ENGLISH_ONLY_REGEX` is set to `True`).
- Create and print hashtags based on the most popular trends while adhering to Twitter's 280-character limit.

## Configuration

- `HEADLESS_MODE`: Set to `True` to run in headless mode (without opening a browser window).
- `ENGLISH_ONLY_REGEX`: Set to `True` to filter for English-only trends based on regex patterns.
- `TWEET_MAX_CHARS`: The character limit for hashtags (default is 280).

## Creating a Standalone Executable

To create a standalone executable from the Python script using PyInstaller:

1. Install PyInstaller:

```bash
pip install pyinstaller
```

2. Navigate to the directory containing your script and run the following command:

```bash
pyinstaller --onefile t3_scraper.py
```

This will generate a standalone executable in the `dist` directory. You can run this executable without needing to install Python or any dependencies on the target machine.

## Executing the Script

On Linux, ensure that the generated executable is set as executable by running:

```bash
chmod +x dist/t3_scraper dist/run_scraper.sh
```

**Running the Script**

You can run the script in two ways:

Option 1: Right-click the `run_scraper.sh` file and select "Run as a Program" to execute it.

Option 2: Using the Terminal

- Open a terminal window.
- Navigate to the directory where the `run_scraper.sh` file is located.
- Run the following command:

```bash
./run_scraper.sh
```

This will execute the scraper by launching the executable.

## Notes

- Ensure you have the Chrome WebDriver installed. You can use the WebDriver Manager to automatically handle this.
- Adjust the sleep times if necessary based on your internet speed or website load time.
