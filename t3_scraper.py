from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import re
from collections import defaultdict

# Import configuration manager
from config_manager import load_config

# Load configuration
config_data = load_config()

# Access configuration constants
TWEET_MAX_CHARS = config_data['TWEET_MAX_CHARS'] # Maximum characters allowed in a tweet
HEADLESS_MODE = config_data['HEADLESS_MODE'] # Set to True to run in headless mode
ENGLISH_ONLY_REGEX = config_data['ENGLISH_ONLY_REGEX'] # Set to True to filter only English topics
SLEEP_TIME_PAGE_LOAD = config_data['SLEEP_TIME_PAGE_LOAD']
SLEEP_TIME_AFTER_COOKIE_CONSENT = config_data['SLEEP_TIME_AFTER_COOKIE_CONSENT']
SLEEP_TIME_AFTER_TAB_CLICK = config_data['SLEEP_TIME_AFTER_TAB_CLICK']

# Set up Chrome options for headless mode
options = Options()
if HEADLESS_MODE:
    options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")  # Disable GPU (helps in some environments)
options.add_argument("--no-sandbox")  # Bypass sandbox for CI environments / Bypass OS security model (use cautiously in CI)
options.add_argument("--window-size=1920,1080")  # Set a window size for rendering
options.add_argument("--disable-dev-shm-usage")  # Address resource limits in containers

# Set up Selenium WebDriver with Service
driver_path = ChromeDriverManager().install()
service = Service(driver_path)

if HEADLESS_MODE:
    driver = webdriver.Chrome(service=service, options=options) # Headless mode
else:
    driver = webdriver.Chrome(service=service) # Headful mode

# Load the page
url = "https://trends24.in/"
driver.get(url)

# Wait for the page to load fully (you might adjust the time)
time.sleep(SLEEP_TIME_PAGE_LOAD)

# Try to click on the cookie consent button if it's present
try:
    # Use the new CSS selector for the button
    cookie_button = driver.find_element(By.CSS_SELECTOR, 'button.css-47sehv span')
    cookie_button.click()
    print("Cookie consent clicked.")
except:
    print("Cookie consent already given or not present.")

# Wait for the page to load after the consent is given
time.sleep(SLEEP_TIME_AFTER_COOKIE_CONSENT)

# Click on the "Table" tab
table_button = driver.find_element(By.ID, 'tab-link-table')
table_button.click()

# Wait for the table to load (adjust the sleep time if necessary)
time.sleep(SLEEP_TIME_AFTER_TAB_CLICK)

# Get the page source after the tab click
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Close the browser window
driver.quit()

# Find the table section
table_section = soup.select_one('section#table .table-container-4 table.the-table tbody.list')

# Extract the trending topics with detailed information
if table_section:
    trending_topics = []  # List to hold extracted information
    rows = table_section.find_all('tr')
    for row in rows:
        rank = row.find('td', class_='rank').text.strip() if row.find('td', class_='rank') else None
        topic_cell = row.find('td', class_='topic')
        topic = topic_cell.find('a', class_='trend-link').text.strip() if topic_cell else None
        position = row.find('td', class_='position').text.strip() if row.find('td', class_='position') else None
        count = row.find('td', class_='count')['data-count'] if row.find('td', class_='count') else None
        duration = row.find('td', class_='duration').text.strip() if row.find('td', class_='duration') else None

        if rank and topic:  # Ensure required fields are present
            trending_topics.append({
                "rank": rank,
                "topic": topic,
                "position": position,
                "count": count,
                "duration": duration,
            })

else:
    print("Trending topics table not found.")

# Print the extracted information
# print("Trending Topics with Details:")
# for topic in trending_topics:
#     print(f"Rank: {topic['rank']}, Topic: {topic['topic']}, Position: {topic['position']}, Count: {topic['count']}, Duration: {topic['duration']}")

# Function to filter English trending topics
def filter_english_trends(trends):
    english_trends = []
    for trend in trends:
        # Access the 'topic' key from each dictionary
        trend_text = trend['topic']
        # Include only topics with alphanumeric, spaces, or hashtags
        if re.match(r'^[a-zA-Z0-9#\s]+$', trend_text):
            english_trends.append(trend)
    return english_trends

# Function to create hashtags within a character limit
def create_hashtags(trends, max_chars=TWEET_MAX_CHARS):
    # Sort trends by their popularity ('count') in descending order
    sorted_trends = sorted(trends, key=lambda x: int(x['count']), reverse=True)
    
    hashtags = []  # List to store hashtags
    total_chars = 0  # Track total character count
    for trend in sorted_trends:
        # Access the 'topic' key from each dictionary
        trend_text = trend['topic']
        # Convert topic to a hashtag (keep letters, numbers, underscores, and Unicode letters)
        # clean_trend = trend_text.lstrip('#') # Remove leading '#' if present
        # hashtag = '#' + clean_trend.replace(' ', '')
        # clean_trend = re.sub(r'[^a-zA-Z0-9_]', '', trend_text.replace(' ', ''))
        clean_trend = re.sub(r'[^\w\u4e00-\u9fff\u0600-\u06ff]+', '', trend_text.replace(' ', ''))
        hashtag = '#' + clean_trend
        hashtag_length = len(hashtag)
        
        # Ensure adding this hashtag stays within the character limit
        if total_chars + hashtag_length <= max_chars:
            hashtags.append(hashtag)
            total_chars += hashtag_length + 1  # Add 1 for the space
        else:
            break  # Stop if the character limit is reached
    
    # Join hashtags with spaces for Twitter compatibility
    return ' '.join(hashtags)  # Return the hashtags as a space-separated string

# Filter English topics
# english_trends = filter_english_trends(trending_topics)
# print(english_trends)
# print([trend['topic'] for trend in english_trends])

# Check if only English trends should be allowed
if ENGLISH_ONLY_REGEX:
    filtered_trends = filter_english_trends(trending_topics)
else:
    filtered_trends = trending_topics  # Use all topics without filtering

# Create hashtags within a character limit from the filtered trending topics
hashtags = create_hashtags(filtered_trends, max_chars=TWEET_MAX_CHARS)
print(hashtags)
