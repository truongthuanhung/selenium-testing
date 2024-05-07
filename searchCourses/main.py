from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import sys

USERNAME = 'student'
PASSWORD = 'moodle'
 
class MoodleTest():
    def __init__(self, username, password, df):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()
        self.df = df
        
    def log_in(self):
        log_in_button = self.driver.find_element(By.LINK_TEXT, 'Log in')
        log_in_button.click()
        username_input = self.driver.find_element(By.NAME, 'username')
        username_input.clear()
        username_input.send_keys(self.username)
        password_input = self.driver.find_element(By.NAME, 'password')
        password_input.clear()
        password_input.send_keys(self.password + Keys.ENTER)
        time.sleep(3)
    
    def log_out(self):
        menu_toggle_element = self.driver.find_element(By.ID, 'user-menu-toggle')
        menu_toggle_element.click()
        log_out_button = self.driver.find_element(By.LINK_TEXT, 'Log out')
        log_out_button.click()
        time.sleep(3)
            
    def search_courses(self):
          for i in range(len(self.df)):
               self.log_in()
               if not pd.isna(self.df.iloc[i]["GROUP"]):
                    grouping_dropdown_element = self.driver.find_element(By.XPATH , "//section/div/div/div/div/div/div/button")
                    grouping_dropdown_element.click()
                    time.sleep(2)
                    group_value = self.df.iloc[i]["GROUP"]
                    grouping_element = self.driver.find_element(By.XPATH, f'//a[contains(text(), "{group_value}")]')
                    grouping_element.click()
                    time.sleep(2)
                
               search_course_element = self.driver.find_element(By.NAME, "search")
               search_course_element.click()
               search_course_element.clear()
               search_course_element.send_keys(self.df.iloc[i]["SEARCH"])
               time.sleep(2)
               
               if self.df.iloc[i]["EXPECT"] == "No courses":
                    verify_text = self.driver.find_element(By.XPATH , '''//p''')
                    
                    if verify_text.text == "No courses":
                         print("Passed search field is" , self.df.iloc[i]["SEARCH"])
                    else:
                         print("No courses - Failed search field is" , self.df.iloc[i]["SEARCH"])
                         
               elif self.df.iloc[i]["EXPECT"] == "Activity examples":
                    verify_text = self.driver.find_element(By.CSS_SELECTOR , "#course-info-container-2-3 > div > div > a > span.multiline > span.sr-only")
                    
                    if verify_text.text == "Activity examples":
                         print("Activity examples - Passed search field is" , self.df.iloc[i]["SEARCH"])
                    else:
                         print("Activity examples - Failed search field is", self.df.iloc[i]["SEARCH"])
               
               time.sleep(2)
               self.log_out()
               
    def run_test(self):
          self.driver.get('https://qa.moodledemo.net/')
          
          # self.driver.maximize_window()
     
          self.search_courses()
          
        
# RUN TEST
 
test = MoodleTest(USERNAME, PASSWORD, pd.read_excel(sys.argv[1]))

test.run_test()

test.driver.quit()


 
