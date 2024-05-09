import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pandas as pd

class SubmitAssignmentBoundary():

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
    
    def enter_assignment(self):
        
        self.driver.find_element(By.LINK_TEXT, "My courses").click()
        self.driver.find_element(By.LINK_TEXT, "Activity examples").click()
        self.driver.find_element(By.LINK_TEXT, "Assignment with file submissions").click()
        time.sleep(5)
    
    def get_test_data(self, idx):
        return self.data.iloc[idx - 1, 1], self.data.iloc[idx - 1, 2]
    
    def remove_file(self):

        # Verify current page
        assert self.driver.find_element(By.XPATH, "//td[contains(.,\'Submitted for grading\')]").text == "Submitted for grading"
        self.driver.find_element(By.XPATH, "//button[contains(.,\'Remove submission\')]").click()

        # Click remove
        assert self.driver.find_element(By.XPATH, "//p[contains(.,\'Are you sure you want to remove your submission?\')]").text == "Are you sure you want to remove your submission?"
        self.driver.find_element(By.XPATH, "//button[contains(.,\'Continue\')]").click()

        assert self.driver.find_element(By.XPATH, "//td[contains(.,\'No submissions have been made yet\')]").text == "No submissions have been made yet"

    def run_test_1(self, idx=1):

        # Get testdata
        _, expected_data = self.get_test_data(idx)

        self.driver.find_element(By.XPATH, "//button[contains(.,\'Add submission\')]").click()

        # Submit file
        self.driver.find_element(By.ID, "id_submitbutton").click()

        # Verify alert
        output_data = self.driver.find_element(By.CSS_SELECTOR, ".alert").text
        print(f"Testcase #{idx} output: {output_data}")
        print(f"Testcase #{idx} expected: {expected_data}")

        return output_data == expected_data
    
    def run_test_2(self, idx=2):

        # Get testdata
        input_data, expected_data = self.get_test_data(idx)

        self.driver.find_element(By.XPATH, "//button[contains(.,\'Add submission\')]").click()
        
        # Upload file
        self.upload_file(input_data)

        # Verify file
        WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".fp-reficons2")))
        WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//input[@id=\'id_submitbutton\']")))

        # Submit file
        self.driver.find_element(By.ID, "id_submitbutton").click()

        # Verify successfully
        output_data = self.driver.find_element(By.XPATH, f"//td[contains(.,\'{expected_data}\')]").text
        print(f"Testcase #{idx} output: {output_data}")
        print(f"Testcase #{idx} expected: {expected_data}")
        
        return output_data == expected_data
    
    def run_test_3(self, idx=3):

        # Get testdata
        input_data, expected_data = self.get_test_data(idx)
        input_data = input_data.split('\n')

        self.driver.find_element(By.XPATH, "//button[contains(.,\'Add submission\')]").click()
        
        # Upload file 1
        self.upload_file(input_data[0])
        # Verify file 1
        WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".fp-reficons2")))

        # Upload file 2
        self.upload_file(input_data[1])
        # Verify file 1, 2
        WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, "//a/div/div[3]")))
        WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, "//div[2]/a/div/div[3]")))

        # Submit file
        WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//input[@id=\'id_submitbutton\']")))
        self.driver.find_element(By.ID, "id_submitbutton").click()

        # Verify successfully
        output_data = self.driver.find_element(By.XPATH, f"//td[contains(.,\'{expected_data}\')]").text
        print(f"Testcase #{idx} output: {output_data}")
        print(f"Testcase #{idx} expected: {expected_data}")
        
        return output_data == expected_data
    
    def run_test_4(self, idx=4):

        # Get testdata
        input_data, expected_data = self.get_test_data(idx)
        input_data = input_data.split('\n')

        self.driver.find_element(By.XPATH, "//button[contains(.,\'Add submission\')]").click()
        
        # Upload file 1
        self.upload_file(input_data[0])
        # Verify file 1
        WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".fp-reficons2")))

        # Upload file 2
        self.upload_file(input_data[1])
        # Verify file 1, 2
        WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, "//a/div/div[3]")))
        WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, "//div[2]/a/div/div[3]")))

        # Verify upload button
        # WebDriverWait(self.driver, 2).until(expected_conditions.invisibility_of_element_located((By.CSS_SELECTOR, ".fa-file-o")))
        element = self.driver.find_element(By.CSS_SELECTOR, ".fa-file-o")
        output_data = element.is_displayed()

        print(f"Testcase #{idx} output: {output_data}")
        print(f"Testcase #{idx} expected: {expected_data}")
        
        return output_data == expected_data

    def upload_file(self, file_path):

        # Click to open Input form
        self.driver.find_element(By.CSS_SELECTOR, ".fa-file-o").click()
        element = self.driver.find_element(By.CSS_SELECTOR, ".fa-file-o")

        # Input form
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

        # Open a file
        self.driver.find_element(By.XPATH, "//span[contains(.,\'Upload a file\')]").click()
        self.driver.find_element(By.NAME, "repo_upload_file").send_keys(file_path) # Upload data

        # Upload file
        self.driver.find_element(By.XPATH, "//button[contains(.,\'Upload this file\')]").click()

    def run_all(self, numOfTests = 4):

        self.log_in()

        for i in range(0, numOfTests):
            
            output = None
            
            try:
                self.enter_assignment()
                output = self.__getattribute__(f"run_test_{i+1}")()
            except Exception as e:
                print(e)
            finally:
                if output == True: print(f"Test {i+1} passed")
                elif output == False: print(f"Test {i+1} failed")
                else:
                    print(f"Test {i+1} run error")
                
                if output == True and (i not in [0, 3]): self.remove_file()

        self.log_out()

def main(data_filename):

    data_path = 'Submit_Assignment/data' + f'/{data_filename}.xlsx'
    test = SubmitAssignmentBoundary("student10", "moodle", pd.read_excel(data_path))

    # Start testcases
    test.run_all()
    test.quit()