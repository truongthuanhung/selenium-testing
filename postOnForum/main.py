from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
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
          time.sleep(3)
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
          time.sleep(2)
            
    def postToForum(self):
          for i in range(len(self.df)):
               self.log_in()
               
               self.driver.find_element(By.XPATH, "//div/div/div/div/div/a/div").click()
               
               time.sleep(2)
               self.driver.find_element(By.LINK_TEXT, f'{self.df.iloc[i]["FORUM"]}').click()
               
               time.sleep(2)
               self.driver.find_element(By.LINK_TEXT, "Add discussion topic").click()
          
               time.sleep(3)
               if not pd.isna(self.df.iloc[i]["ADVANDED_MODE"]):
                    self.driver.find_element(By.NAME, "advancedadddiscussion").click()
                    time.sleep(3)
                
                    
               
               if not pd.isna(self.df.iloc[i]["SUBJECT"]):
                    subject_element = self.driver.find_element(By.NAME, "subject")
                    subject_element.send_keys(self.df.iloc[i]["SUBJECT"])
                    time.sleep(3)
                
                    
                    
               if not pd.isna(self.df.iloc[i]["MESSAGE"]):
                    self.driver.switch_to.frame(0)
                    self.driver.find_element(By.CSS_SELECTOR, "html").click()
                    element = self.driver.find_element(By.XPATH, "//body[@id=\'tinymce\']")
                    self.driver.execute_script(f"if(arguments[0].contentEditable === 'true') {{arguments[0].innerText = '{self.df.iloc[i]['MESSAGE']}'}}", element)
                    self.driver.switch_to.default_content()
                    time.sleep(3)
                 
                    
                    
               if not pd.isna(self.df.iloc[i]["ATTACHMENT"]):    
                    self.driver.find_element(By.XPATH , "//div/div[2]/div/div/div/a/i").click()
                    time.sleep(3)
                    self.driver.find_element(By.LINK_TEXT , "Recent files").click()
                    time.sleep(3)
                    self.driver.find_element(By.XPATH , "//a/div/div[3]").click()
                    time.sleep(3)
                    self.driver.find_element(By.XPATH , "//form/div[4]/div/button").click()
                    time.sleep(3)

               
               
               prevMethod = self.method
               self.method = self.df.iloc[i]["METHOD_TEST"]
               if self.method != prevMethod:
                    print(self.method)
                    
               
               if not pd.isna(self.df.iloc[i]["ACTION"]):    
                    if self.df.iloc[i]["ACTION"] == "submit":
                         self.driver.find_element(By.NAME, "submitbutton").click()
                         time.sleep(5)
                    elif self.df.iloc[i]["ACTION"] == "cancel":
                         if not pd.isna(self.df.iloc[i]["ADVANDED_MODE"]):
                              self.driver.find_element(By.NAME, "cancel").click()
                         else:
                              self.driver.find_element(By.NAME, "cancelbtn").click()
                         time.sleep(5)
                       
               
               if not pd.isna(self.df.iloc[i]["VERIFY_TEST"]):    
                    if self.df.iloc[i]["VERIFY_TEST"] == "Your post was successfully added.":
                         message_element = self.driver.find_element(By.XPATH, "//p")
                         message_element_text = message_element.text
                         if message_element_text == self.df.iloc[i]["VERIFY_TEST"]:
                              print("PASS - " , self.df.iloc[i]["TC_ID"])
                         else:
                              print("FAILED - " , self.df.iloc[i]["TC_ID"])
                              time.sleep(3)
                              
                    elif self.df.iloc[i]["VERIFY_TEST"] == "Required":
                         if pd.isna(self.df.iloc[i]["SUBJECT"]):
                              message_element = self.driver.find_element(By.XPATH, "//div[@id='id_error_subject']")
                         else:
                              message_element = self.driver.find_element(By.XPATH, "//div[@id='id_error_message']")
                              
                         message_element_text = message_element.text
                         if message_element_text == "- " + self.df.iloc[i]["VERIFY_TEST"]:
                              print("PASS - " , self.df.iloc[i]["TC_ID"])
                         else:
                              print("FAILED - " , self.df.iloc[i]["TC_ID"])
                              time.sleep(3)
                              
                    elif self.df.iloc[i]["VERIFY_TEST"] == "Maximum of 255 characters":
                         message_element = self.driver.find_element(By.ID, "id_error_subject")
                         message_element_text = message_element.text
                         if message_element_text == "- " + self.df.iloc[i]["VERIFY_TEST"]:
                              print("PASS - " , self.df.iloc[i]["TC_ID"])
                         else:
                              print("FAILED - " , self.df.iloc[i]["TC_ID"])
                              time.sleep(3)
               else:
                    print("PASS - " , self.df.iloc[i]["TC_ID"])
                    time.sleep(3)
               
               self.log_out()
               
               
    def run_test(self):
         
          self.driver.get('https://qa.moodledemo.net/')
          
          self.postToForum()
           
          
        
# RUN TEST
 
test = MoodleTest(USERNAME, PASSWORD, pd.read_excel(sys.argv[1]))

test.run_test()

test.driver.quit()


 
