from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import random
import os

class Snapchat:
    def __init__(self, path_delay=5, driver_arguments=[]):
        self.path_delay = path_delay
        self.driver_arguments = ["--window-size=1920,1080", "--disable-gpu", "--start-maximized", "--no-sandbox", f"--user-data-dir={os.path.join(os.path.dirname(__file__), 'driver')}"]
        self.driver_arguments.extend(driver_arguments)
        
    def driver(self):
        options = webdriver.ChromeOptions()
        for option in self.driver_arguments:
            options.add_argument(option)
            
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
        driver.get("https://web.snapchat.com/")
        return driver
    
    def farm_points(self):
        driver = self.driver()
        wait = WebDriverWait(driver, self.path_delay)

        friends_path = By.CLASS_NAME, "FiLwP"
        snap_take_button_path = By.CLASS_NAME, "HEkDJ"
        take_snap_path = By.CLASS_NAME, "UEYhD"
        choice_users_path = By.CLASS_NAME, "RbA83"
        confirm_snap_path = By.XPATH, "/html/body/div[3]/div/div/div/div/div/div/div[2]/div/form/div[2]/button"

        driver.get("https://web.snapchat.com/")

        while True:
            try:
                friends = wait.until(EC.presence_of_all_elements_located(friends_path))
                listo = [user for user in friends if friends[-1].text != user.text]
                for user in listo.copy():
                    user.click()
                    button = wait.until(EC.element_to_be_clickable(snap_take_button_path))
                    button.click()
                    buttons = wait.until(EC.presence_of_all_elements_located(take_snap_path))
                    random.choice(buttons).click()
                    buttons = wait.until(EC.presence_of_all_elements_located(choice_users_path))
                    clicked = []
                    for btn in buttons:
                        if btn.text not in clicked:
                            btn.click()
                            clicked.append(btn.text)
                    button = wait.until(EC.element_to_be_clickable(confirm_snap_path))
                    button.click()
            except Exception:
                action_chains = ActionChains(driver)
                html_element = driver.find_element(By.TAG_NAME, "html")
                action_chains.move_to_element_with_offset(html_element, 0, 0).click().perform()     


snapchat = Snapchat()
snapchat.farm_points()
