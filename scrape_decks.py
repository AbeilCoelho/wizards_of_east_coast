import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- Configuration ---
MAIN_URL = "http://mtgo.com/decklists/2026/10?filter=Standard"
DOWNLOAD_DIR = r"C:\Users\abeil\Downloads\decks"

# Create the download directory if it doesn't exist
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# --- Chrome Setup ---
chrome_options = webdriver.ChromeOptions()
# Set Chrome preferences to download files automatically to your specified folder
prefs = {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)

# Initialize the Chrome driver
print("Starting Chrome...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
wait = WebDriverWait(driver, 10)

try:
    # 1. Go to the main page
    print(f"Loading main page: {MAIN_URL}")
    driver.get(MAIN_URL)

    # 2. Wait for the tournament links to load and extract their URLs
    # We extract URLs instead of clicking them directly so we can easily loop through them 
    # without breaking the page navigation.
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "decklists-link")))
    tournament_elements = driver.find_elements(By.CLASS_NAME, "decklists-link")
    
    tournament_urls = [elem.get_attribute("href") for elem in tournament_elements]
    print(f"Found {len(tournament_urls)} tournaments.")

    # 3. Loop through every tournament URL
    for url in tournament_urls:
        print(f"\nNavigating to tournament: {url}")
        driver.get(url)

        try:
            # Wait until at least one download button is present
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.decklist-download")))
            
            # Find all download buttons on the page
            download_buttons = driver.find_elements(By.CSS_SELECTOR, "button.decklist-download")
            print(f"Found {len(download_buttons)} decks in this tournament. Downloading...")

            # 4. Click each download button
            for index, button in enumerate(download_buttons):
                # Scroll the button into view just in case
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                time.sleep(0.2) # tiny pause after scrolling
                
                # We use JavaScript to click to bypass any potential sticky headers/cookie banners
                driver.execute_script("arguments[0].click();", button)
                
                # Brief pause to ensure the browser registers the download trigger before moving to the next
                time.sleep(0.5) 
                
            print("Finished downloading decks for this tournament.")
            
        except Exception as e:
            print(f"Could not find download buttons for {url} or an error occurred.")

    # Wait a few seconds at the very end to ensure the last files finish downloading 
    # before the browser closes.
    print("\nAll tasks complete. Waiting 5 seconds for final downloads to finish...")
    time.sleep(5)

finally:
    print("Closing browser.")
    driver.quit()