import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pandas as pd
import sys

class SearchActivityUsecase():

    def __init__(self, username, password, data):

        self.data = data
        self.login_path = "https://qa.moodledemo.net/"
        self.target_path = "https://qa.moodledemo.net/my/courses.php"
        self.driver = webdriver.Chrome()
        self.username = username
        self.password = password
        self.driver.implicitly_wait(30)  # Set an implicit wait time of 10 seconds
        self.driver.set_script_timeout(30)
  
    def quit(self):
        self.driver.quit()
          
    def log_in(self):

        self.driver.get(self.login_path)
        self.driver.maximize_window()
        # click log in button
        log_in_button = self.driver.find_element(By.LINK_TEXT, 'Log in')
        log_in_button.click()
        # get input element
        username_input = self.driver.find_element(By.NAME, 'username')
        password_input = self.driver.find_element(By.NAME, 'password')
        # Clear input fields
        username_input.send_keys(Keys.CONTROL + "a")
        username_input.send_keys(Keys.DELETE)
        password_input.send_keys(Keys.CONTROL + "a")
        password_input.send_keys(Keys.DELETE)
        # fill in the input and submit
        username_input.send_keys(self.username)
        password_input.send_keys(self.password + Keys.ENTER)
        time.sleep(5)
    
    def log_out(self):

        menu_toggle_element = self.driver.find_element(By.ID, 'user-menu-toggle')
        menu_toggle_element.click()
        log_out_button = self.driver.find_element(By.LINK_TEXT, 'Log out')
        log_out_button.click()
    
    def enter_dashboard(self):

        # self.driver.find_element(By.XPATH,"//a[contains(@class, 'nav-link') and contains(text(), 'Dasboard')]").click()
        self.driver.find_element(By.LINK_TEXT, "Dashboard").click()
        time.sleep(5)
    
    def get_test_data(self, idx):
        return self.data.iloc[idx - 1, 1], self.data.iloc[idx - 1, 2], self.data.iloc[idx - 1, 3], self.data.iloc[idx - 1, 4]
    
    def run_test_1(self, idx=1):

        # Get testdata
        group_data, sort_data, search_data, expected_data = self.get_test_data(idx)

        # Filter by Group
        self.driver.find_element(By.ID, "timeline-day-filter-current-selection").click()
        self.driver.find_element(By.LINK_TEXT, group_data).click()
        time.sleep(1)

        # Filter by Sort
        self.driver.find_element(By.ID, "timeline-view-selector-current-selection").click()
        self.driver.find_element(By.LINK_TEXT, sort_data).click()
        time.sleep(1)

        # Enter search input
        self.driver.find_element(By.NAME, "search").click()
        self.driver.find_element(By.NAME, "search").send_keys(search_data)
        time.sleep(3)

        # Verify output
        output_data = self.driver.find_element(By.LINK_TEXT, f"{expected_data}").text
        
        print(output_data)
        print(expected_data)

        return output_data == expected_data
    
    def run_test_2(self, idx=2):

        # Get testdata
        group_data, sort_data, search_data, expected_data = self.get_test_data(idx)

         # Filter by Group
        self.driver.find_element(By.ID, "timeline-day-filter-current-selection").click()
        self.driver.find_element(By.LINK_TEXT, group_data).click()
        time.sleep(1)

        # Filter by Sort
        self.driver.find_element(By.ID, "timeline-view-selector-current-selection").click()
        self.driver.find_element(By.LINK_TEXT, sort_data).click()
        time.sleep(1)

        # Enter search input
        self.driver.find_element(By.NAME, "search").click()
        self.driver.find_element(By.NAME, "search").send_keys(search_data)
        time.sleep(3)

        # Verify output
        output_data = self.driver.find_element(By.LINK_TEXT, f"{expected_data}").text
        
        return output_data == expected_data


    def run_all(self, numOfTests = 2):

        self.log_in()

        for i in range(0, numOfTests):
            
            output = None
            
            try:
                self.enter_dashboard()
                output = self.__getattribute__(f"run_test_{i+1}")()
            except Exception as e:
                print(e)
            finally:
                if output == True: print(f"Test {i+1} passed")
                elif output == False: print(f"Test {i+1} failed")
                else:
                    print(f"Test {i+1} run error")

            time.sleep(2)

        self.log_out()

def main(data_filename):

    data_path = 'Search_Activity/data' + f'/{data_filename}.xlsx'
    test = SearchActivityUsecase("student10", "moodle", pd.read_excel(data_path))

    # Start testcases
    test.run_all()
    test.quit()

