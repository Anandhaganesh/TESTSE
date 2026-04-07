from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# 1. Setup Driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.maximize_window()

# 2. Define a standard wait (10 seconds timeout)
wait = WebDriverWait(driver, 10)

try:
    # --- TEST 1: Checkboxes (Using Explicit Wait to avoid IndexError) ---
    print("Test 1: Checkboxes")
    driver.get("https://the-internet.herokuapp.com/checkboxes")
    
    # Wait until at least one input tag is present
    checkboxes = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "input")))
    
    if len(checkboxes) > 0:
        if not checkboxes[0].is_selected():
            checkboxes[0].click()
        print(f"Success: Found {len(checkboxes)} checkboxes and clicked the first one.")

    # --- TEST 2: Form Authentication ---
    print("\nTest 2: Login Form")
    driver.get("https://the-internet.herokuapp.com/login")
    
    # Wait for the username field to be interactable
    user_field = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    user_field.send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # Verify success by waiting for the flash message
    flash = wait.until(EC.presence_of_element_located((By.ID, "flash")))
    print(f"Login Result: {'Success' in flash.text}")

    # --- TEST 3: Dropdown ---
    print("\nTest 3: Dropdown Menu")
    driver.get("https://the-internet.herokuapp.com/dropdown")
    
    dropdown_element = wait.until(EC.presence_of_element_located((By.ID, "dropdown")))
    dropdown = Select(dropdown_element)
    dropdown.select_by_visible_text("Option 2")
    print("Selected Option 2 successfully.")

    # --- TEST 4: Add/Remove Elements ---
    print("\nTest 4: Adding Elements")
    driver.get("https://the-internet.herokuapp.com/add_remove_elements/")
    
    add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Add Element']")))
    for i in range(3):
        add_btn.click()
    
    # Wait for the buttons to actually appear in the DOM
    delete_btns = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "added-manually")))
    print(f"Verified: {len(delete_btns)} buttons added manually.")

    # --- TEST 5: Status Codes ---
    print("\nTest 5: Status Codes (404)")
    driver.get("https://the-internet.herokuapp.com/status_codes")
    
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "404"))).click()
    content = wait.until(EC.presence_of_element_located((By.TAG_NAME, "p"))).text
    if "404" in content:
        print("Verified 404 status message on the page.")

except Exception as e:
    print(f"\nAn error occurred: {e}")

finally:
    print("\nCleaning up... Closing browser in 3 seconds.")
    time.sleep(3)
    driver.quit()