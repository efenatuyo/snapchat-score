from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import random
import os
import time

class Snapchat:
    def __init__(self, username, password, path_delay=10):
        self.username = username
        self.password = password
        self.path_delay = path_delay
        self.driver_arguments = [
            "--window-size=1920,1080", 
            "--disable-gpu", 
            "--start-maximized", 
            "--no-sandbox", 
            f"--user-data-dir={os.path.join(os.path.dirname(__file__), 'driver')}",
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        
    def driver_init(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        for option in self.driver_arguments:
            options.add_argument(option)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return self.driver

    def login(self):
        self.driver.get("https://web.snapchat.com/")
        wait = WebDriverWait(self.driver, self.path_delay)
        
        try:
            # Check if we are already logged in (look for the friends list)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "FiLwP")))
            print("Already logged in.")
        except TimeoutException:
            print("Login required. Entering credentials...")
            try:
                # Enter Username
                user_field = wait.until(EC.element_to_be_clickable((By.ID, "account_identifier")))
                user_field.send_keys(self.username)
                self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
                
                # Enter Password
                pass_field = wait.until(EC.element_to_be_clickable((By.ID, "password")))
                time.sleep(random.uniform(1, 2))
                pass_field.send_keys(self.password)
                self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
                
                print("Checking for 2FA... Please solve manually if prompted.")
                # Long wait for 2FA or page load
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "FiLwP")))
            except Exception as e:
                print(f"Login failed: {e}")

    def farm_points(self):
        self.driver_init()
        self.login()
        
        wait = WebDriverWait(self.driver, self.path_delay)
        start_time = time.time()
        
        # Selectors (Keep updated based on site changes)
        friends_path = By.CLASS_NAME, "FiLwP"
        snap_take_button_path = By.CLASS_NAME, "HEkDJ"
        take_snap_path = By.CLASS_NAME, "UEYhD"
        choice_users_path = By.CLASS_NAME, "RbA83"
        confirm_snap_path = By.XPATH, "//button[contains(text(), 'Send')]" 

        while True:
            # 4-hour Break Logic
            if time.time() - start_time > (4 * 3600):
                pause = random.randint(600, 900)
                print(f"Taking a {pause/60:.1f} min break...")
                time.sleep(pause)
                start_time = time.time()

            try:
                friends = wait.until(EC.presence_of_all_elements_located(friends_path))
                listo = [u for u in friends if friends[-1].text != u.text]
                
                for user in listo.copy():
                    time.sleep(random.uniform(2, 4))
                    user.click()
                    
                    wait.until(EC.element_to_be_clickable(snap_take_button_path)).click()
                    time.sleep(random.uniform(1, 2))
                    
                    random.choice(wait.until(EC.presence_of_all_elements_located(take_snap_path))).click()
                    
                    btns = wait.until(EC.presence_of_all_elements_located(choice_users_path))
                    for b in btns:
                        time.sleep(random.uniform(0.2, 0.5))
                        b.click()
                    
                    wait.until(EC.element_to_be_clickable(confirm_snap_path)).click()
                    
                    # Randomized delay between batches
                    cycle_delay = random.uniform(30, 300)
                    print(f"Batch sent. Sleeping {cycle_delay:.1f}s")
                    time.sleep(cycle_delay)

            except Exception:
                self.login() # Re-verify login status on error
                time.sleep(5)

# Usage
snapchat = Snapchat(username="YOUR_USER", password="YOUR_PASSWORD")
snapchat.farm_points()
