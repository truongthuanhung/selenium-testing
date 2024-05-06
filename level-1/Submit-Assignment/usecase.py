import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from dragDrop import drop_file
import pandas as pd
import sys

class SubmitAssignment():

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

        self.driver.find_element(By.XPATH,"//a[contains(@class, 'nav-link') and contains(text(), 'My courses')]").click()
        self.driver.find_element(By.XPATH, "//a[contains(@class, 'coursename') and contains(., 'Activity examples')]").click()
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
        input_data, expected_data = self.get_test_data(idx)

        self.driver.find_element(By.XPATH, "//button[contains(.,\'Add submission\')]").click()
        # Click to open Input form
        self.driver.find_element(By.CSS_SELECTOR, ".fa-file-o").click()
        element = self.driver.find_element(By.CSS_SELECTOR, ".fa-file-o")

        # Input form
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

        # Open a file
        self.driver.find_element(By.XPATH, "//span[contains(.,\'Upload a file\')]").click()
        self.driver.find_element(By.NAME, "repo_upload_file").send_keys(input_data) # Upload data

        # Change file name
        self.driver.find_element(By.XPATH, "//div/div[2]/input").click()
        self.driver.find_element(By.XPATH, "//div/div[2]/input").send_keys("Normal-file")

        # Upload file
        self.driver.find_element(By.XPATH, "//button[contains(.,\'Upload this file\')]").click()

        # Verify file
        WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".fp-reficons2")))
        WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//input[@id=\'id_submitbutton\']")))

        # Submit file
        self.driver.find_element(By.ID, "id_submitbutton").click()
        self.driver.find_element(By.CSS_SELECTOR, ".submissionstatussubmitted").click()

        # Verify successfully
        output_data = self.driver.find_element(By.XPATH, "//td[contains(.,\'Submitted for grading\')]").text
        assert output_data == expected_data
        
        return output_data == expected_data
    
    def run_test_2(self, idx=2):

        # Get testdata
        input_data, expected_data = self.get_test_data(idx)

        self.driver.find_element(By.XPATH, "//button[contains(.,\'Add submission\')]").click()

        # TODO perform drag and drop file

        # Find the drop target element
        drop_target = self.driver.find_element(By.CSS_SELECTOR, ".dndupload-message > .dndupload-arrow")
        drop_target.click()
        time.sleep(1)

        # Find the file input element
        file_input = self.driver.find_element(By.NAME, "repo_upload_file")
        file_input.send_keys(input_data)
        time.sleep(2)

        # Upload file
        self.driver.find_element(By.XPATH, "//button[contains(.,\'Upload this file\')]").click()

        # Verify file
        WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".fp-reficons2")))
        self.driver.find_element(By.CSS_SELECTOR, ".fp-reficons2").click()

        # Change file name
        self.driver.find_element(By.XPATH, "//form/div[2]/div/input").click()
        self.driver.find_element(By.XPATH, "//form/div[2]/div/input").send_keys("normal.pdf")
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//button[contains(.,\'Update\')]").click()

        # Submit file
        self.driver.find_element(By.ID, "id_submitbutton").click()

        # Verify successfully
        output_data = self.driver.find_element(By.XPATH, "//td[contains(.,\'Submitted for grading\')]").text
        assert output_data == expected_data
        
        return output_data == expected_data

    def run_test_3(self, idx=3):

        # Get testdata
        input_data, expected_data = self.get_test_data(idx)

        self.driver.find_element(By.XPATH, "//button[contains(.,\'Add submission\')]").click()
        # Create folder
        self.driver.find_element(By.CSS_SELECTOR, ".fa-folder-o").click()
        # elements = self.driver.find_elements(By.XPATH, "//div[7]/div[3]/div/div[2]/div/div/input")
        # assert len(elements) > 0

        # Change folder name
        # self.driver.find_element(By.XPATH, "//div[7]/div[3]/div/div[2]/div/div/input").send_keys("folder")
        self.driver.find_element(By.XPATH, "//input[@class='form-control' and @data-initial-value='New folder']").send_keys("folder")
        self.driver.find_element(By.XPATH, "//button[contains(.,\'Create folder\')]").click()
        time.sleep(5)
        
        # File input form
        self.driver.find_element(By.CSS_SELECTOR, ".fp-reficons2").click()
        self.driver.find_element(By.CSS_SELECTOR, ".fa-file-o").click()
        time.sleep(2)

        # Upload file
        self.driver.find_element(By.XPATH, "//form/div/div/div/input").send_keys(input_data)
        self.driver.find_element(By.XPATH, "//button[contains(.,\'Upload this file\')]").click()
        time.sleep(2)

        # Verify file
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".fp-reficons2")
        assert len(elements) > 0

        # Submit file
        self.driver.find_element(By.ID, "id_submitbutton").click()

        # Verify successfully
        output_data = self.driver.find_element(By.XPATH, "//td[contains(.,\'Submitted for grading\')]").text
        assert output_data == expected_data

        return output_data == expected_data

    def run_test_4(self, idx=4):

        # Get testdata
        input_data, expected_data = self.get_test_data(idx)

        self.driver.find_element(By.XPATH, "//button[contains(.,\'Add submission\')]").click()
        # Click to open Input form
        self.driver.find_element(By.CSS_SELECTOR, ".fa-file-o").click()
        element = self.driver.find_element(By.CSS_SELECTOR, ".fa-file-o")

        # Input form
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

        # Open a file
        self.driver.find_element(By.XPATH, "//span[contains(.,\'Upload a file\')]").click()
        self.driver.find_element(By.NAME, "repo_upload_file").send_keys(input_data) # Upload data
        time.sleep(2)

        # Change file name
        self.driver.find_element(By.XPATH, "//div/div[2]/input").click()
        self.driver.find_element(By.XPATH, "//div/div[2]/input").send_keys("Normal-file")
        time.sleep(2)

        # Upload file
        self.driver.find_element(By.XPATH, "//button[contains(.,\'Upload this file\')]").click()

        # Verify file
        WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".fp-reficons2")))
        WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//input[@id=\'id_submitbutton\']")))

        # Submit file
        self.driver.find_element(By.ID, "id_submitbutton").click()
        self.driver.find_element(By.CSS_SELECTOR, ".submissionstatussubmitted").click()

        # Verify successfully
        output_data = self.driver.find_element(By.XPATH, "//td[contains(.,\'Submitted for grading\')]").text
        assert output_data == expected_data
        
        return output_data == expected_data

    def run_test_5(self, idx=5):

        # Get testdata
        _, expected_data = self.get_test_data(idx)

        self.driver.find_element(By.XPATH, "//button[contains(.,\'Add submission\')]").click()

        # Submit file
        self.driver.find_element(By.ID, "id_submitbutton").click()
        # self.driver.find_element(By.CSS_SELECTOR, ".alert").click()

        # Verify alert
        output_data = self.driver.find_element(By.CSS_SELECTOR, ".alert").text
        assert output_data == expected_data

        return output_data == expected_data

    def run_all(self, numOfTests = 5):

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
                
                if output == True and (i != 4): self.remove_file()

        self.log_out()

def main(data_filename):

    data_path = './data' + f'/{data_filename}.xlsx'
    test = SubmitAssignment("student10", "moodle", pd.read_excel(data_path))

    # Start testcases
    test.run_all()
    test.quit()

main(sys.argv[1])

