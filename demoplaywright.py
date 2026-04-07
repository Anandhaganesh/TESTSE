#from   playwright.async_api import async_playwright
#import asyncio


#async def playwright_function():
    #async with async_playwright() as p:
    #browser = await p.chromium.launch(headless=False)
    #pages = await browser.new_page()

    #navigation
    #await pages.go("https://www.google.com")

#if _name_== "_main_"
#asyncio.run(playwright_function()) 
from playwright.sync_api import sync_playwright
import time

def get_current_hora():
    with sync_playwright() as p:
        # 1. Launch the browser (headless=False lets you see it happen)
        print("Launching browser...")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 2. Go to Google
        print("Navigating to Google...")
        page.goto("https://www.google.com")

        # 3. Handle the search bar
        # Instead of coordinates, we use the 'name' attribute of the search box
        search_bar = page.get_by_role("combobox")
        search_bar.fill("current hora of the day in Chennai")
        search_bar.press("Enter")

        # 4. Wait for results to load
        print("Waiting for search results...")
        page.wait_for_load_state("networkidle")

        # 5. Click the first relevant link
        # We look for a link containing 'Hora' or 'Panchangam'
        # 'nth(0)' ensures we grab the very first result
        first_result = page.locator("h3").nth(0)
        print(f"Opening: {first_result.inner_text()}")
        first_result.click()

        # Keep it open for 10 seconds so you can read the Hora
        time.sleep(10)
        
        browser.close()

if __name__ == "__main__":
    get_current_hora()