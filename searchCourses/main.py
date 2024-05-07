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
        self.method = None
        
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
               
               prevMethod = self.method
               self.method = self.df.iloc[i]["METHOD_TEST"]
               if self.method != prevMethod:
                    print(self.method)
               
               if self.df.iloc[i]["EXPECT"] == "No courses":
                    time.sleep(2)
                    verify_text = self.driver.find_element(By.XPATH , "//p")
                    
                    if verify_text.text == "No courses":
                         print("PASS - " , self.df.iloc[i]["TC_ID"])
                    else:
                         print("FAILED - " , self.df.iloc[i]["TC_ID"] , " - EXPECT:" , self.df.iloc[i]["EXPECT"], " - RESULT",self.df.iloc[i]["NOTE"]  )
                         
               elif self.df.iloc[i]["EXPECT"] == "Activity examples":
                    time.sleep(2)
                    verify_text = self.driver.find_element(By.XPATH , "//span[3]/span[2]")
                    
                    if verify_text.text == "Activity examples":
                         print("PASS - " , self.df.iloc[i]["TC_ID"])
                    else:
                         print("FAILED - " , self.df.iloc[i]["TC_ID"] , " - EXPECT:" , self.df.iloc[i]["EXPECT"], " - RESULT",self.df.iloc[i]["NOTE"]  )
               
               time.sleep(2)
               self.log_out()
               
    def run_test(self):
          self.driver.get('https://qa.moodledemo.net/')
          
          self.driver.maximize_window()
     
          self.search_courses()
          
        
# RUN TEST
 
test = MoodleTest(USERNAME, PASSWORD, pd.read_excel(sys.argv[1]))

test.run_test()

test.driver.quit()


 
