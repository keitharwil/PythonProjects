import os
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright

# --- Configuration ---
TARGET_URL = 'https://www.studocu.com/ph/document/tarlac-agricultural-university/bs-in-geodetic-engineering/solution-manual-earl-david-rainville-elementary-differential-equations-7th-edition/75951205'
OUTPUT_DIR = 'scraped_images_final_fix'
# ---------------------

def download_image(url, folder):
    """Downloads a file using the simple requests library."""
    try:
        # We need requests for this function
        import requests 
        
        # Simple file naming based on the last part of the URL path
        # Since these URLs are long and unique, they make great filenames
        image_name = os.path.basename(urlparse(url).path)
        if not image_name or len(image_name.split('.')) < 2:
            image_name = f"file_{len(os.listdir(folder)) + 1}.jpg"
            
        # Clean up the name a bit
        image_name = "".join(c for c in image_name if c.isalnum() or c in ('.', '_', '-', '.')).rstrip()
        if len(image_name) > 50: # Truncate long names for safety
             image_name = image_name[:45] + ".jpg"

        image_path = os.path.join(folder, image_name)

        print(f"Attempting to download: {image_name}")

        response = requests.get(url, stream=True, timeout=15) 
        
        if response.status_code == 200:
            with open(image_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"-> Saved to {image_path}")
        else:
            print(f"-> Failed to download. Status code: {response.status_code} for URL: {url}")

    except Exception as e:
        print(f"-> An error occurred while downloading {url}: {e}")

def scrape_images_with_playwright(url, output_folder):
    """Scrapes images by rendering the page and waiting for a specific element."""
    
    print(f"--- Starting Playwright Scraper for: {url} ---")
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output directory: {output_folder}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(url, timeout=60000)

            # 1. CRITICAL FIX: Wait for the specific element you found to appear.
            # The structure is: div[data-page-index] -> div[class="pf w0 h18"] -> img
            # We can wait for the first image tag's parent to ensure rendering has started.
            
            # This selector waits for ANY element with the class 'page-content'
            print("Waiting for key document element to appear...")
            page.wait_for_selector('.page-content', timeout=20000) # Wait up to 20 seconds
            print("Key element found.")
            
            # 2. Force more pages to load by scrolling down
            print("Scrolling down to load additional pages...")
            for _ in range(3): # Scroll a few times to force lazy-loading
                 page.mouse.wheel(0, 1500) # Scroll down 1500px
                 time.sleep(2) # Give it time to load after scrolling

            # 3. Get the fully rendered HTML content
            page_source = page.content()
            
            print("Webpage successfully rendered and page source retrieved.")

            # 4. Parse the HTML using BeautifulSoup
            soup = BeautifulSoup(page_source, 'html.parser')

            # 5. Find all image tags
            # Since you confirmed they are <img> tags, this is the focus.
            image_tags = soup.find_all('img')
            
            # You might also look for images inside the page divs specifically
            # document_page_divs = soup.find_all('div', class_='page-content')

            print(f"Found {len(image_tags)} <img> tags in the rendered source.")

            image_urls = []
            for img in image_tags:
                src = img.get('src') or img.get('data-src')
                
                if src:
                    absolute_url = urljoin(url, src)
                    
                    # Ensure it's not a tiny tracking pixel, but a document asset
                    if 'studocu.com/' in absolute_url and not absolute_url.startswith('data:'):
                        image_urls.append(absolute_url)

            # 6. Remove duplicates and start downloading
            unique_image_urls = set(image_urls)
            print(f"\nFound {len(unique_image_urls)} unique document image URLs to download.")
            
            # IMPORTANT: This may still only download the *preview* pages 
            # if the full document requires a subscription/login.

            if len(unique_image_urls) > 0:
                print("--- Starting Downloads ---")
                for img_url in unique_image_urls:
                    download_image(img_url, output_folder)
            else:
                 print("No unique document images found. The content is likely paywalled/not fully rendered.")
                
            print("\n--- Scraping Complete! ---")

        except Exception as e:
            print(f"\n--- FATAL ERROR during Playwright session ---\n{e}")
            print("This usually means the page took too long to load or the selector failed.")
        finally:
            browser.close()

# --- Execute the scraper ---
if __name__ == "__main__":
    scrape_images_with_playwright(TARGET_URL, OUTPUT_DIR)