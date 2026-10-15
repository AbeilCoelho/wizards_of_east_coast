import os
import time
import requests

# --- Configuration ---
QUERY = "set:fra"
API_URL = f"https://api.scryfall.com/cards/search?q={QUERY}"
DOWNLOAD_DIR = r"C:\Users\abeil\Downloads\card_images"

# Create the download directory if it doesn't exist
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# --- Browser Headers ---
# This mimics a Google Chrome GET request so the image server doesn't block us
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}

def download_cards():
    current_page_url = API_URL

    while current_page_url:
        print(f"\nFetching API: {current_page_url}")
        
        # 1. Fetch the JSON data from the API
        response = requests.get(current_page_url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Failed to fetch API. Status Code: {response.status_code}")
            break
            
        data = response.json()
        cards = data.get("data", [])
        
        # 2. Iterate through all cards on this page
        for card in cards:
            oracle_id = card.get("oracle_id")
            card_name = card.get("name", "Unknown Card")
            
            # Scryfall edge-case: Double-faced cards store their images inside "card_faces"
            if "image_uris" in card:
                img_url = card["image_uris"].get("normal")
            elif "card_faces" in card and "image_uris" in card["card_faces"][0]:
                img_url = card["card_faces"][0]["image_uris"].get("normal")
            else:
                img_url = None
                
            if not oracle_id or not img_url:
                print(f"Skipping '{card_name}' - Missing oracle_id or image_uri.")
                continue
                
            filepath = os.path.join(DOWNLOAD_DIR, f"{oracle_id}.jpg")
            
            # Skip if we already downloaded this card previously
            if os.path.exists(filepath):
                print(f"Already downloaded: {card_name} ({oracle_id}.jpg)")
                continue
                
            # 3. Download the image
            print(f"Downloading: {card_name} -> {oracle_id}.jpg")
            img_response = requests.get(img_url, headers=HEADERS)
            
            if img_response.status_code == 200:
                with open(filepath, 'wb') as file:
                    file.write(img_response.content)
            else:
                print(f"Failed to download image for '{card_name}'. Status Code: {img_response.status_code}")
            
            # 4. Mandatory 2-second wait between requests (Image downloads)
            time.sleep(2)
            
        # 5. Check if there is another page of cards to process
        if data.get("has_more") and data.get("next_page"):
            current_page_url = data.get("next_page")
            # Mandatory 2-second wait before hitting the next API page
            time.sleep(2) 
        else:
            current_page_url = None # This will break the loop

    print("\nFinished downloading all card images!")

if __name__ == "__main__":
    download_cards()